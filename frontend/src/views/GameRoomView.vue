<template>
    <v-container fluid>
        <v-row>
            <v-col cols="12" md="8">
                <v-card>
                    <v-card-text>
                        <div id="board" style="width: 80%;"></div>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12" md="4">
                <v-card class="chat-card">
                    <v-card-text class="chat-messages">
                        <div v-for="(message, index) in chatMessages" :key="index"
                            :class="['message', message.user === userName ? 'message-right' : 'message-left']">
                            <div class="message-content">
                                <strong>{{ message.user }}:</strong> {{ message.text }}
                            </div>
                        </div>
                    </v-card-text>
                    <v-card-actions class="chat-input">
                        <v-text-field v-model="chatInput" label="Type a message" @keyup.enter="sendChatMessage"
                            hide-details dense></v-text-field>
                        <v-btn @click="sendChatMessage" color="primary" class="ml-2">Send</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
        <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout">
            {{ snackbarText }}
        </v-snackbar>
    </v-container>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue';
import { Chess } from 'chess.js';
import { fetchInitialRoomData } from '@/services/api';

const chess = new Chess();
let board;

const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(3000);
const currentTurn = ref('w');
const tempTurn = ref('w');
const chatMessages = ref([]);
const chatInput = ref('');
const roomName = localStorage.getItem('roomName');
const userName = localStorage.getItem('userName');
const playerCount = ref(0);
const playerNumber = ref(1);
const socket = ref(null);
const isSocketReady = ref(false);

const orientationToTurn = {
    white: 'w',
    black: 'b',
};

const loadInitialData = async () => {
    try {
        const initialData = await fetchInitialRoomData(roomName, userName);
        let orientation;
        let position = 'start';

        if (initialData[userName]) {
            orientation = initialData[userName].orientation;
            playerCount.value = initialData.players;
            playerNumber.value = initialData[userName].player;
        } else {
            showSnackbar('You are not a player in this room.', 'error');
            return;
        }

        if (initialData.fen) {
            chess.load(initialData.fen);
            position = initialData.fen;
            tempTurn.value = orientationToTurn[orientation];
            handleGameEndings();
        }

        currentTurn.value = chess.turn();

        board = Chessboard('board', {
            draggable: true,
            dropOffBoard: 'snapback',
            position: position,
            orientation: orientation,
            onDrop: handleMove,
            pieceTheme: piece => {
                const piecesPath = '/src/assets/pawn/';
                const pieceMap = {
                    bK: `${piecesPath}b_king_1x.png`,
                    bQ: `${piecesPath}b_queen_1x.png`,
                    bR: `${piecesPath}b_rook_1x.png`,
                    bB: `${piecesPath}b_bishop_1x.png`,
                    bN: `${piecesPath}b_knight_1x.png`,
                    bP: `${piecesPath}b_pawn_1x.png`,
                    wK: `${piecesPath}w_king_1x.png`,
                    wQ: `${piecesPath}w_queen_1x.png`,
                    wR: `${piecesPath}w_rook_1x.png`,
                    wB: `${piecesPath}w_bishop_1x.png`,
                    wN: `${piecesPath}w_knight_1x.png`,
                    wP: `${piecesPath}w_pawn_1x.png`,
                };
                return pieceMap[piece];
            },
        });

        window.addEventListener('resize', () => {
            board.resize();
        });

        initializeWebSocket();
    } catch (error) {
        console.log(error);
        showSnackbar('Error initializing chessboard. Please refresh the page.', 'error');
    }
};

const initializeWebSocket = () => {
    socket.value = new WebSocket(`ws://localhost:8000/ws/chess/${roomName}/`);

    socket.value.onopen = () => {
        socket.value.send(JSON.stringify({
            type: 'player_joined',
            username: userName,
            number_of_players: playerCount.value,
            player_number: playerNumber.value,
        }));
        isSocketReady.value = true;
    };

    socket.value.onmessage = event => {
        if (!isSocketReady.value) return;

        const data = JSON.parse(event.data);
        handleSocketMessage(data);
    };
};

const handleSocketMessage = data => {
    switch (data.type) {
        case 'move':
            handleMoveMessage(data);
            break;
        case 'chat':
            chatMessages.value.push(data.message);
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

const handleMoveMessage = data => {
    const { move, fen, turn } = data;
    if (currentTurn.value === move.color) {
        chess.move(move);
        currentTurn.value = chess.turn();
        tempTurn.value = turn;
    }
    board.position(fen);
    handleGameEndings();
};

const handlePlayerJoinedMessage = data => {
    playerCount.value = data.number_of_players;
    playerNumber.value = data.number_of_players;
    if (userName !== data.username) {
        addSystemMessage(`${data.username} has joined the game.`);
    }
    if (playerCount.value === 2) {
        showSnackbar('Both players have joined. The game can now begin!', 'info');
    }
};

const handlePlayerLeftMessage = data => {
    playerCount.value = data.number_of_players;
    playerNumber.value = data.number_of_players;
    addSystemMessage(`${data.username} has left the game.`);
    loadInitialData();
};

const handleGameEndings = () => {
    const gameEndings = [
        { condition: chess.isCheckmate, message: `Checkmate! ${chess.turn() === 'w' ? 'Black' : 'White'} wins!` },
        { condition: chess.isDraw, message: 'Draw by stalemate or insufficient material.' },
        { condition: chess.isInsufficientMaterial, message: 'Draw due to insufficient material.' },
        { condition: chess.isStalemate, message: 'Stalemate!' },
        { condition: chess.isGameOver, message: 'Game over!' },
    ];

    for (const ending of gameEndings) {
        if (ending.condition.call(chess)) {
            showSnackbar(ending.message, 'info');
            break;
        }
    }
};

const handleMove = (source, target) => {
    if (playerCount.value < 2) {
        showSnackbar('Waiting for another player to join.', 'warning');
        return 'snapback';
    }

    if (source === target) return 'snapback';

    const move = {
        from: source,
        to: target,
        promotion: 'q',
    };

    const piece = chess.get(source);
    if (!piece || piece.color !== tempTurn.value) {
        return 'snapback';
    }

    try {
        const validMove = chess.move(move);

        if (validMove) {
            currentTurn.value = chess.turn();
            socket.value.send(JSON.stringify({
                type: 'move',
                move: validMove,
                fen: chess.fen(),
                turn: chess.turn(),
            }));

            handleGameEndings();
        } else {
            showSnackbar('Invalid move: Please select a valid move.', 'error');
            return 'snapback';
        }
    } catch (error) {
        return 'snapback';
    }
};

const sendChatMessage = () => {
    if (chatInput.value.trim() !== '') {
        const message = {
            user: userName,
            text: chatInput.value.trim(),
        };
        socket.value.send(JSON.stringify({
            type: 'chat',
            message: message,
        }));
        chatInput.value = '';
    }
};

const showSnackbar = (message, color = 'info', timeout = 5000) => {
    snackbarText.value = message;
    snackbarColor.value = color;
    snackbarTimeout.value = timeout;
    snackbar.value = true;
};

const addSystemMessage = message => {
    chatMessages.value.push({
        user: 'System',
        text: message,
        isSystem: true,
    });
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
            username: userName,
            number_of_players: playerCount.value,
            player_number: playerNumber.value,
        }));
        socket.value.close();
    } else {
        sessionStorage.removeItem('isReloading');
    }
};

onMounted(() => {
    loadInitialData();
    window.addEventListener('beforeunload', handleBeforeUnload);
});

onBeforeUnmount(() => {
    window.removeEventListener('beforeunload', handleBeforeUnload);
    closeWebSocket();
});
</script>

<style scoped>
#board {
    margin: 20px auto;
    height: 100%;
}

.chat-card {
    height: 100%;
    display: flex;
    flex-direction: column;
}

.chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    height: auto;
    padding: 16px;
    background-color: #44dbf130;
}

.message {
    margin-bottom: 16px;
    max-width: 80%;
    clear: both;
}

.message-content {
    padding: 8px 12px;
    border-radius: 12px;
    display: inline-block;
}

.message-left {
    float: left;
}

.message-left .message-content {
    background-color: #f0f0f0;
    border: 1px solid #e0e0e0;
}

.message-right {
    float: right;
}

.message-right .message-content {
    background-color: #e3f2fd;
    border: 1px solid #bbdefb;
}

.chat-input {
    padding: 16px;
    background-color: #f5f5f5;
    display: flex;
    align-items: center;
}

.chat-input .v-text-field {
    flex-grow: 1;
}

.message-system {
    text-align: center;
    margin-bottom: 16px;
}

.message-system .message-content {
    background-color: #e8eaf6;
    border: 1px solid #c5cae9;
    color: #3f51b5;
    padding: 4px 8px;
    border-radius: 12px;
    display: inline-block;
}
</style>