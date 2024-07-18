<template>
    <v-container fluid>
        <v-row>
            <v-col cols="12" md="8">
                <ChessBoard ref="boardComponent" :socket="socket" :showSnackbar="showSnackbar"
                    @gameEnding="handleGameEnding" />
            </v-col>
            <v-col cols="12" md="4">
                <Chat ref="chatComponent" :socket="socket" :userName="userName"/>
            </v-col>
        </v-row>
        <Snackbar ref="snackbarComponent" />
    </v-container>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useGameStore } from '@/stores/gameStore';
import Snackbar from '@/components/Snackbar.vue';
import ChessBoard from '@/components/ChessBoard.vue';
import Chat from '@/components/Chat.vue';


const gameStore = useGameStore();
const boardComponent = ref(null);
const chatComponent = ref(null);
const snackbarComponent = ref(null);
const socket = ref(null);
const roomName = localStorage.getItem('roomName')
const userName = localStorage.getItem('userName')

// Set room name and user name from localStorage
gameStore.setRoomName(roomName);
gameStore.setUserName(userName);

const initializeWebSocket = () => {
    socket.value = new WebSocket(`ws://localhost:8000/ws/chess/${gameStore.roomName}/`);

    socket.value.onopen = () => {
        socket.value.send(JSON.stringify({
            type: 'player_joined',
            username: gameStore.userName
        }));
    };

    socket.value.onmessage = event => {
        const data = JSON.parse(event.data);
        handleSocketMessage(data);
    };
};

const handleSocketMessage = data => {
    switch (data.type) {
        case 'move':
            boardComponent.value.updateBoard(data);
            break;
        case 'chat':
            chatComponent.value.addMessage(data.message);
            break;
        case 'player_joined':
            handlePlayerJoinedMessage(data);
            break;
        case 'player_left':
            handlePlayerLeftMessage(data);
            break;
        case 'error':
            showSnackbar(data.message, 'error');
            break;
        default:
            console.log('Unknown message type:', data.type);
    }
};

const handlePlayerJoinedMessage = data => {
    if (gameStore.userName !== data.username) {
        chatComponent.value.addSystemMessage(`${data.username} has joined the game.`);
        boardComponent.value.loadInitialData();
    }

};

const handlePlayerLeftMessage = data => {
    boardComponent.value.loadInitialData();
    chatComponent.value.addSystemMessage(`${data.username} has left the game.`);
};

const showSnackbar = (message, color, timeout) => {
    snackbarComponent.value.showSnackbar(message, color, timeout);
};

const handleGameEnding = (message) => {
    showSnackbar(message, 'info');
};

const handleBeforeUnload = event => {
    if (event.persisted) {
        sessionStorage.setItem('isReloading', 'true');
    }
};

const closeWebSocket = () => {
    const isReloading = sessionStorage.getItem('isReloading') === 'true';

    if (!isReloading && socket.value && socket.value.readyState === WebSocket.OPEN) {
        socket.value.send(JSON.stringify({
            type: 'player_left',
            username: gameStore.userName,
        }));
        socket.value.close();
    } else {
        sessionStorage.removeItem('isReloading');
    }
};

onMounted(() => {
    initializeWebSocket();
    window.addEventListener('beforeunload', handleBeforeUnload);
});

onBeforeUnmount(() => {
    window.removeEventListener('beforeunload', handleBeforeUnload);
    closeWebSocket();
});
</script>