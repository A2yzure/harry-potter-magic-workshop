<template>
  <div class="puzzles-view">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-hp-gold mb-2">谜题闯关游戏</h2>
        <p class="text-gray-400">挑战经典谜题，测试你的魔法智慧</p>
      </div>

      <!-- 关卡进度 -->
      <div class="rounded-2xl p-6 mb-8 border-2 border-hp-gold/40"
           style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl text-hp-gold font-bold">关卡进度</h3>
          <span class="text-gray-300">{{ currentLevel }} / {{ puzzles.length }}</span>
        </div>
        <div class="grid grid-cols-7 gap-2">
          <div
            v-for="(puzzle, idx) in puzzles"
            :key="puzzle.id"
            @click="selectLevel(idx)"
            class="aspect-square rounded-lg flex items-center justify-center cursor-pointer transition-all duration-300 border-2 font-bold"
            :class="getLevelClass(idx)"
          >
            {{ idx + 1 }}
          </div>
        </div>
      </div>

      <!-- 谜题区域 -->
      <div v-if="currentPuzzle" class="rounded-2xl p-8 border-2 border-hp-gold/40"
           style="background: linear-gradient(145deg, #0a0a0a 0%, #1a1a1a 100%);">
        <div class="text-center mb-8">
          <div class="text-6xl mb-4 magic-float">{{ currentPuzzle.icon }}</div>
          <h3 class="text-2xl text-hp-gold font-bold mb-2">{{ currentPuzzle.title }}</h3>
          <p class="text-gray-300">{{ currentPuzzle.scene }}</p>
        </div>

        <!-- 谜题描述 -->
        <div class="rounded-xl p-6 mb-6 border-2 border-hp-gold/20"
             style="background: rgba(10, 10, 10, 0.8);">
          <h4 class="text-hp-gold font-bold mb-4">🧩 谜题</h4>
          <p class="text-gray-200 text-lg leading-relaxed">{{ currentPuzzle.puzzle }}</p>
        </div>

        <!-- 对话线索 -->
        <div v-if="showHint" class="rounded-xl p-4 mb-6 border-2 border-hp-gold/30"
             style="background: rgba(10, 10, 10, 0.7);">
          <h4 class="text-hp-gold font-bold mb-2">💡 线索</h4>
          <p class="text-gray-300">{{ currentPuzzle.hint }}</p>
        </div>

        <!-- 答题区域 -->
        <div v-if="!solved" class="space-y-4">
          <div>
            <label class="text-gray-300 text-sm mb-2 block">你的答案</label>
            <t-input
              v-model="userAnswer"
              placeholder="输入你的答案..."
              @keypress.enter="checkAnswer"
              size="large"
            />
          </div>
          
          <div class="flex gap-4">
            <t-button @click="checkAnswer" :disabled="!userAnswer.trim()">
              提交答案
            </t-button>
            <t-button variant="outline" @click="showHint = !showHint">
              {{ showHint ? '隐藏线索' : '显示线索' }}
            </t-button>
            <t-button variant="outline" @click="showDialog = true">
              与向导对话
            </t-button>
          </div>

          <!-- 答案提示 -->
          <div v-if="attemptCount >= 2" class="rounded-lg p-4 border-2 border-orange-500/30"
               style="background: rgba(217, 119, 6, 0.2);">
            <p class="text-orange-400 text-sm">💭 提示：仔细阅读谜题中的关键词...</p>
          </div>
        </div>

        <!-- 成功提示 -->
        <div v-if="solved" class="text-center">
          <div class="text-6xl mb-4 magic-sparkle">🎉</div>
          <h3 class="text-3xl text-hp-gold font-bold mb-4 glow-text">正确！</h3>
          <p class="text-gray-300 mb-6">{{ currentPuzzle.explanation }}</p>
          <div class="flex justify-center gap-4">
            <t-button theme="success" size="large" @click="nextLevel">
              {{ currentLevel < puzzles.length ? '下一关' : '完成挑战' }}
            </t-button>
            <t-button variant="outline" @click="retry">
              重试此关
            </t-button>
          </div>
        </div>
      </div>

      <!-- 向导对话弹窗 -->
      <t-dialog v-model:visible="showDialog" header="与邓布利多对话" width="800px">
        <div class="space-y-4 max-h-96 overflow-y-auto">
          <div
            v-for="(msg, idx) in guideMessages"
            :key="idx"
            :class="msg.role === 'assistant' ? 'text-left' : 'text-right'"
          >
            <div
              :class="msg.role === 'assistant'
                ? 'bg-black/60 border-2 border-hp-gold/40 rounded-2xl rounded-tl-none'
                : 'bg-hp-gold/15 border-2 border-hp-gold/40 rounded-2xl rounded-tr-none'"
              class="inline-block p-4 max-w-[80%]"
            >
              <p class="text-gray-200">{{ msg.content }}</p>
            </div>
          </div>
        </div>
        <div class="mt-4 flex gap-2">
          <t-input
            v-model="guideInput"
            placeholder="向邓布利多提问..."
            @keypress.enter="askGuide"
            class="flex-1"
          />
          <t-button @click="askGuide">提问</t-button>
        </div>
      </t-dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const currentLevel = ref(1)
const userAnswer = ref('')
const showHint = ref(false)
const solved = ref(false)
const attemptCount = ref(0)
const showDialog = ref(false)
const guideInput = ref('')
const guideMessages = ref<Array<{ role: string; content: string }>>([])

const puzzles = [
  {
    id: 1,
    title: '三头犬的谜题',
    scene: '你在魔法石保卫战中遇到了巨大的三头犬路威...',
    icon: '🐕',
    puzzle: '我没有眼睛却能看见，没有翅膀却能飞翔，没有身体却能穿越山河。没有空气却能呼吸，没有声音却能歌唱。我是什么？',
    hint: '邓布利多：想想那些无形却无处不在的事物...',
    explanation: '风！风看不见却能吹动万物，没有翅膀却能远行，无形却能传递声音。'
  },
  {
    id: 2,
    title: '飞马谜题',
    scene: '你需要从一群生物中选出唯一可以骑乘的...',
    icon: '🦄',
    puzzle: '我的兄弟会咬人，我的姐妹会蜇人，但我不伤害任何人。我有翅膀却不是鸟，我能飞翔却不是天使。我是什么？',
    hint: '赫敏：不是所有马都能飞，也不是所有有翅膀的都是鸟...',
    explanation: '独角兽或飞马！在魔法生物中，它们是温和无害的神奇生物。'
  },
  {
    id: 3,
    title: '魔药谜题',
    scene: '斯内普教授的魔药课，他提出了一个经典问题...',
    icon: '⚗️',
    puzzle: '我既是毒药也是良药，尝起来苦涩却能带来甜美。一滴可以夺命，适量却能救命。我是魔药师的助手，也是巫师的工具。我是什么？',
    hint: '斯内普：魔药的本质在于剂量...',
    explanation: '魔药本身！魔药既可以用来伤害也可以用来拯救，关键在于用途和剂量。'
  },
  {
    id: 4,
    title: '镜子谜题',
    scene: '你站在厄里斯魔镜前，看到了不同的景象...',
    icon: '🪞',
    puzzle: '我能展示你最深切的渴望，我也能揭示你最深的恐惧。我从不撒谎，但也不总是说真话。我可以预见未来，也可以改变过去。我是什么？',
    hint: '邓布利多：这面镜子的名字叫厄里斯...',
    explanation: '镜子/厄里斯魔镜！镜子反射现实，但厄里斯魔镜展示的是人内心深处的渴望。'
  },
  {
    id: 5,
    title: '时间谜题',
    scene: '赫敏在研究时间转换器时遇到的难题...',
    icon: '⏰',
    puzzle: '我能让昨天成为明天，也能让明天回到昨天。我能让年轻人变老，也能让老人重返青春。但我从不改变任何事物的本质。我是什么？',
    hint: '赫敏：时间是相对的，时间是循环的...',
    explanation: '时间转换器！它可以让人回到过去，但不能改变已经发生的事情。'
  },
  {
    id: 6,
    title: '死亡圣器谜题',
    scene: '你正在研究三兄弟的故事...',
    icon: '☠️',
    puzzle: '三个兄弟，三件圣器。老三想要逃避死亡，老二想要召回爱人，老大想要主宰战争。哪个兄弟是真正的胜利者？',
    hint: '邓布利多：理解死亡，才能超越死亡...',
    explanation: '老三！他明智地使用了隐身衣，最终接受了自己的命运，成为了真正的死亡大师。'
  },
  {
    id: 7,
    title: '爱的谜题',
    scene: '哈利在面对伏地魔时最后的思考...',
    icon: '❤️',
    puzzle: '它看不见摸不着，却能创造奇迹。它是最强大的魔法，最古老的咒语。它能让死去的生命延续，让懦弱的人变得勇敢。它是什么？',
    hint: '邓布利多：这是伏地魔永远无法理解的力量...',
    explanation: '爱！爱是伏地魔无法理解也无法击败的力量，它保护了哈利，也拯救了魔法世界。'
  }
]

const currentPuzzle = computed(() => {
  return puzzles[currentLevel.value - 1]
})

const getLevelClass = (idx: number) => {
  const level = idx + 1
  if (level < currentLevel.value) {
    return 'bg-green-600/80 border-green-500/60 text-white border-2'
  } else if (level === currentLevel.value) {
    return 'bg-hp-gold text-black border-2 border-hp-gold shadow-lg shadow-hp-gold/30'
  } else {
    return 'bg-black/60 border-gray-700/50 text-gray-400 border-2'
  }
}

const selectLevel = (idx: number) => {
  if (idx + 1 <= currentLevel.value || isLevelCompleted(idx + 1)) {
    currentLevel.value = idx + 1
    userAnswer.value = ''
    showHint.value = false
    solved.value = false
    attemptCount.value = 0
  }
}

const isLevelCompleted = (level: number) => {
  return level <= currentLevel.value && solved.value
}

const checkAnswer = () => {
  if (!userAnswer.value.trim()) return

  attemptCount.value++
  
  const correctAnswers = getCorrectAnswers(currentLevel.value)
  const isCorrect = correctAnswers.some(
    ans => userAnswer.value.toLowerCase().trim() === ans.toLowerCase()
  )

  if (isCorrect) {
    solved.value = true
    userStore.updatePuzzleProgress(currentLevel.value)
  } else if (attemptCount.value >= 3) {
    alert('答案不正确。提示：' + currentPuzzle.value.hint)
  } else {
    alert('答案不正确，请再试试！')
  }
}

const getCorrectAnswers = (level: number) => {
  const answers: Record<number, string[]> = {
    1: ['风', 'wind', '微风', '气流'],
    2: ['独角兽', '飞马', 'unicorn', 'pegasus'],
    3: ['魔药', 'potion', '药剂'],
    4: ['镜子', '魔镜', '厄里斯魔镜', 'mirror', 'erised'],
    5: ['时间转换器', '时间器', 'time turner', '时间'],
    6: ['老三', '第三个兄弟', 'the third brother', '佩弗利尔三兄弟'],
    7: ['爱', 'love', '爱意']
  }
  return answers[level] || []
}

const nextLevel = () => {
  if (currentLevel.value < puzzles.length) {
    currentLevel.value++
    userAnswer.value = ''
    showHint.value = false
    solved.value = false
    attemptCount.value = 0
  } else {
    alert('恭喜你完成了所有谜题挑战！🎉')
  }
}

const retry = () => {
  userAnswer.value = ''
  showHint.value = false
  solved.value = false
  attemptCount.value = 0
}

const askGuide = async () => {
  if (!guideInput.value.trim()) return

  guideMessages.value.push({
    role: 'user',
    content: guideInput.value
  })

  const question = guideInput.value
  guideInput.value = ''

  // 模拟邓布利多回复
  setTimeout(() => {
    const responses = [
      '这是一个很好的问题。在魔法世界里，答案往往隐藏在细节中...',
      '让我想想...记住，最复杂的谜题往往有最简单的答案。',
      '你已经很接近了。再仔细读一遍谜题，你会发现的。',
      '邓布利多总是说，不要忽视显而易见的事物。'
    ]
    
    guideMessages.value.push({
      role: 'assistant',
      content: responses[Math.floor(Math.random() * responses.length)]
    })
  }, 1000)
}
</script>
