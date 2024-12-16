<script setup>
import axios from "axios"
import { computed, onBeforeMount, ref } from 'vue'
import useUserProfileStore from '@/stores/UserProfileStore'
import { storeToRefs } from "pinia"

const userProfileStore = useUserProfileStore()
const OTPKey = ref()
const {
  is_authenticated,
  username
} = storeToRefs(userProfileStore)
async function onClick() {
  //await axios.post("/accounts/logout/")
  await axios.get("/api/user/logout/")
  document.location.reload()
}
function onOTPLogin(){
  axios.get("/api/user/otp-login/")
}
function onOTPLoginAfter(){
  axios.post("/api/user/otp-login/", {
    "key" : OTPKey.value
  })
}
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
      <a class="navbar-brand ms-4" href="/">Главная</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Переключатель навигации">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/"> Персонажи </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/race"> Рассы </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/fraction"> Фракции </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/planet"> Планеты </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/starship"> Звёздные корабли </RouterLink>
          </li>
        </ul>
      </div>
      <ul class="navbar-nav me-4">
        <li>
          <div class="nav-link">{{ userProfileStore.username }}</div>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Пользователь</a>
          <ul class="dropdown-menu">
            <li><button class="dropdown-item" @click="onOTPLogin()" data-bs-toggle="modal"
                data-bs-target="#onOTPLoginModal">
                Пройти двойную аутентификацию
              </button></li>
            <li><a class="dropdown-item" href="/admin">Админка</a></li>
            <li>
              <RouterLink class="dropdown-item" to="/login"> Вход </RouterLink>
            </li>
            <li><button class="dropdown-item" @click="onClick()">Выход</button></li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>
  <div class="m-4">

    <RouterView />
  </div>
  <div class="modal fade" id="onOTPLoginModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            Ключ
          </h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-12 m-1">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="OTPKey" />
                <label for="floatingInput">Введите ключ</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Закрыть
          </button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onOTPLoginAfter">
            Отправить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>