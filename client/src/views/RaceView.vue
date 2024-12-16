<script setup>
import { computed, onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

const races = ref([])
const planets = ref([])
const raceToAdd = ref({})
const raceToEdit = ref({})

const statistics = ref([])

async function fetchRaces() {
  const r1 = await axios.get("/api/races/")
  races.value = r1.data

  const r2 = await axios.get("/api/planets/")
  planets.value = r2.data

  const r3 = await axios.get("/api/races/stats/")
  statistics.value = r3.data
}

async function onRaceEditClick(race) {
  raceToEdit.value = { ...race };
}

async function onUpdateRace() {
  const rt = await axios.get("/api/user/otp-status/")
  const otpStatus = rt.data
  if (otpStatus["otp_good"]) {
    await axios.put(`/api/races/${raceToEdit.value.id}/`, {
      ...raceToEdit.value,
    });
    await fetchRaces();
  }
}

async function onRaceAdd() {
  await axios.post("/api/races/", {
    "name": raceToAdd.value.name,
    "homePlanet": raceToAdd.value.homePlanet
  })
  await fetchRaces()
}

async function onRemoveClick(race) {
  await axios.delete(`api/races/${race.id}/`)
  await fetchRaces()
}

async function onLoadClick() {
  await fetchRaces()
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  await fetchRaces()
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
    <div v-for="item in races" class="race-item card" style="width: 18rem;">
      <div class="card-title ms-4">Название: {{ item.name }}</div>
      <div class="card-text ms-4">Родная планета: {{ item.homePlanet.name }}</div>
      <div class="mt-2 mb-2 ms-4 me-4" style="display: flex; justify-content: space-between;">
        <button class="btn btn-success" @click="onRaceEditClick(item)" data-bs-toggle="modal"
          data-bs-target="#editRaceModal">
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
  <form @submit.prevent.stop="onRaceAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
          <input type="text" class="form-control" v-model="raceToAdd.name" required />
          <label for="floatingInput">Имя</label>
        </div>
      </div>
      <div class="col-auto">
        <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
        <div class="form-floating">
          <select class="form-select" v-model="raceToAdd.homePlanet" required>
            <option :value="pln.id" v-for="pln in planets">{{ pln.name }}</option>
          </select>
          <label for="floatingInput">Родная планета</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>

  <div class="modal fade" id="editRaceModal" tabindex="-1">
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
                <input type="text" class="form-control" v-model="raceToEdit.name" />
                <label for="floatingInput">Имя</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="raceToEdit.homePlanet">
                  <option :value="pln.id" v-for="pln in planets">
                    {{ pln.name }}
                  </option>
                </select>
                <label for="floatingInput">Родная планета</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Закрыть
          </button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateRace">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style></style>
