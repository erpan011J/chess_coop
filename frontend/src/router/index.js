import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GameRoomView from '../views/GameRoomView.vue'
// import ChessRoom from '../components/ChessRoom.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/room/:roomname',
      name: 'room',
      component: GameRoomView
    }
    // {
    //   path: '/room/:roomname',
    //   name: 'room',
    //   component: ChessRoom,
    //   props: true
    // },
  ]
})

export default router
