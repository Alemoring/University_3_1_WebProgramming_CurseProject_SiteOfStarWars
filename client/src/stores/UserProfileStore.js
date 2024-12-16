import {defineStore} from "pinia"
import { ref, onBeforeMount } from 'vue'
import axios from "axios"
const useUserProfileStore = defineStore("UserProfileStore", () => {
	const is_authenticated = ref()
	const username = ref()
	const is_superuser = ref()

	onBeforeMount(async () => {
		const r = await axios.get("api/user/check-login/")
		is_authenticated.value = r.data.is_authenticated
		username.value = r.data.name
		is_superuser.value = r.data.is_superuser
	})

	return {is_authenticated, username, is_superuser}
})
export default useUserProfileStore