import { defineStore } from 'pinia'

export const useGameStore = defineStore('game', {
  state: () => ({
    playerCount: 0,
    playerNumber: 1,
    roomName: '',
    userName: ''
  }),
  actions: {
    updatePlayerCount(count) {
      this.playerCount = count
    },
    updatePlayerNumber(number) {
      this.playerNumber = number
    },
    setRoomName(name) {
      this.roomName = name
    },
    setUserName(name) {
      this.userName = name
    }
  }
})