<script setup>
import { computed, onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

const planets = ref([])
const planetToAdd = ref({})
const planetToEdit = ref({})

const statistics = ref([])

async function fetchPlanets() {
  const r = await axios.get('/api/planets/')
  planets.value = r.data
  const r2 = await axios.get('/api/planets/stats/')
  statistics.value = r2.data
}

async function onPlanetEditClick(planet) {
  planetToEdit.value = { ...planet };
}

async function onUpdatePlanet() {
  const rt = await axios.get("/api/user/otp-status/")
  const otpStatus = rt.data
  if (otpStatus["otp_good"]) {
    await axios.put(`/api/planets/${planetToEdit.value.id}/`, {
      ...planetToEdit.value,
    });
    await fetchPlanets();
  }
}

async function onPlanetAdd() {
  await axios.post("/api/planets/", {
    "name": planetToAdd.value.name,
    "population": planetToAdd.value.population,
  })
  await fetchPlanets()
}

async function onRemoveClick(planet) {
  await axios.delete(`api/planets/${planet.id}/`)
  await fetchPlanets()
}

async function onLoadClick() {
  await fetchPlanets()
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  await fetchPlanets()
})
</script>

<template>
  <div class="row mt-2 mb-2">
    <div class="col-auto border border-dark">Количество записей: {{ statistics.count }}</div>
    <div class="col-auto border border-dark">Среднее id в записях: {{ statistics.avg }}</div>
    <div class="col-auto border border-dark"> Минимальное id в записях:{{ statistics.min }}</div>
    <div class="col-auto border border-dark"> Максимальное id в записях: {{ statistics.max }}</div>
  </div>
  <div class="row">
    <div v-for="item in planets" class="planet-item card m-2" style="width: 18rem;">
      <div class="card-title ms-4">Название: {{ item.name }}</div>
      <div class="card-text ms-4">Популяция: {{ item.population }}</div>
      <div class="mt-2 mb-2 ms-4 me-4" style="display: flex; justify-content: space-between;">
        <button class="btn btn-success" @click="onPlanetEditClick(item)" data-bs-toggle="modal"
          data-bs-target="#editPlanetModal">
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
  <form @submit.prevent.stop="onPlanetAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
          <input type="text" class="form-control" v-model="planetToAdd.name" required />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
          <input type="number" class="form-control" v-model="planetToAdd.population" required />
          <label for="floatingInput">Популяция</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>

  <div class="modal fade" id="editPlanetModal" tabindex="-1">
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
            <div class="col">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="planetToEdit.name" />
                <label for="floatingInput">Название</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="planetToEdit.population" />
                <label for="floatingInput">Популяция</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Закрыть
          </button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdatePlanet">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
