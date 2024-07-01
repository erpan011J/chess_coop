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
import { useUserStore } from '@/stores/userStore';

const userStore = useUserStore();
const chess = new Chess();
let board;

// Snackbar state variables
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(3000);

// WebSocket connection
const socket = new WebSocket(`ws://localhost:8000/ws/chess/${userStore.roomName}/`);

// Function to handle moves and send them via WebSocket
const handleMove = (source, target) => {
    if (source === target) return 'snapback';

    const move = chess.move({
        from: source,
        to: target,
        promotion: 'q'
    });

    if (move) {
        socket.send(JSON.stringify({
            'move': move
        }));

        if (chess.isCheckmate()) {
            const winner = chess.turn() === 'w' ? 'Black' : 'White';
            showSnackbar(`Checkmate! ${winner} wins!`, 'info');
        } else if (chess.isDraw()) {
            showSnackbar('Draw by stalemate or insufficient material.', 'info');
        } else if (chess.isInsufficientMaterial()) {
            showSnackbar('Draw due to insufficient material.', 'info');
        } else if (chess.isStalemate()) {
            showSnackbar('Stalemate!', 'info');
        } else if (chess.isGameOver()) {
            showSnackbar('Game over!', 'info');
        }

        board.position(chess.fen());
    } else {
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

onMounted(() => {
    board = Chessboard('board', {
        draggable: true,
        dropOffBoard: 'snapback',
        position: 'start',
        orientation: 'white',
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

    // Resize chessboard on window resize
    window.addEventListener('resize', () => {
        board.resize();
    });

    // Handle incoming WebSocket messages
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const move = data.move;

        chess.move({
            from: move.from,
            to: move.to,
            promotion: move.promotion
        });

        board.position(chess.fen());
    };
});
</script>

<style scoped>
#board {
    margin: 20px auto;
    height: 100%;
}
</style>
