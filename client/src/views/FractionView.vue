<script setup>
import { computed, onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

const fractions = ref([])
const fractionToAdd = ref({})
const fractionToEdit = ref({})

async function fetchFractions() {
  const r = await axios.get('/api/fractions/')
  fractions.value = r.data
}

async function onFractionEditClick(fraction) {
  fractionToEdit.value = { ...fraction };
}

async function onUpdateFraction() {
  await axios.put(`/api/fractions/${fractionToEdit.value.id}/`, {
    ...fractionToEdit.value,
  });
  await fetchFractions();
}

async function onFractionAdd() {
  await axios.post("/api/fractions/", {
    "name": fractionToAdd.value.name,
    "periodInLive": fractionToAdd.value.periodInLive,
  })
  await fetchFractions()
}

async function onRemoveClick(fraction) {
  await axios.delete(`api/fractions/${fraction.id}/`)
  await fetchFractions()
}

async function onLoadClick() {
  await fetchFractions()
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  await fetchFractions()
})
</script>

<template>
  <div class="row">
    <div v-for="item in fractions" class="fraction-item card m-2" style="width: 18rem;">
      <div class="card-title ms-4">Название: {{ item.name }}</div>
      <div class="card-text ms-4">Период существования: {{ item.periodInLive }}</div>
      <div class="mt-2 mb-2 ms-4" style="display: flex; justify-content: space-between;">
        <button class="btn btn-success" @click="onFractionEditClick(item)" data-bs-toggle="modal"
          data-bs-target="#editFractionModal">
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
  <form @submit.prevent.stop="onFractionAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
          <input type="text" class="form-control" v-model="fractionToAdd.name" required />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ characterToAdd.name -->
          <input type="text" class="form-control" v-model="fractionToAdd.periodInLive" required />
          <label for="floatingInput">Период существования</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>

  <div class="modal fade" id="editFractionModal" tabindex="-1">
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
                <input type="text" class="form-control" v-model="fractionToEdit.name" />
                <label for="floatingInput">Название</label>
              </div>
            </div>
            <div class="col">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="fractionToEdit.periodInLive" />
                <label for="floatingInput">Период существования</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Закрыть
          </button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateFraction">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>