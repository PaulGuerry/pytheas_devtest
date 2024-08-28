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
  },
  {
    path: '/PFIC1',
    name: 'PFIC1',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC1View.vue')
  },
  {
    path: '/PFIC2',
    name: 'PFIC2',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC2View.vue')
  },
  {
    path: '/PFIC3',
    name: 'PFIC3',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC3View.vue')
  },
  {
    path: '/PFIC4',
    name: 'PFIC4',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC4View.vue')
  },
  {
    path: '/PFIC5',
    name: 'PFIC5',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC5View.vue')
  },
  {
    path: '/PFIC6',
    name: 'PFIC6',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC6View.vue')
  },
  {
    path: '/PFIC7',
    name: 'PFIC7',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC7View.vue')
  },
  {
    path: '/PFIC8',
    name: 'PFIC8',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC8View.vue')
  },
  {
    path: '/PFIC9',
    name: 'PFIC9',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC9View.vue')
  },
  {
    path: '/PFIC10',
    name: 'PFIC10',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC10View.vue')
  },
  {
    path: '/PFIC11',
    name: 'PFIC11',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PFIC11View.vue')
  },
  {
    path: '/THES1',
    name: 'THES1',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/THES1View.vue')
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
