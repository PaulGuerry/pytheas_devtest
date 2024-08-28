import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import "@fontsource/koho/200.css"
import "@fontsource/koho/300.css"
import "@fontsource/koho/400.css"
import "@fontsource/koho/500.css"
import "@fontsource/koho/600.css"
import "@fontsource/koho/700.css"

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
