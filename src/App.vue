<template>
  <div id="app" class="relative min-h-screen text-white overflow-hidden"
       style="background: linear-gradient(180deg, #0a0a0a 0%, #151515 50%, #1a1a1a 100%);">
    <!-- 背景粒子效果 -->
    <div class="fixed inset-0 pointer-events-none overflow-hidden z-0">
      <div v-for="i in 15" :key="i" class="particle" :style="getParticleStyle(i)"></div>
    </div>

    <t-layout class="relative z-10">
      <!-- 侧边栏 -->
      <t-aside class="w-72 border-r-2 border-hp-gold/30 backdrop-blur-xl"
               style="background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);">
        <div class="p-8 border-b border-hp-gold/10">
          <div class="flex items-center gap-3 mb-3">
            <div class="text-4xl magic-sparkle">🏰</div>
            <div>
              <h1 class="text-2xl font-bold text-hp-gold glow-text">魔法工坊</h1>
              <p class="text-xs text-gray-400 tracking-widest uppercase">Magic Workshop</p>
            </div>
          </div>
          <div class="mt-4 h-0.5 bg-gradient-to-r from-hp-gold/50 via-hp-gold to-hp-gold/50 rounded-full"></div>
        </div>

        <t-menu v-model="activeMenu" theme="dark" class="border-none bg-transparent p-4">
          <div v-for="item in menuItems" :key="item.value">
            <t-menu-item
              :value="item.value"
              @click="navigateTo(item.value)"
              class="mb-2 rounded-xl transition-all duration-300 hover:bg-hp-gold/15 border-2 border-transparent"
            >
              <template #icon>
                <div class="text-2xl magic-float" :style="{ animationDelay: item.delay }">{{ item.icon }}</div>
              </template>
              <span class="font-medium">{{ item.label }}</span>
            </t-menu-item>
          </div>
        </t-menu>

        <!-- 底部用户信息 -->
        <div class="absolute bottom-0 left-0 right-0 p-6 border-t-2 border-hp-gold/30"
             style="background: linear-gradient(180deg, transparent 0%, rgba(10, 10, 10, 0.8) 100%);">
          <div v-if="userStore.house" class="flex items-center gap-3">
            <div :class="getHouseBackground()" class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shadow-lg">
              {{ getHouseIcon() }}
            </div>
            <div>
              <p class="text-sm text-gray-400">当前学院</p>
              <p class="text-lg font-bold text-hp-gold">{{ userStore.house }}</p>
            </div>
          </div>
          <div v-else class="text-center">
            <p class="text-sm text-gray-400">尚未分院</p>
            <button @click="navigateTo('sorting')" class="text-xs text-hp-gold hover:underline mt-1">
              开始分院测试 →
            </button>
          </div>
        </div>
      </t-aside>

      <!-- 主内容区 -->
      <t-layout>
        <!-- 顶部导航 -->
        <t-header class="border-b-2 border-hp-gold/30 px-8 py-4 flex items-center justify-between backdrop-blur-xl"
                  style="background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);">
          <div class="flex items-center gap-4">
            <div class="w-1 h-8 bg-gradient-to-b from-hp-gold to-transparent rounded-full"></div>
            <h2 class="text-2xl font-bold text-hp-gold glow-text">{{ currentPageTitle }}</h2>
          </div>
          <div class="flex items-center gap-6">
            <div v-if="userStore.wand" class="flex items-center gap-3 px-4 py-2 rounded-xl border-2 border-hp-gold/20"
               style="background: rgba(10, 10, 10, 0.8);">
              <span class="text-xl">🪄</span>
              <div class="text-left">
                <p class="text-xs text-gray-400">专属魔杖</p>
                <p class="text-sm text-hp-gold">{{ userStore.wand.wood }} · {{ userStore.wand.length }}"</p>
              </div>
            </div>
            <t-avatar size="medium" class="ring-2 ring-hp-gold/50 ring-offset-2 ring-offset-black">
              <div class="w-full h-full bg-gradient-to-br from-hp-gold to-hp-purple flex items-center justify-center text-xl">
                🧙
              </div>
            </t-avatar>
          </div>
        </t-header>

        <!-- 内容区域 -->
        <t-content class="p-8"
                  style="background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);">
          <div class="max-w-7xl mx-auto">
            <router-view />
          </div>
        </t-content>
      </t-layout>
    </t-layout>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const activeMenu = ref('home')

const menuItems = [
  { value: 'home', icon: '🏠', label: '首页', delay: '0s' },
  { value: 'wand', icon: '🪄', label: '魔杖定制', delay: '0.2s' },
  { value: 'sorting', icon: '🎩', label: '分院测试', delay: '0.4s' },
  { value: 'spells', icon: '⚡', label: '咒语学习', delay: '0.6s' },
  { value: 'characters', icon: '🧙', label: '角色互动', delay: '0.8s' },
  { value: 'puzzles', icon: '🧩', label: '谜题闯关', delay: '1s' }
]

const currentPageTitle = computed(() => {
  const titles: Record<string, string> = {
    home: '欢迎来到魔法工坊',
    wand: '魔杖个性定制',
    sorting: '霍格沃茨分院测试',
    spells: '魔法咒语学习',
    characters: '角色互动对话',
    puzzles: '谜题闯关游戏'
  }
  return titles[route.name as string] || '魔法工坊'
})

const navigateTo = (page: string) => {
  activeMenu.value = page
  router.push({ name: page })
}

const getParticleStyle = (index: number) => {
  return {
    left: `${Math.random() * 100}%`,
    animationDelay: `${Math.random() * 8}s`,
    animationDuration: `${8 + Math.random() * 4}s`
  }
}

const getHouseBackground = () => {
  const backgrounds: Record<string, string> = {
    '格兰芬多': 'bg-gradient-to-br from-red-700 to-red-900',
    '斯莱特林': 'bg-gradient-to-br from-emerald-700 to-emerald-900',
    '拉文克劳': 'bg-gradient-to-br from-blue-600 to-blue-900',
    '赫奇帕奇': 'bg-gradient-to-br from-yellow-600 to-yellow-800'
  }
  return backgrounds[userStore.house] || 'bg-gradient-to-br from-gray-600 to-gray-800'
}

const getHouseIcon = () => {
  const icons: Record<string, string> = {
    '格兰芬多': '🦁',
    '斯莱特林': '🐍',
    '拉文克劳': '🦅',
    '赫奇帕奇': '🦡'
  }
  return icons[userStore.house] || '⭐'
}
</script>

<style scoped>
:deep(.t-layout) {
  height: 100vh;
}

:deep(.t-layout__sider) {
  overflow-y: auto;
  background: transparent !important;
}

:deep(.t-menu) {
  background: transparent !important;
}

:deep(.t-menu__item) {
  border-radius: 0.75rem;
  margin: 0.5rem 0;
  transition: all 0.3s ease;
}

:deep(.t-menu__item.t-is-active) {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(46, 26, 71, 0.2)) !important;
  border-color: #D4AF37 !important;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.25);
}

:deep(.t-menu__item:hover) {
  background: rgba(212, 175, 55, 0.12) !important;
  border-color: rgba(212, 175, 55, 0.4);
  transform: translateX(4px);
}

:deep(.t-layout__header) {
  background: transparent !important;
}

:deep(.t-layout__content) {
  background: transparent !important;
  overflow-y: auto;
}
</style>
