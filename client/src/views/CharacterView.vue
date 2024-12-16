<script setup>
import { computed, onBeforeMount, onMounted, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'
import { storeToRefs } from "pinia"
import useUserProfileStore from '@/stores/UserProfileStore'



const userProfileStore = useUserProfileStore()
const {
  is_authenticated,
  is_superuser,
  username
} = storeToRefs(userProfileStore)

const users = ref([])

const userFilter = ref()

const characters = ref([])
const characterPictureRef = ref()
const characterPictureEditRef = ref()
const characterAddImageURL = ref()
const characterEditImageURL = ref()
const races = ref([])
const fractions = ref([])
const characterToAdd = ref({})
const characterToEdit = ref({})

async function fetchCharacters() {
  const r1 = await axios.get("/api/characters/")
  characters.value = r1.data
  const r2 = await axios.get("/api/races/")
  races.value = r2.data
  const r3 = await axios.get("/api/fractions/")
  fractions.value = r3.data
  const r4 = await axios.get("/api/users/")
  users.value = r4.data
}

async function onFilterUser(user) {
  await fetchCharacters()
  if (user != -1) {
    characters.value = characters.value.filter((item) => item.user == user + 1)
  }
}

async function charactersAddPictureChange() {
  if (characterPictureRef.value.files[0] != null) {
    characterAddImageURL.value = URL.createObjectURL(characterPictureRef.value.files[0])
  } else {
    characterAddImageURL.value = null
  }
}
async function charactersEditPictureChange() {
  if (characterPictureEditRef.value.files[0] != null) {
    characterEditImageURL.value = URL.createObjectURL(characterPictureEditRef.value.files[0])
  } else {
    characterEditImageURL.value = null
    characterToEdit.value.picture = null
  }
  characterToEdit.value.picture = null
}

async function onCharacterEditClick(character) {
  characterToEdit.value = { ...character };
  characterEditImageURL.value = characterToEdit.value.picture
}

async function onUpdateCharacter() {
  const formData = new FormData()
  if (characterPictureEditRef.value.files[0] != null) {
    formData.append('picture', characterPictureEditRef.value.files[0])

    formData.set('name', characterToEdit.value.name)
    formData.set("race", characterToEdit.value.race)
    formData.set("fraction", characterToEdit.value.fraction)

    await axios.put(`/api/characters/${characterToEdit.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  } else if (characterToEdit.value.picture != null) {
    await axios.put(`/api/characters/${characterToEdit.value.id}/`, {
      'name': characterToEdit.value.name,
      "race": characterToEdit.value.race,
      "fraction": characterToEdit.value.fraction
    });
  }
  else {
    await axios.put(`/api/characters/${characterToEdit.value.id}/`, {
      'name': characterToEdit.value.name,
      "race": characterToEdit.value.race,
      "fraction": characterToEdit.value.fraction,
      "picture": null
    });
  }
  characterPictureEditRef.value = null
  await fetchCharacters();
}

async function onCharacterAdd() {
  const formData = new FormData()
  formData.set('name', characterToAdd.value.name)
  formData.set("race", characterToAdd.value.race)
  formData.set("fraction", characterToAdd.value.fraction)
  if (characterPictureRef.value.files[0] != null) {
    formData.append('picture', characterPictureRef.value.files[0])
    await axios.post("/api/characters/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    characterPictureRef.value = null
  } else {
    await axios.post("/api/characters/", {
      'name': characterToAdd.value.name,
      "race": characterToAdd.value.race,
      "fraction": characterToAdd.value.fraction,
      "picture": null
    })
  }
  await fetchCharacters()
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
  <div class="row">
    <div class="col-1 ">
      <div v-if="userProfileStore.is_superuser" class="form-floating">
        <select id="floatingSelect" class="form-select" v-model="userFilter"
          @change="onFilterUser(users.findIndex((item) => item.username == userFilter.username))">
          <option selected>Все</option>
          <option v-for="n in users" :value="n">{{ n.username }}</option>
        </select>
        <label for="floatingSelect">Юзер</label>
      </div>
    </div>
  </div>
  <div class="row">
    <div v-for="item in characters" class="character-item card m-2" style="width: 18rem;">
      <div v-show="item.picture" class="mt-3 mb-2" style="margin-left: auto; margin-right: auto;"><img
          :src="item.picture"
          style="max-height: 200px; border: 2px solid black; box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.4);" alt="">
      </div>
      <div class="card-title ms-4"> Имя: {{ item.name }}</div>
      <div class="card-text ms-4">Расса: {{ item.race.name }}</div>
      <div class="card-text ms-4">Фракция: {{ item.fraction.name }}</div>
      <div v-if="userProfileStore.is_superuser" class="card-text ms-4">Юзер: {{ users[item.user - 1].username }}</div>
      <div class="mt-2 mb-2 ms-4 me-4" style="display: flex; justify-content: space-between;">
        <button class="btn btn-success" @click="onCharacterEditClick(item)" data-bs-toggle="modal"
          data-bs-target="#editCharacterModal">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger" @click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>

  <div class="mt-2 mb-2">
    <button @click="onLoadClick()">Загрузить</button>
  </div>

  <!-- ТУТ ПОДКЛЮЧИЛ обработчик отправки формы -->
  <form @submit.prevent.stop="onCharacterAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
          <input type="text" class="form-control" v-model="characterToAdd.name" required />
          <label for="floatingInput">Имя</label>
        </div>
      </div>
      <div class="col-auto">
        <input type="file" class="form-control" ref="characterPictureRef" @change="charactersAddPictureChange">
      </div>
      <div class="col-auto">
        <img :src="characterAddImageURL" style="max-height: 60px;" alt="">
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
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-12 m-1">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="characterToEdit.name" />
                <label for="floatingInput">Имя</label>
              </div>
            </div>
            <div class="col-auto">
              <input type="file" class="form-control" ref="characterPictureEditRef"
                @change="charactersEditPictureChange">
            </div>
            <div class="col-auto">
              <img :src="characterEditImageURL" style="max-height: 60px;" alt="">
            </div>
            <div class="col-5 m-1">
              <div class="form-floating">
                <select class="form-select" v-model="characterToEdit.race">
                  <option :value="rc.id" v-for="rc in races">
                    {{ rc.name }}
                  </option>
                </select>
                <label for="floatingInput">Расса</label>
              </div>
            </div>
            <div class="col-5 m-1">
              <div class="form-floating">
                <select class="form-select" v-model="characterToEdit.fraction">
                  <option :value="fr.id" v-for="fr in fractions">
                    {{ fr.name }}
                  </option>
                </select>
                <label for="floatingInput">Фракция</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Закрыть
          </button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateCharacter">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>