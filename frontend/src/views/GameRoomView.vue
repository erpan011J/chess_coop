<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12" md="8">
                <v-card>
                    <v-card-title>Chess Game</v-card-title>
                    <v-card-text>
                        <div id="board" style="width: 600px;"></div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <!-- Snackbar component for displaying errors -->
        <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout">
            {{ snackbarText }}
        </v-snackbar>
    </v-container>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { Chess } from 'chess.js';
import { fetchInitialRoomData } from '@/services/api';

const chess = new Chess();
let board;

// Snackbar state variables
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(3000);
const currentTurn = ref('w')
const tempTurn = ref('w')

// Retrieve username and roomName from localStorage
const roomName = localStorage.getItem('roomName');
const userName = localStorage.getItem('userName');

// WebSocket connection
const socket = new WebSocket(`ws://localhost:8000/ws/chess/${roomName}/`);

// Function to handle game event 
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

// Function to handle moves and send them via WebSocket
const handleMove = (source, target) => {
    if (source === target) return 'snapback';

    const move = {
        from: source,
        to: target,
        promotion: 'q'
    };

    const piece = chess.get(source);
    if (!piece || piece.color !== tempTurn.value) {
        // showSnackbar('Invalid move: it is not your turn.', 'error');
        return 'snapback';
    }

    try {
        const validMove = chess.move(move);

        if (validMove) {
            currentTurn.value = chess.turn(); 
            socket.send(JSON.stringify({
                'move': validMove,
                'fen': chess.fen(),
                'turn': chess.turn(),
            }));

            handleGameEndings();
        } else {
            showSnackbar('Invalid move: Please select a valid move.', 'error');
            return 'snapback';
        }
    } catch (error) {
        // showSnackbar('Invalid move: Please select a valid move.', 'error');
        return 'snapback';
    }
};

// Function to show snackbar with message and color
const showSnackbar = (message, color = 'info', timeout = 5000) => {
    snackbarText.value = message;
    snackbarColor.value = color;
    snackbarTimeout.value = timeout;
    snackbar.value = true;
};

onMounted(async () => {
    const orientationToTurn = {
        'white': 'w',
        'black': 'b',
    }

    try {
        const initialData = await fetchInitialRoomData(roomName, userName);
        let orientation, position = 'start';

        if (initialData[userName]) {
            orientation = initialData[userName].orientation;
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

        currentTurn.value = chess.turn(); // Initialize the turn based on the loaded game state
        board = Chessboard('board', {
            draggable: true,
            dropOffBoard: 'snapback',
            position: position,
            orientation: orientation,
            onDrop: handleMove,
            pieceTheme: piece => {
                const piecesPath = '/src/assets/pawn/';
                const pieceMap = {
                    'bK': `${piecesPath}b_king_1x.png`,
                    'bQ': `${piecesPath}b_queen_1x.png`,
                    'bR': `${piecesPath}b_rook_1x.png`,
                    'bB': `${piecesPath}b_bishop_1x.png`,
                    'bN': `${piecesPath}b_knight_1x.png`,
                    'bP': `${piecesPath}b_pawn_1x.png`,
                    'wK': `${piecesPath}w_king_1x.png`,
                    'wQ': `${piecesPath}w_queen_1x.png`,
                    'wR': `${piecesPath}w_rook_1x.png`,
                    'wB': `${piecesPath}w_bishop_1x.png`,
                    'wN': `${piecesPath}w_knight_1x.png`,
                    'wP': `${piecesPath}w_pawn_1x.png`
                };
                return pieceMap[piece];
            }
        });

        window.addEventListener('resize', () => {
            board.resize();
        });

    } catch (error) {
        console.log(error);
        showSnackbar('Error initializing chessboard. Please refresh the page.', 'error');
    }
});

// Handle incoming WebSocket messages
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const move = data.move;
    const fen = data.fen;
    const turn = data.turn;
    if(currentTurn.value == move.color) {
        chess.move(move);
        currentTurn.value = chess.turn();
        tempTurn.value = turn;
    } 
    board.position(fen);
    handleGameEndings();
};

</script>

<style scoped>
#board {
    margin: 20px auto;
    height: 100%;
}
</style>
