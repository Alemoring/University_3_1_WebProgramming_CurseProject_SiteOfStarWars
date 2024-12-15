import RaceView from '@/views/RaceView.vue'
import CharacterView from '@/views/CharacterView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import PlanetView from '@/views/PlanetView.vue'
import StarshipView from '@/views/StarshipView.vue'
import FractionView from '../views/FractionView.vue'
import LogInView from '@/views/LogInView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name:'home',
      component: CharacterView
    },
    {
      path:'/race',
      name:'race',
      component: RaceView
    },
    {
      path: '/fraction',
      name: 'fraction',
      component: () => import('../views/FractionView.vue')
    },
    {
      path:'/planet',
      name:'planet',
      component: PlanetView
    },
    {
      path:'/starship',
      name:'starship',
      component: StarshipView
    },
    {
      path:'/admin',
      name:'admin',
      component: RaceView
    },
    {
      path:'/login',
      name:'login',
      component: LogInView
    }
  ]
})

export default router
