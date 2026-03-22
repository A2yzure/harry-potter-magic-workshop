<template>
  <div class="sorting-view">
    <div class="max-w-5xl mx-auto">
      <!-- 标题区 -->
      <div class="text-center mb-12 relative">
        <div class="absolute -top-16 left-1/2 -translate-x-1/2 text-8xl opacity-20 magic-sparkle">🎩</div>
        <h2 class="text-5xl font-bold text-hp-gold mb-4 glow-text relative z-10">霍格沃茨分院测试</h2>
        <p class="text-lg text-gray-400 max-w-xl mx-auto">
          与分院帽对话，回答问题，找到你在霍格沃茨的真正归属
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- 左侧：对话区域 -->
        <div class="lg:col-span-2">
        <div class="rounded-2xl border-2 border-hp-gold/30 relative overflow-hidden"
             style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
          <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-80"></div>
          <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-hp-gold to-transparent opacity-60"></div>

          <div class="relative z-10 p-8">
            <!-- 对话历史 -->
            <div ref="chatContainer" class="chat-container h-96 overflow-y-auto mb-6 space-y-4 pr-2">
              <div
                v-for="(msg, idx) in chatMessages"
                :key="idx"
                :class="msg.role === 'assistant' ? 'flex justify-start' : 'flex justify-end'"
                class="animate-fadeIn"
              >
                <div
                  :class="msg.role === 'assistant'
                    ? 'bg-black/60 border-2 border-hp-gold/30 rounded-2xl rounded-tl-none'
                    : 'bg-black/60 border-2 border-hp-gold/40 rounded-2xl rounded-tr-none'"
                  class="max-w-[85%] p-5 shadow-lg"
                >
                  <div class="flex items-center gap-3 mb-3">
                    <span class="text-2xl">{{ msg.role === 'assistant' ? '🎩' : '👤' }}</span>
                    <span class="text-sm font-bold" :class="msg.role === 'assistant' ? 'text-hp-gold' : 'text-gray-300'">
                      {{ msg.role === 'assistant' ? '分院帽' : '你' }}
                    </span>
                  </div>
                  <p class="text-gray-200 leading-relaxed">{{ msg.content }}</p>
                </div>
              </div>

              <!-- 加载状态 -->
              <div v-if="isLoading" class="flex justify-start">
                <div class="bg-black/60 border-2 border-hp-gold/30 rounded-2xl rounded-tl-none p-5 shadow-lg">
                  <div class="flex items-center gap-3 mb-3">
                    <span class="text-2xl">🎩</span>
                    <span class="text-sm font-bold text-hp-gold">分院帽</span>
                  </div>
                  <t-loading size="small" />
                </div>
              </div>
            </div>

            <!-- 输入区域 -->
            <div v-if="!isSorted" class="flex gap-3">
              <t-input
                v-model="userInput"
                placeholder="回答分院帽的问题..."
                @keypress.enter="sendMessage"
                :disabled="isLoading"
                size="large"
                class="flex-1"
              >
                <template #suffix>
                  <span class="text-gray-500 text-sm">按 Enter 发送</span>
                </template>
              </t-input>
              <t-button @click="sendMessage" :disabled="isLoading || !userInput.trim()" size="large" class="px-6">
                发送
              </t-button>
            </div>

            <!-- 分院结果 -->
            <div v-if="isSorted && sortingResult" class="mt-8 text-center animate-fadeIn">
              <div class="text-8xl mb-6 magic-float">{{ houseEmoji[sortingResult.house] }}</div>
              <h3 class="text-4xl text-hp-gold font-bold mb-4 glow-text">
                {{ sortingResult.house }}！
              </h3>
              <p class="text-gray-300 mb-8 text-lg leading-relaxed">{{ sortingResult.description }}</p>

              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <div
                  v-for="(trait, idx) in sortingResult.traits"
                  :key="idx"
                  class="p-4 rounded-xl bg-black/60 border-2 border-hp-gold/20 hover:border-hp-gold/50 transition-colors"
                >
                  <div class="text-3xl mb-2">{{ trait.icon }}</div>
                  <div class="text-sm text-gray-300">{{ trait.name }}</div>
                </div>
              </div>

              <div class="flex justify-center gap-4">
                <t-button theme="success" size="large" @click="saveHouse" class="px-8">
                  确认加入 {{ sortingResult.house }}
                </t-button>
                <t-button variant="outline" size="large" @click="reset">
                  重新测试
                </t-button>
              </div>
            </div>
          </div>
        </div>
        </div>

        <!-- 右侧：学院介绍 -->
        <div class="space-y-4">
          <div class="rounded-2xl p-6 border-2 border-hp-gold/30"
               style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
            <h3 class="text-xl text-hp-gold font-bold mb-4">四大学院</h3>
            <div class="space-y-3">
              <div
                v-for="house in houses"
                :key="house.name"
                class="p-4 rounded-xl border-2 border-gray-700 hover:border-hp-gold/60 transition-all cursor-pointer group hover:scale-105 bg-black/40"
                :class="{'border-hp-gold/60 bg-hp-gold/10': sortingResult?.house === house.name}"
              >
                <div class="flex items-center gap-3">
                  <div class="text-3xl group-hover:scale-110 transition-transform">{{ house.icon }}</div>
                  <div>
                    <h4 class="text-hp-gold font-bold">{{ house.name }}</h4>
                    <p class="text-gray-300 text-xs">{{ house.motto }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 提示卡片 -->
          <div class="rounded-2xl p-6 border-2 border-hp-gold/30"
               style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
            <h3 class="text-lg text-hp-gold font-bold mb-3">💡 提示</h3>
            <ul class="text-sm text-gray-300 space-y-2">
              <li class="flex items-start gap-2">
                <span class="text-hp-gold">•</span>
                <span>真诚回答问题，分院帽会找到最适合你的学院</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-hp-gold">•</span>
                <span>没有"最好"的学院，每个学院都有其独特的价值</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-hp-gold">•</span>
                <span>分院结果会保存在你的账户中</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const userStore = useUserStore()

const chatContainer = ref<HTMLElement>()
const userInput = ref('')
const chatMessages = ref<Array<{ role: string; content: string }>>([])
const isLoading = ref(false)
const isSorted = ref(false)
const sortingResult = ref<any>(null)

const houseEmoji: Record<string, string> = {
  '格兰芬多': '🦁',
  '斯莱特林': '🐍',
  '拉文克劳': '🦅',
  '赫奇帕奇': '🦡'
}

const houses = [
  { name: '格兰芬多', icon: '🦁', motto: '勇气与荣耀', color: 'red' },
  { name: '斯莱特林', icon: '🐍', motto: '野心与智慧', color: 'green' },
  { name: '拉文克劳', icon: '🦅', motto: '智慧与才智', color: 'blue' },
  { name: '赫奇帕奇', icon: '🦡', motto: '忠诚与勤劳', color: 'yellow' }
]

onMounted(() => {
  startSorting()
})

const startSorting = async () => {
  chatMessages.value.push({
    role: 'assistant',
    content: '嗯...又一个新生来到了霍格沃茨。让我好好看看你...你的思想很有趣。告诉我，你觉得自己最大的优点是什么？'
  })
  await scrollToBottom()
}

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  chatMessages.value.push({
    role: 'user',
    content: userInput.value
  })

  const userMessage = userInput.value
  userInput.value = ''
  isLoading.value = true

  try {
    const response = await axios.post('/api/sorting/chat', {
      messages: chatMessages.value
    })

    const assistantMessage = response.data.message
    chatMessages.value.push({
      role: 'assistant',
      content: assistantMessage
    })

    if (response.data.sorted) {
      isSorted.value = true
      sortingResult.value = response.data.result
    }
  } catch (error) {
    // 演示模式：本地模拟
    await simulateResponse(userMessage)
  }

  isLoading.value = false
  await scrollToBottom()
}

const simulateResponse = async (userMsg: string) => {
  await new Promise(resolve => setTimeout(resolve, 1500))

  const responses = [
    '嗯...很有趣。那么，面对危险，你会怎么做？',
    '我看到了...但还需要了解更多。你最珍视什么？',
    '分院帽的视野越来越清晰了。告诉我，你希望别人记住你什么？',
    '这很难抉择...你更看重个人成就还是集体荣誉？',
    '嗯...你的内心很复杂。再告诉我最后一个问题，你最害怕什么？'
  ]

  const randomResponse = responses[Math.floor(Math.random() * responses.length)]
  chatMessages.value.push({
    role: 'assistant',
    content: randomResponse
  })

  // 模拟分院结果（第5个问题后）
  if (chatMessages.value.filter(m => m.role === 'user').length >= 5) {
    await new Promise(resolve => setTimeout(resolve, 2000))

    const houses = ['格兰芬多', '斯莱特林', '拉文克劳', '赫奇帕奇']
    const selectedHouse = houses[Math.floor(Math.random() * houses.length)]

    const houseTraits: Record<string, any> = {
      '格兰芬多': [
        { icon: '⚔️', name: '勇敢' },
        { icon: '🔥', name: '热情' },
        { icon: '💪', name: '坚韧' },
        { icon: '⭐', name: '领导力' }
      ],
      '斯莱特林': [
        { icon: '🎯', name: '野心' },
        { icon: '🧠', name: '智慧' },
        { icon: '🐍', name: '狡黠' },
        { icon: '💎', name: '优雅' }
      ],
      '拉文克劳': [
        { icon: '📚', name: '学识' },
        { icon: '💡', name: '创新' },
        { icon: '🔍', name: '洞察' },
        { icon: '🦅', name: '独立' }
      ],
      '赫奇帕奇': [
        { icon: '💛', name: '忠诚' },
        { icon: '🌱', name: '勤劳' },
        { icon: '🤝', name: '包容' },
        { icon: '🏆', name: '公正' }
      ]
    }

    isSorted.value = true
    sortingResult.value = {
      house: selectedHouse,
      description: `${selectedHouse}是最适合你的学院！你的特质与这里的精神完美契合。在这里，你将找到志同道合的伙伴，共同成长，追求卓越。`,
      traits: houseTraits[selectedHouse]
    }
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const saveHouse = () => {
  userStore.setHouse(sortingResult.value.house)
  alert(`恭喜你成为 ${sortingResult.value.house} 的学员！`)
}

const reset = () => {
  chatMessages.value = []
  userInput.value = ''
  isLoading.value = false
  isSorted.value = false
  sortingResult.value = null
  startSorting()
}
</script>

<style scoped>
.sorting-view {
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

.animate-fadeIn {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-container {
  scroll-behavior: smooth;
}

:deep(.t-input__inner) {
  background-color: rgba(26, 26, 46, 0.8);
  border-color: rgba(212, 175, 55, 0.3);
  color: white;
}

:deep(.t-input__inner:focus) {
  border-color: #D4AF37;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
}

:deep(.t-input__inner::placeholder) {
  color: rgba(156, 163, 175, 0.8);
}
</style>
