<script setup>
import axios from "axios"
import { computed, onBeforeMount, ref } from 'vue'
import useUserProfileStore from '@/stores/UserProfileStore'
import { storeToRefs } from "pinia"

const userProfileStore = useUserProfileStore()
const {
  is_authenticated,
  username
} = storeToRefs(userProfileStore)
async function onClick() {
  await axios.post("/accounts/logout/")
  document.location.reload()
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
            <li><a class="dropdown-item" href="/admin">Админка</a></li>
            <li><RouterLink class="dropdown-item" to="/login"> Вход </RouterLink></li>
            <li><button class="dropdown-item" @click="onClick()">Выход</button></li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>
  <div class="m-4">

    <RouterView />
  </div>

</template>

<style scoped></style>