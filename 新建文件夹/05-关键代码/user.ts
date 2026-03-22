import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const house = ref<string>('')
  const wand = ref<any>(null)
  const spells = ref<string[]>([])
  const puzzleProgress = ref(0)
  const unlockedSpells = ref<string[]>([])

  function setHouse(houseName: string) {
    house.value = houseName
  }

  function setWand(wandData: any) {
    wand.value = wandData
  }

  function unlockSpell(spellId: string) {
    if (!unlockedSpells.value.includes(spellId)) {
      unlockedSpells.value.push(spellId)
    }
  }

  function updatePuzzleProgress(level: number) {
    puzzleProgress.value = level
  }

  function reset() {
    house.value = ''
    wand.value = null
    spells.value = []
    puzzleProgress.value = 0
    unlockedSpells.value = []
  }

  return {
    house,
    wand,
    spells,
    puzzleProgress,
    unlockedSpells,
    setHouse,
    setWand,
    unlockSpell,
    updatePuzzleProgress,
    reset
  }
})
