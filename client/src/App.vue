<script setup>
import {computed, onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie';

const characters = ref([])
const races = ref([])
const fractions = ref([])
const characterToAdd = ref({})

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
  <div>
    <div v-for="item in characters" class="character-item">
      <div>{{ item.name }}</div>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>

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

</template>

<style scoped></style>