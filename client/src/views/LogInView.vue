<script setup>
import { computed, onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'
import {storeToRefs} from "pinia"
import useUserProfileStore from '@/stores/UserProfileStore'

const user = ref()
const password = ref()

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Если cookie начинается с нужного имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//var csrftoken = getCookie('csrftoken')
async function onLogIn() {
    var csrftoken = getCookie('csrftoken')
    console.log(csrftoken)
    console.log(user.value)
    console.log(password.value)
    const formData = new FormData()
    formData.set('username', user.value)
    formData.set("password", password.value)
    const response = await axios.post('/accounts/login/', formData, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    console.log(response.data)
    document.location.reload()
}
</script>
<template>
    <form @submit.prevent.stop="onLogIn">
        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="user" required />
                    <label for="">Имя</label>
                </div>
            </div>
            <div class="form-floating">
                <input type="password" class="form-control" v-model="password" required />
                <label for="">Пароль</label>
            </div>
            <div class="col-auto">
                <button class="btn btn-primary">
                    Войти
                </button>
            </div>
        </div>
    </form>
</template>
