<template>
  <div class="characters-view">
    <div class="max-w-5xl mx-auto">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-hp-gold mb-2">角色互动对话</h2>
        <p class="text-gray-300">与魔法世界的角色深入交流</p>
      </div>

      <!-- 角色选择 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div
          v-for="char in characters"
          :key="char.id"
          @click="selectCharacter(char)"
          :class="[
            'card cursor-pointer transition-all duration-300 hover:scale-105',
            selectedCharacter?.id === char.id ? 'border-2 border-[#D4AF37]' : 'border-2 border-[#D4AF37]/30'
          ]"
        >
          <div class="text-center">
            <div class="text-5xl mb-2">{{ char.avatar }}</div>
            <h3 class="text-[#f1dc84] font-bold">{{ char.name }}</h3>
            <p class="text-gray-300 text-sm">{{ char.title }}</p>
          </div>
        </div>
      </div>

      <!-- 对话区域 -->
      <div v-if="selectedCharacter" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 对话历史 -->
        <div class="lg:col-span-2 card">
          <div ref="chatContainer" class="chat-container h-[500px] overflow-y-auto mb-4 space-y-4">
            <div
              v-for="(msg, idx) in messages"
              :key="idx"
              :class="msg.role === 'assistant' ? 'flex justify-start' : 'flex justify-end'"
            >
              <div
                :class="msg.role === 'assistant'
                  ? 'bg-black/60 border-2 border-[#D4AF37]/40'
                  : 'bg-black/60 border-2 border-[#D4AF37]/60'"
                class="max-w-[80%] p-4 rounded-lg"
              >
                <div class="flex items-center gap-2 mb-2">
                  <span v-if="msg.role === 'assistant'" class="text-xl">{{ selectedCharacter.avatar }}</span>
                  <span class="text-sm font-bold" :class="msg.role === 'assistant' ? 'text-hp-gold' : 'text-white'">
                    {{ msg.role === 'assistant' ? selectedCharacter.name : '你' }}
                  </span>
                </div>
                <p class="text-white whitespace-pre-wrap">{{ msg.content }}</p>
              </div>
            </div>

            <div v-if="isLoading" class="flex justify-start">
              <div class="bg-black/60 border-2 border-hp-gold/40 rounded-lg p-4">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-xl">{{ selectedCharacter.avatar }}</span>
                  <span class="text-sm font-bold text-hp-gold">{{ selectedCharacter.name }}</span>
                </div>
                <t-loading size="small" />
              </div>
            </div>
          </div>

          <!-- 快捷问题 -->
          <div v-if="messages.length <= 1" class="mb-4">
            <p class="text-gray-300 text-sm mb-2">试试问这些问题：</p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="(q, idx) in quickQuestions"
                :key="idx"
                @click="askQuickQuestion(q)"
                class="px-3 py-1.5 bg-black/60 border-2 border-[#D4AF37]/30 rounded-full text-sm text-white hover:border-[#D4AF37] hover:bg-black/80 transition-all"
              >
                {{ q }}
              </button>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="flex gap-3">
            <t-textarea
              v-model="userInput"
              placeholder="输入你想问的问题..."
              :autosize="{ minRows: 2, maxRows: 4 }"
              @keypress.ctrl.enter="sendMessage"
              :disabled="isLoading"
              class="flex-1"
            />
            <t-button @click="sendMessage" :disabled="isLoading || !userInput.trim()">
              发送
            </t-button>
          </div>
        </div>

        <!-- 角色信息 -->
        <div class="card">
          <div class="text-center mb-6">
            <div class="text-8xl mb-4">{{ selectedCharacter.avatar }}</div>
            <h3 class="text-2xl text-hp-gold font-bold">{{ selectedCharacter.name }}</h3>
            <p class="text-gray-300">{{ selectedCharacter.title }}</p>
          </div>

          <div class="space-y-4">
            <div>
              <h4 class="text-hp-gold font-bold mb-2">简介</h4>
              <p class="text-white text-sm">{{ selectedCharacter.description }}</p>
            </div>

            <div>
              <h4 class="text-hp-gold font-bold mb-2">特点</h4>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="(trait, idx) in selectedCharacter.traits"
                  :key="idx"
                  class="px-2 py-1 bg-black/60 border border-hp-gold/30 rounded text-xs text-white"
                >
                  {{ trait }}
                </span>
              </div>
            </div>

            <div>
              <h4 class="text-hp-gold font-bold mb-2">经典台词</h4>
              <p class="text-gray-200 text-sm italic">"{{ selectedCharacter.quote }}"</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, computed } from 'vue'
import axios from 'axios'

const chatContainer = ref<HTMLElement>()
const selectedCharacter = ref<any>(null)
const userInput = ref('')
const messages = ref<Array<{ role: string; content: string }>>([])
const isLoading = ref(false)

const characters = [
  {
    id: 'dumbledore',
    name: '阿白思·邓布利多',
    avatar: '🧙‍♂️',
    title: '霍格沃茨校长',
    description: '霍格沃茨魔法学校校长，被公认为当代最伟大的巫师。智慧、仁慈，对哈利关怀备至。',
    traits: ['智慧', '仁慈', '勇敢', '有远见'],
    quote: '决定我们成为什么样人的，不是我们的能力，而是我们的选择。'
  },
  {
    id: 'snape',
    name: '西弗勒斯·斯内普',
    avatar: '🧛',
    title: '魔药课教授',
    description: '斯莱特林学院院长，魔药课大师。外表冷漠严厉，内心却隐藏着深厚的情感。',
    traits: ['聪明', '勇敢', '忠诚', '复杂'],
    quote: 'Always。'
  },
  {
    id: 'hermione',
    name: '赫敏·格兰杰',
    avatar: '👩‍🎓',
    title: '最聪明的女巫',
    description: '哈利的好友，以超常的智慧和勤奋著称。对魔法知识有着近乎狂热的追求。',
    traits: ['聪明', '勇敢', '忠诚', '勤奋'],
    quote: '书本！还有聪明！但还有更多重要的东西——友谊和勇气。'
  },
  {
    id: 'voldemort',
    name: '伏地魔',
    avatar: '🐍',
    title: '黑魔头',
    description: '历史上最危险的黑巫师，追求永生和权力。他的名字被人们恐惧地称为"那个人"。',
    traits: ['强大', '狡猾', '无情', '孤独'],
    quote: '世上没有善恶，只有权力，还有那些太软弱而无法追求它的人。'
  }
]

const quickQuestions = computed(() => {
  if (!selectedCharacter.value) return []
  
  const questionMap: Record<string, string[]> = {
    dumbledore: ['邓布利多教授，您好', '什么是爱的力量？', '如何面对恐惧？', '您对哈利有什么建议？'],
    snape: ['教授，您好', '为什么您总是对哈利很严厉？', '魔药学的精髓是什么？', '您最骄傲的时刻是什么？'],
    hermione: ['赫敏，你好', '你怎么这么聪明？', '学习魔法最好的方法是什么？', '你和哈利是如何成为朋友的？'],
    voldemort: ['伏地魔', '你为什么追求永生？', '你后悔过什么吗？', '死亡意味着什么？']
  }
  
  return questionMap[selectedCharacter.value.id] || []
})

const selectCharacter = (char: any) => {
  selectedCharacter.value = char
  messages.value = []
  userInput.value = ''
  
  messages.value.push({
    role: 'assistant',
    content: `${char.name}：${getGreeting(char.id)}`
  })
  
  nextTick(() => {
    scrollToBottom()
  })
}

const getGreeting = (charId: string) => {
  const greetings: Record<string, string> = {
    dumbledore: '欢迎来到我的办公室，年轻的巫师。有什么我可以帮助你的吗？',
    snape: '你想要什么？如果是关于魔药学的，我或许可以指点一二。',
    hermione: '你好！很高兴见到你。你有什么问题想问吗？',
    voldemort: '竟然有人敢与我对话...说吧，你想知道什么？'
  }
  return greetings[charId] || '你好，有什么问题吗？'
}

const askQuickQuestion = (question: string) => {
  userInput.value = question
  sendMessage()
}

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value || !selectedCharacter.value) return

  messages.value.push({
    role: 'user',
    content: userInput.value
  })

  const userMessage = userInput.value
  userInput.value = ''
  isLoading.value = true

  try {
    const response = await axios.post('/api/characters/chat', {
      characterId: selectedCharacter.value.id,
      messages: messages.value
    })

    messages.value.push({
      role: 'assistant',
      content: response.data.message
    })
  } catch (error) {
    // 演示模式：模拟响应
    await simulateResponse(userMessage)
  }

  isLoading.value = false
  nextTick(() => {
    scrollToBottom()
  })
}

const simulateResponse = async (userMsg: string) => {
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  const responses = [
    '这是一个很有趣的问题。在魔法世界里，很多事物都和麻瓜世界很不一样...',
    '嗯...我理解你的意思。每个巫师都有自己的道路，重要的是要找到属于自己的那一条。',
    '魔法不仅仅是挥舞魔杖那么简单，它需要用心去感受，用智慧去理解。',
    '在霍格沃茨，我们学会的不仅仅是咒语，更是如何成为一个更好的人。'
  ]

  const randomResponse = responses[Math.floor(Math.random() * responses.length)]
  messages.value.push({
    role: 'assistant',
    content: randomResponse
  })
}

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-container {
  scroll-behavior: smooth;
}

:deep(.t-textarea__inner) {
  background: rgba(10, 10, 10, 0.8) !important;
  border: 2px solid rgba(212, 175, 55, 0.3) !important;
  color: white !important;
}

:deep(.t-textarea__inner:focus) {
  border-color: #D4AF37 !important;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2) !important;
}

:deep(.t-textarea__inner::placeholder) {
  color: rgba(255, 255, 255, 0.4) !important;
}
</style>
