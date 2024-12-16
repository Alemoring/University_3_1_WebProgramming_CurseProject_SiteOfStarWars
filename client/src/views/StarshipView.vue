<script setup>
import { computed, onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'
import { storeToRefs } from "pinia"
import useUserProfileStore from '@/stores/UserProfileStore'

const userFilter = ref()

const starships = ref([])
const starshipToAdd = ref({})
const starshipToEdit = ref({})
const starshipPictureRef = ref()
const starshipPictureEditRef = ref()
const starshipAddImageURL = ref()
const starshipEditImageURL = ref()

const statistics = ref([])

const users = ref([])

const userProfileStore = useUserProfileStore()
const {
  is_authenticated,
  is_superuser,
  username
} = storeToRefs(userProfileStore)

async function fetchStarships(user) {
  var r
  if (user != null) {
    r = await axios.get("/api/starships/?username=" + user)
  } else {
    r = await axios.get("/api/starships/")
  }
  starships.value = r.data
  const r2 = await axios.get("/api/starships/stats/")
  statistics.value = r2.data
  const r3 = await axios.get("/api/users/")
  users.value = r3.data
}

async function onFilterUser(user) {
  await fetchStarships()
  if (user != -1) {
    await fetchStarships(user + 1)
  }
}

async function starshipsAddPictureChange() {
  if (starshipPictureRef.value.files[0] != null) {
    starshipAddImageURL.value = URL.createObjectURL(starshipPictureRef.value.files[0])
  } else {
    starshipAddImageURL.value = null
  }
}
async function starshipsEditPictureChange() {
  if (starshipPictureEditRef.value.files[0] != null) {
    starshipEditImageURL.value = URL.createObjectURL(starshipPictureEditRef.value.files[0])
  } else {
    starshipEditImageURL.value = null
  }
  starshipToEdit.value.picture = null
}

async function onStarshipEditClick(starship) {
  starshipToEdit.value = { ...starship };
  starshipEditImageURL.value = starshipToEdit.value.picture
}

async function onUpdateStarship() {
  const rt = await axios.get("/api/user/otp-status/")
  const otpStatus = rt.data
  if (otpStatus["otp_good"]) {
    const formData = new FormData()
    if (starshipPictureEditRef.value.files[0] != null) {
      formData.append('picture', starshipPictureEditRef.value.files[0])

      formData.set('name', starshipToEdit.value.name)
      formData.set("type", starshipToEdit.value.type)
      formData.set("crew", starshipToEdit.value.crew)

      await axios.put(`/api/starships/${starshipToEdit.value.id}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    } else if (starshipToEdit.value.picture != null) {
      await axios.put(`/api/starships/${starshipToEdit.value.id}/`, {
        'name': starshipToEdit.value.name,
        "type": starshipToEdit.value.type,
        "crew": starshipToEdit.value.crew
      });
    }
    else {
      await axios.put(`/api/starships/${starshipToEdit.value.id}/`, {
        'name': starshipToEdit.value.name,
        "type": starshipToEdit.value.type,
        "crew": starshipToEdit.value.crew,
        "picture": null
      });
    }
    starshipPictureEditRef.value = null
    await fetchStarships();
  }
}

async function onStarshipAdd() {
  const formData = new FormData()
  console.log(starshipPictureRef.value.files[0])
  formData.set('name', starshipToAdd.value.name)
  formData.set("type", starshipToAdd.value.type)
  formData.set("crew", starshipToAdd.value.crew)
  if (starshipPictureRef.value.files[0] != null) {
    formData.append('picture', starshipPictureRef.value.files[0])
    console.log("OK")
    await axios.post("/api/starships/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    starshipPictureRef.value = null
  } else {
    await axios.post("/api/starships/", {
      'name': starshipToAdd.value.name,
      "type": starshipToAdd.value.type,
      "crew": starshipToAdd.value.crew,
      "picture": null
    })
  }
  await fetchStarships()
}

async function onRemoveClick(starship) {
  await axios.delete(`api/starships/${starship.id}/`)
  await fetchStarships()
}

async function onLoadClick() {
  await fetchStarships()
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  await fetchStarships()
})
</script>

<template>
  <div class="row">
    <div class="col-auto ">
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
  <div class="row mt-2 mb-2">
    <div class="col-auto border border-dark">Количество записей: {{ statistics.count }}</div>
    <div class="col-auto border border-dark">Среднее id в записях: {{ statistics.avg }}</div>
    <div class="col-auto border border-dark"> Минимальное id в записях:{{ statistics.min }}</div>
    <div class="col-auto border border-dark"> Максимальное id в записях: {{ statistics.max }}</div>
  </div>
  <div class="row">
    <div v-for="item in starships" class="starship-item card m-2" style="width: 18rem;">
      <div v-show="item.picture" class="mt-3 mb-2" style="margin-left: auto; margin-right: auto;"><img
          :src="item.picture"
          style="max-height: 200px; width: 16rem; border: 2px solid black; box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.4);"
          alt=""></div>
      <div class="card-title ms-4">Название: {{ item.name }}</div>
      <div class="card-text ms-4">Тип: {{ item.type }}</div>
      <div class="card-text ms-4">Команда: {{ item.crew }}</div>
      <div v-if="userProfileStore.is_superuser" class="card-text ms-4">Юзер: {{ users[item.user - 1].username }}</div>
      <div class="mt-2 mb-2 ms-4 me-4" style="display: flex; justify-content: space-between;">
        <button class="btn btn-success btn" @click="onStarshipEditClick(item)" data-bs-toggle="modal"
          data-bs-target="#editStarshipModal">
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
  <form @submit.prevent.stop="onStarshipAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
          <input type="text" class="form-control" v-model="starshipToAdd.name" required />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col-auto">
        <input type="file" class="form-control" ref="starshipPictureRef" @change="starshipsAddPictureChange">
      </div>
      <div class="col-auto">
        <img :src="starshipAddImageURL" style="max-height: 60px;" alt="">
      </div>
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
          <input type="text" class="form-control" v-model="starshipToAdd.type" required />
          <label for="floatingInput">Тип</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
          <input type="text" class="form-control" v-model="starshipToAdd.crew" required />
          <label for="floatingInput">Команда</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>

  <div class="modal fade" id="editStarshipModal" tabindex="-1">
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
                <input type="text" class="form-control" v-model="starshipToEdit.name" />
                <label for="floatingInput">Название</label>
              </div>
            </div>
            <div class="col-auto">
              <input type="file" class="form-control" ref="starshipPictureEditRef" @change="starshipsEditPictureChange">
            </div>
            <div class="col-auto">
              <img :src="starshipEditImageURL" style="max-height: 60px;" alt="">
            </div>
            <div class="col-12 m-1">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="starshipToEdit.type" />
                <label for="floatingInput">Тип</label>
              </div>
            </div>
            <div class="col-12 m-1">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="starshipToEdit.crew" />
                <label for="floatingInput">Команда</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Закрыть
          </button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateStarship">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
