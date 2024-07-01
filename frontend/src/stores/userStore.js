import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const userName = ref('')
  const roomName = ref('')

  function setUserName(name) {
    userName.value = name
  }

  function setRoomName(name) {
    roomName.value = name
  }

  return { userName, roomName, setUserName, setRoomName }
})
