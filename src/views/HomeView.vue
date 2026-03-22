<template>
  <div class="home-view">
    <!-- 欢迎横幅 -->
    <div class="text-center mb-16 relative">
      <div class="absolute -top-20 left-1/2 -translate-x-1/2 text-9xl opacity-20 magic-sparkle">✨</div>
      <h1 class="text-6xl font-bold text-hp-gold mb-6 glow-text relative z-10">
        欢迎来到魔法工坊
      </h1>
      <p class="text-xl text-gray-300 mb-4 max-w-2xl mx-auto leading-relaxed">
        探索哈利波特的魔法世界，体验AI驱动的沉浸式互动
      </p>
      <div class="flex justify-center gap-2 mt-6">
        <span class="px-4 py-2 rounded-full glass-card text-sm text-hp-gold border border-hp-gold/30">
          ⚡ AI驱动
        </span>
        <span class="px-4 py-2 rounded-full glass-card text-sm text-hp-gold border border-hp-gold/30">
          🎮 互动体验
        </span>
        <span class="px-4 py-2 rounded-full glass-card text-sm text-hp-gold border border-hp-gold/30">
          🌟 沉浸式
        </span>
      </div>
    </div>

    <!-- 功能卡片网格 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
      <div
        v-for="feature in features"
        :key="feature.id"
        class="magic-card rounded-2xl p-8 cursor-pointer border-2 border-hp-gold/30 hover:border-hp-gold/70 hover:shadow-2xl hover:shadow-hp-gold/20 relative overflow-hidden group"
        style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);"
        @click="navigateTo(feature.id)"
      >
        <!-- 装饰性金色边框 -->
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-60"></div>
        <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-60"></div>

        <!-- 悬停时的金色光晕 -->
        <div class="absolute inset-0 bg-gradient-to-br from-hp-gold/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

        <div class="relative z-10">
          <div class="text-6xl mb-6 magic-float">{{ feature.icon }}</div>
          <h3 class="text-2xl font-bold text-hp-gold mb-3">{{ feature.title }}</h3>
          <p class="text-gray-300 leading-relaxed">{{ feature.description }}</p>
          <div class="mt-6 flex items-center text-hp-gold group-hover:text-hp-gold transition-colors">
            <span class="text-sm font-medium">开始体验</span>
            <svg class="w-4 h-4 ml-2 transform group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 魔法统计 -->
    <div class="rounded-2xl p-10 mb-16 border-2 border-hp-gold/30 relative overflow-hidden"
         style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
      <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-80"></div>
      <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-60"></div>

      <div class="relative z-10">
        <h2 class="text-3xl font-bold text-hp-gold mb-8 text-center glow-text">魔法统计</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div v-for="stat in statsDisplay" :key="stat.label" class="text-center group">
            <div class="relative inline-block">
              <div class="text-5xl font-bold text-hp-gold mb-3 magic-sparkle">{{ stat.value }}</div>
              <div class="absolute -inset-4 bg-hp-gold/10 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            </div>
            <div class="text-gray-300 text-sm uppercase tracking-wider">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 用户状态卡片 -->
    <div v-if="userStore.house" class="rounded-2xl p-8 border-2 border-hp-gold/40 relative overflow-hidden magic-glow"
         style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
      <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-80"></div>
      <div class="absolute inset-0 bg-gradient-to-br from-hp-gold/5 to-transparent"></div>
      <div class="relative z-10">
        <div class="flex items-start gap-6">
          <div class="w-20 h-20 rounded-2xl flex items-center justify-center text-4xl shadow-2xl border-2 border-hp-gold/30"
               :class="getHouseBackgroundClass()">
            {{ getHouseIcon() }}
          </div>
          <div class="flex-1">
            <h3 class="text-2xl font-bold text-hp-gold mb-3">
              🎉 恭喜你成为 {{ userStore.house }} 的学员！
            </h3>
            <p class="text-gray-300 mb-4 leading-relaxed">
              你的魔法之旅已经开始，继续探索各个模块，解锁更多魔法能力吧！
            </p>
            <div v-if="userStore.wand" class="mt-6 p-4 rounded-xl bg-black/60 border-2 border-hp-gold/20">
              <p class="text-sm text-gray-400 mb-2">你的专属魔杖</p>
              <div class="flex items-center gap-4">
                <span class="text-3xl">🪄</span>
                <div>
                  <p class="text-lg text-hp-gold font-semibold">
                    {{ userStore.wand.wood }}木材 · {{ userStore.wand.core }}杖芯
                  </p>
                  <p class="text-sm text-gray-400">长度: {{ userStore.wand.length }} 英寸</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态提示 -->
    <div v-else class="rounded-2xl p-12 text-center border-2 border-hp-gold/30 hover:border-hp-gold/60 transition-colors duration-300"
         style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
      <div class="text-6xl mb-6 magic-float">🎩</div>
      <h3 class="text-2xl font-bold text-hp-gold mb-4">开始你的魔法之旅</h3>
      <p class="text-gray-300 mb-6 max-w-md mx-auto">
        还没有找到你的学院？立即进行分院测试，开启属于你的魔法冒险！
      </p>
      <button
        @click="navigateTo('sorting')"
        class="magic-btn px-8 py-4 bg-gradient-to-r from-hp-gold to-yellow-600 text-black font-bold rounded-xl hover:shadow-2xl hover:shadow-hp-gold/30 transition-all duration-300"
      >
        开始分院测试
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const features = [
  {
    id: 'wand',
    icon: '🪄',
    title: '魔杖定制',
    description: '通过AI分析你的性格，生成专属魔杖外观与属性，每一根都独一无二'
  },
  {
    id: 'sorting',
    icon: '🎩',
    title: '分院测试',
    description: '与分院帽对话，回答问题，找到你在霍格沃茨的真正归属'
  },
  {
    id: 'spells',
    icon: '⚡',
    title: '咒语学习',
    description: '练习发音，掌握经典魔法咒语，感受挥舞魔杖的力量'
  },
  {
    id: 'characters',
    icon: '🧙',
    title: '角色互动',
    description: '与邓布利多、斯内普等角色深入对话，探索他们的内心世界'
  },
  {
    id: 'puzzles',
    icon: '🧩',
    title: '谜题闯关',
    description: '挑战经典谜题，测试你的魔法智慧，解锁隐藏的秘密'
  },
  {
    id: 'explore',
    icon: '📚',
    title: '探索更多',
    description: '持续更新中，更多魔法功能即将呈现，敬请期待...'
  }
]

const stats = ref({
  users: 1247,
  wands: 892,
  spells: 3421,
  dialogues: 5678
})

const statsDisplay = computed(() => [
  { label: '魔法学员', value: stats.value.users.toLocaleString() },
  { label: '定制魔杖', value: stats.value.wands.toLocaleString() },
  { label: '学习咒语', value: stats.value.spells.toLocaleString() },
  { label: '角色对话', value: stats.value.dialogues.toLocaleString() }
])

const navigateTo = (page: string) => {
  router.push({ name: page })
}

const getHouseBackgroundClass = () => {
  const backgrounds: Record<string, string> = {
    '格兰芬多': 'bg-gradient-to-br from-red-600 to-red-800',
    '斯莱特林': 'bg-gradient-to-br from-emerald-600 to-emerald-800',
    '拉文克劳': 'bg-gradient-to-br from-blue-500 to-blue-800',
    '赫奇帕奇': 'bg-gradient-to-br from-yellow-500 to-yellow-700'
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
.home-view {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.magic-card:hover {
  transform: translateY(-12px) scale(1.02);
}
</style>
