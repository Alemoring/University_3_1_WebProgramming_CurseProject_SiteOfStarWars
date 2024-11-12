<script setup>
import {computed, onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'
import About from './views/AboutView.vue'

const routes = {
  '/about' : About
}
const currentPath = ref(window.location.hash)
window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})
const currentView = computed(() => {
  return routes[currentPath.value.slice(1) || '/' || NotFound ]
})

const characters = ref([])
const races = ref([])
const fractions = ref([])
const characterToAdd = ref({})
const characterToEdit = ref({})

async function fetchCharacters() {
  const r1 = await axios.get("/api/characters/")
  console.log(r1.data)
  characters.value = r1.data
  const r2 = await axios.get("/api/races/")
  console.log(r2.data)
  races.value = r2.data
  const r3 = await axios.get("/api/fractions/")
  console.log(r3.data)
  fractions.value = r3.data
}

async function onCharacterEditClick(character) {
  characterToEdit.value = { ...character };
}

async function onUpdateCharacter() {
  await axios.put(`/api/characters/${characterToEdit.value.id}/`, {
    ...characterToEdit.value,
  });
  await fetchCharacters();
}

async function onCharacterAdd(){
  await axios.post("/api/characters/", {
    "name" : characterToAdd.value.name,
    "race" : characterToAdd.value.race,
    "fraction" : characterToAdd.value.fraction
  })
}

async function onRemoveClick(character) {
  await axios.delete(`api/characters/${character.id}/`)
  await fetchCharacters()
}

async function onLoadClick() {
  await fetchCharacters()
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  await fetchCharacters()
})
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
      <a class="navbar-brand" href="/">Главная</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Переключатель навигации">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="/">Персонажи</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#/about">Рассы</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/fractions">Фракции</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/planets">Планеты</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/starships">Корабли</a>
          </li>
        </ul>
      </div>
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Пользователь</a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="/admin">Админка</a></li>
            </ul>
        </li>
      </ul>
    </div>
  </nav> 
  
  <component :is="currentView" />

  <div>
    <div v-for="item in characters" class="character-item">
      <div>{{ item.name }}</div>
      <div>{{ races[item.race]?.name }}</div>
      <button
        class="btn btn-success"
        @click="onCharacterEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editCharacterModal"
      >
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>
</div>

  <div>
    <button @click="onLoadClick()">Загрузить</button>
  </div>

  <!-- ТУТ ПОДКЛЮЧИЛ обработчик отправки формы -->
<form @submit.prevent.stop="onCharacterAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
        <input
          type="text"
          class="form-control"
          v-model="characterToAdd.name"
          required
        />
        <label for="floatingInput">Имя</label>
      </div>
    </div>
    <div class="col-auto">
        <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
      <div class="form-floating">
        <select class="form-select" v-model="characterToAdd.race" required>
          <option :value="rc.id" v-for="rc in races">{{ rc.name }}</option>
        </select>
        <label for="floatingInput">Расса</label>
      </div>
      <div class="form-floating">
        <select class="form-select" v-model="characterToAdd.fraction" required>
          <option :value="f.id" v-for="f in fractions">{{ f.name }}</option>
        </select>
        <label for="floatingInput">Фракция</label>
      </div>
    </div>
    <div class="col-auto">
      <button class="btn btn-primary">
        Добавить
      </button>
    </div>
  </div>
</form>

<div class="modal fade" id="editCharacterModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            редактировать
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="characterToEdit.name"
                />
                <label for="floatingInput">Имя</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="characterToEdit.race">
                  <option :value="rc.id" v-for="rc in races">
                    {{ rc.name }}
                  </option>
                </select>
                <label for="floatingInput">Расса</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Закрыть
          </button>
          <button
            data-bs-dismiss="modal"
            type="button"
            class="btn btn-primary"
            @click="onUpdateCharacter"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
</div>



</template>

<style scoped></style>