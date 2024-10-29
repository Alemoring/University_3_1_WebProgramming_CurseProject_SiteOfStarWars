<script setup>
import { ref } from 'vue'
import axios from "axios"

const list  = ref([4,3,2,5,1,2])

async function onLoadClick() {
  axios.get("/api/characters/")
}
</script>

<template>
  <div>
    <div v-for="item in list">
      <div>{{ item }}</div>
    </div>

    <button @click="onLoadClick()">Загрузить</button>
  </div>

</template>

<style scoped></style>