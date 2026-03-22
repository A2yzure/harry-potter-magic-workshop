<template>
  <div class="wand-view">
    <div class="max-w-5xl mx-auto">
      <!-- 标题区 -->
      <div class="text-center mb-12 relative">
        <div class="absolute -top-16 left-1/2 -translate-x-1/2 text-8xl opacity-20 magic-sparkle">🪄</div>
        <h2 class="text-5xl font-bold text-hp-gold mb-4 glow-text relative z-10">魔杖个性定制</h2>
        <p class="text-lg text-gray-400 max-w-xl mx-auto">
          回答几个问题，AI将根据你的性格为你生成专属魔杖
        </p>
      </div>

      <!-- 步骤1: 问答 -->
      <div v-if="step === 1" class="rounded-2xl p-10 border-2 border-hp-gold/30 relative overflow-hidden"
           style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-80"></div>
        <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-60"></div>

        <div v-if="currentQuestion < questions.length" class="relative z-10">
          <!-- 进度条 -->
          <div class="mb-8">
            <div class="flex items-center justify-between mb-4">
              <span class="text-hp-gold font-bold text-lg">
                <span class="bg-hp-gold/20 px-3 py-1 rounded-full text-sm">问题 {{ currentQuestion + 1 }}</span>
                <span class="text-gray-500 mx-2">/</span>
                <span class="text-gray-300">{{ questions.length }}</span>
              </span>
              <div class="w-64 h-2 bg-gray-800 rounded-full overflow-hidden border border-gray-700">
                <div
                  class="h-full bg-gradient-to-r from-hp-gold to-yellow-600 transition-all duration-500"
                  :style="{ width: ((currentQuestion + 1) / questions.length) * 100 + '%' }"
                ></div>
              </div>
            </div>
          </div>

          <!-- 问题 -->
          <h3 class="text-2xl font-semibold text-white mb-8 leading-relaxed">
            {{ questions[currentQuestion].question }}
          </h3>

          <!-- 选项 -->
          <div class="space-y-4">
            <button
              v-for="(option, idx) in questions[currentQuestion].options"
              :key="idx"
              @click="selectOption(idx)"
              class="magic-btn w-full p-5 text-left bg-black/60 border-2 border-hp-gold/30 rounded-xl hover:border-hp-gold hover:bg-hp-gold/15 transition-all duration-300 group relative overflow-hidden"
            >
              <div class="flex items-center gap-4">
                <div class="w-8 h-8 rounded-lg border-2 border-hp-gold/40 flex items-center justify-center text-hp-gold text-sm group-hover:bg-hp-gold/30 transition-colors">
                  {{ idx + 1 }}
                </div>
                <span class="text-gray-200 group-hover:text-white transition-colors">{{ option }}</span>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- 步骤2: 生成中 -->
      <div v-if="step === 2" class="text-center py-20 rounded-2xl border-2 border-hp-gold/40 relative overflow-hidden"
           style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-80"></div>
        <div class="absolute inset-0 bg-gradient-to-br from-hp-gold/5 to-transparent"></div>
        <div class="relative z-10">
          <div class="text-9xl mb-8 magic-sparkle">🪄</div>
          <h3 class="text-3xl text-hp-gold font-bold mb-4 glow-text">正在锻造你的魔杖...</h3>
          <p class="text-gray-300 mb-8 max-w-md mx-auto">
            奥利凡德正在根据你的答案选择最合适的材料，请稍候...
          </p>
          <div class="flex justify-center">
            <t-loading size="large" />
          </div>
        </div>
      </div>

      <!-- 步骤3: 结果 -->
      <div v-if="step === 3 && wandResult" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 魔杖详情 -->
        <div class="rounded-2xl p-10 border-2 border-hp-gold/40 relative overflow-hidden magic-glow"
             style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
          <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-80"></div>
          <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-60"></div>

          <div class="text-center mb-8">
            <div class="text-9xl mb-6 magic-float">🪄</div>
            <h3 class="text-3xl text-hp-gold font-bold glow-text">你的专属魔杖</h3>
            <p class="text-gray-300 mt-2">独一无二，为你而生</p>
          </div>

          <div class="space-y-6 mb-8">
            <div v-for="attr in wandAttributes" :key="attr.label" class="flex justify-between items-center p-4 rounded-xl bg-black/60 border-2 border-hp-gold/20">
              <span class="text-gray-300">{{ attr.label }}</span>
              <span class="text-hp-gold font-bold text-lg">{{ attr.value }}</span>
            </div>
          </div>

          <div class="p-6 rounded-xl bg-black/60 border-2 border-hp-gold/20 mb-8">
            <h4 class="text-hp-gold font-bold mb-3">✨ 特性描述</h4>
            <p class="text-gray-300 leading-relaxed">{{ wandResult.description }}</p>
          </div>

          <button
            @click="saveWand"
            class="magic-btn w-full px-8 py-4 bg-gradient-to-r from-hp-gold to-yellow-600 text-black font-bold rounded-xl hover:shadow-2xl hover:shadow-hp-gold/30 transition-all duration-300 text-lg"
          >
            保存我的魔杖
          </button>
        </div>

        <!-- 预览与操作 -->
        <div class="space-y-6">
          <div class="rounded-2xl p-8 border-2 border-hp-gold/30"
               style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
            <h3 class="text-xl text-hp-gold mb-6 font-semibold">魔杖预览</h3>
            <div class="aspect-square bg-black/60 rounded-xl flex items-center justify-center mb-6 relative overflow-hidden group border-2 border-hp-gold/20">
              <div class="absolute inset-0 bg-gradient-to-br from-hp-gold/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div class="text-center relative z-10">
                <div class="text-8xl mb-4 magic-float">🪄</div>
                <p class="text-gray-300 text-sm">AI 生成的魔杖图像</p>
                <p class="text-gray-400 text-xs mt-2">(演示版本使用占位符)</p>
              </div>
            </div>
            <div class="space-y-3">
              <t-button theme="default" variant="outline" block size="large">
                📥 下载图片
              </t-button>
            </div>
          </div>

          <div class="rounded-2xl p-6 border-2 border-hp-gold/30"
               style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
            <h3 class="text-lg text-hp-gold mb-4 font-semibold">更多操作</h3>
            <div class="space-y-3">
              <t-button theme="default" variant="dashed" block @click="reset">
                🔄 重新定制
              </t-button>
              <t-button theme="default" variant="dashed" block>
                📤 分享给朋友
              </t-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const userStore = useUserStore()

const step = ref(1)
const currentQuestion = ref(0)
const answers = ref<number[]>([])
const wandResult = ref<any>(null)

const questions = [
  {
    question: '你最看重魔杖的什么品质？',
    options: ['力量与掌控', '智慧与创造力', '忠诚与勇气', '优雅与精致']
  },
  {
    question: '面对困难时，你通常会？',
    options: ['直接面对，积极解决', '思考策略，谨慎行动', '寻求朋友的帮助', '相信直觉，顺其自然']
  },
  {
    question: '你认为最重要的魔法特质是什么？',
    options: ['意志坚定', '聪明才智', '勇敢无畏', '真诚善良']
  },
  {
    question: '你更喜欢哪种魔法风格？',
    options: ['强大的攻击魔法', '精妙的变形术', '实用的防护咒', '神秘的预言魔法']
  },
  {
    question: '如果在霍格沃茨，你最想加入哪个学院？',
    options: ['斯莱特林', '拉文克劳', '格兰芬多', '赫奇帕奇']
  }
]

const wandAttributes = computed(() => [
  { label: '木材类型', value: wandResult.value?.wood },
  { label: '杖芯', value: wandResult.value?.core },
  { label: '长度', value: `${wandResult.value?.length} 英寸` },
  { label: '弹性', value: wandResult.value?.flexibility }
])

const selectOption = async (optionIndex: number) => {
  answers.value.push(optionIndex)

  if (currentQuestion.value < questions.length - 1) {
    currentQuestion.value++
  } else {
    step.value = 2
    await generateWand()
  }
}

const generateWand = async () => {
  try {
    const response = await axios.post('/api/wand/generate', {
      answers: answers.value
    })
    wandResult.value = response.data
    step.value = 3
  } catch (error) {
    // 演示模式：使用本地模拟数据
    setTimeout(() => {
      wandResult.value = {
        wood: ['冬青木', '山毛榉木', '橡木', '紫杉木'][answers.value[0]],
        core: ['凤凰羽毛', '龙神经', '独角兽毛', '雷鸟尾羽'][answers.value[1]],
        length: 10 + answers.value[2],
        flexibility: ['柔韧', '坚固', '弹性', '坚硬'][answers.value[3]],
        description: '这根魔杖与它的主人有着深厚的联系。它将在你手中展现出真正的力量，帮助你克服一切挑战。每一根魔杖都有其独特的性格，而这根选择了你，说明你们有着特殊的缘分。'
      }
      step.value = 3
    }, 2000)
  }
}

const saveWand = () => {
  userStore.setWand(wandResult.value)
  alert('魔杖已保存！')
}

const reset = () => {
  step.value = 1
  currentQuestion.value = 0
  answers.value = []
  wandResult.value = null
}
</script>

<style scoped>
.wand-view {
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
</style>
