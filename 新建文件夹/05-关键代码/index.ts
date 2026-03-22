import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/wand',
    name: 'wand',
    component: () => import('@/views/WandView.vue')
  },
  {
    path: '/sorting',
    name: 'sorting',
    component: () => import('@/views/SortingView.vue')
  },
  {
    path: '/spells',
    name: 'spells',
    component: () => import('@/views/SpellsView.vue')
  },
  {
    path: '/characters',
    name: 'characters',
    component: () => import('@/views/CharactersView.vue')
  },
  {
    path: '/puzzles',
    name: 'puzzles',
    component: () => import('@/views/PuzzlesView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
