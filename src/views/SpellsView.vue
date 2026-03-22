<template>
  <div class="spells-view">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-hp-gold mb-2">魔法咒语学习</h2>
        <p class="text-gray-300">练习咒语发音，解锁魔法能力</p>
      </div>

      <!-- 咒语列表 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <div
          v-for="spell in spells"
          :key="spell.id"
          @click="selectSpell(spell)"
          class="card cursor-pointer transition-all duration-300"
          :class="[
            selectedSpell?.id === spell.id ? 'border-2 border-[#D4AF37]' : 'border-2 border-[#D4AF37]/30',
            isUnlocked(spell.id) ? 'opacity-100' : 'opacity-50'
          ]"
        >
          <div class="flex items-center justify-between mb-3">
            <span class="text-3xl magic-float">{{ spell.icon }}</span>
            <span v-if="isUnlocked(spell.id)" class="text-hp-gold text-xl">✓</span>
            <span v-else class="text-gray-500 text-xl">🔒</span>
          </div>
          <h3 class="text-lg font-bold text-hp-gold mb-1">{{ spell.name }}</h3>
          <p class="text-white text-sm">{{ spell.incantation }}</p>
          <p class="text-gray-300 text-xs mt-2">{{ spell.effect }}</p>
        </div>
      </div>

      <!-- 练习区域 -->
      <div v-if="selectedSpell" class="card">
        <div class="text-center mb-8">
          <div class="text-6xl mb-4">{{ selectedSpell.icon }}</div>
          <h3 class="text-2xl text-hp-gold font-bold mb-2">{{ selectedSpell.name }}</h3>
          <p class="text-xl text-white mb-4">{{ selectedSpell.incantation }}</p>
          <p class="text-gray-300">{{ selectedSpell.description }}</p>
        </div>

        <!-- 播放示范发音 -->
        <div class="text-center mb-6">
          <t-button variant="outline" @click="playDemonstration">
            🔊 播放示范发音
          </t-button>
        </div>

        <!-- 录音练习 -->
        <div v-if="isUnlocked(selectedSpell.id)" class="border-t border-hp-gold/20 pt-6">
          <h4 class="text-xl text-hp-gold mb-4">发音练习</h4>

          <div class="flex flex-col items-center">
            <button
              @click="toggleRecording"
              class="magic-btn w-24 h-24 rounded-full flex items-center justify-center text-4xl mb-6 transition-all duration-300 border-2"
              :class="[
                isRecording ? 'bg-red-600 border-red-400 animate-pulse' : 'bg-black/60 border-[#D4AF37]/50 hover:bg-black/80'
              ]"
            >
              {{ isRecording ? '⏹️' : '🎤' }}
            </button>
            <p class="text-white mb-4">{{ recordingStatus }}</p>

            <!-- 评分结果 -->
            <div v-if="score !== null" class="w-full max-w-md">
              <div class="text-center mb-4">
                <div class="text-5xl font-bold glow-text" :class="getScoreColor(score)">
                  {{ score }}
                </div>
                <p class="text-white text-sm">发音准确度</p>
              </div>
              <div v-if="feedback" class="rounded-xl p-4 mb-4 border-2 border-hp-gold/20"
                   style="background: rgba(10, 10, 10, 0.8);">
                <h5 class="text-hp-gold mb-2">改进建议</h5>
                <p class="text-white text-sm">{{ feedback }}</p>
              </div>
              <t-button theme="success" size="large" block @click="confirmScore" class="!bg-gradient-to-r from-green-600 to-green-700 !border-green-500">
                确认成绩
              </t-button>
            </div>
          </div>
        </div>

        <div v-else class="text-center">
          <t-alert theme="warning" message="请先通过对话练习解锁此咒语" />
          <t-button theme="default" class="mt-4" @click="startUnlockChallenge">
            开始解锁挑战
          </t-button>
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

const selectedSpell = ref<any>(null)
const isRecording = ref(false)
const recordingStatus = ref('点击麦克风开始录音')
const score = ref<number | null>(null)
const feedback = ref('')

const spells = [
  {
    id: 'lumos',
    name: '荧光闪烁',
    incantation: 'Lumos',
    effect: '产生光亮',
    icon: '💡',
    description: '让魔杖尖端发出光亮，照亮黑暗的地方'
  },
  {
    id: 'expelliarmus',
    name: '缴械咒',
    incantation: 'Expelliarmus',
    effect: '解除武装',
    icon: '⚔️',
    description: '让对手失去手中的魔杖或其他武器'
  },
  {
    id: 'stupefy',
    name: '昏迷咒',
    incantation: 'Stupefy',
    effect: '使人昏迷',
    icon: '💫',
    description: '使目标瞬间昏迷，暂时失去意识'
  },
  {
    id: 'protego',
    name: '护盾咒',
    incantation: 'Protego',
    effect: '防护魔法',
    icon: '🛡️',
    description: '召唤一面隐形盾牌，阻挡魔咒和攻击'
  },
  {
    id: 'wingardium',
    name: '漂浮咒',
    incantation: 'Wingardium Leviosa',
    effect: '让物体漂浮',
    icon: '🪶',
    description: '让物体悬浮在空中，并控制其移动'
  },
  {
    id: 'accio',
    name: '召唤咒',
    incantation: 'Accio',
    effect: '召唤物体',
    icon: '🎯',
    description: '让远处的物体飞向自己'
  }
]

const isUnlocked = (spellId: string) => {
  return userStore.unlockedSpells.includes(spellId)
}

const selectSpell = (spell: any) => {
  selectedSpell.value = spell
  score.value = null
  feedback.value = ''
  recordingStatus.value = '点击麦克风开始录音'
}

const playDemonstration = () => {
  // 演示模式：使用浏览器TTS播放示范发音
  const utterance = new SpeechSynthesisUtterance(selectedSpell.value.incantation)
  utterance.lang = 'en-US'
  utterance.rate = 0.8
  speechSynthesis.speak(utterance)
}

const toggleRecording = async () => {
  if (!isRecording.value) {
    isRecording.value = true
    recordingStatus.value = '正在录音...请清晰念出咒语'
    
    try {
      // 实际项目中这里应该调用录音API和语音识别服务
      // 演示模式：模拟录音和评分
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      const randomScore = Math.floor(Math.random() * 30) + 70
      score.value = randomScore
      
      if (randomScore >= 90) {
        feedback.value = '完美！你的发音非常标准，堪比霍格沃茨教授！'
      } else if (randomScore >= 80) {
        feedback.value = '很好！注意尾音要更加饱满一些。'
      } else if (randomScore >= 70) {
        feedback.value = '还不错，多练习几次就会更好。注意元音的发音。'
      } else {
        feedback.value = '继续加油！注意每个音节都要清晰。'
      }
      
      recordingStatus.value = '录音完成'
    } catch (error) {
      recordingStatus.value = '录音失败，请检查麦克风权限'
    }
    
    isRecording.value = false
  }
}

const getScoreColor = (s: number) => {
  if (s >= 90) return 'text-green-400'
  if (s >= 80) return 'text-yellow-400'
  if (s >= 70) return 'text-orange-400'
  return 'text-red-400'
}

const confirmScore = () => {
  alert(`成绩已记录：${score.value} 分`)
  score.value = null
  feedback.value = ''
  recordingStatus.value = '点击麦克风开始录音'
}

const startUnlockChallenge = () => {
  alert('解锁挑战功能即将上线，敬请期待！')
}
</script>
