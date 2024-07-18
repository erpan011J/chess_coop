<template>
    <v-card>
        <v-card-text>
            <div id="board" style="width: 80%;"></div>
        </v-card-text>
    </v-card>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue';
import { useGameStore } from '@/stores/gameStore';
import { Chess } from 'chess.js';
import { fetchInitialRoomData } from '@/services/roomService';

const props = defineProps(['socket', 'showSnackbar']);
const emit = defineEmits(['gameEnding']);

const gameStore = useGameStore();
const chess = new Chess();
let board;

const currentTurn = ref('w');
const playerTurn = ref('w');

const orientationToTurn = {
    'white': 'w',
    'black': 'b',
};

const loadInitialData = async () => {
    try {
        const initialFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        const initialData = await fetchInitialRoomData(gameStore.roomName, gameStore.userName);
        let orientation;
        let position = 'start';
        chess.load(initialFen);

        if (initialData.players === 2) {
            props.showSnackbar('Both players have joined. The game can now begin!', 'info');
        }

        if (initialData[gameStore.userName]) {
            orientation = initialData[gameStore.userName].orientation;
            playerTurn.value = orientationToTurn[orientation];
            gameStore.updatePlayerCount(initialData.players);
            gameStore.updatePlayerNumber(initialData[gameStore.userName].player);
        } else {
            props.showSnackbar('You are not a player in this room.', 'error');
            return;
        }

        if (initialData.fen) {
            position = initialData.fen;
            chess.load(initialData.fen)
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

    } catch (error) {
        console.log(error)
        props.showSnackbar('Error initializing chessboard. Please refresh the page.', 'error');
    }
};

const handleMove = (source, target) => {
    if (gameStore.playerCount < 2) {
        props.showSnackbar('Waiting for another player to join.', 'warning');
        return 'snapback';
    }

    if (source === target) return 'snapback';

    const move = {
        from: source,
        to: target,
        promotion: 'q',
    };

    const piece = chess.get(source);
    if (!piece || piece.color !== playerTurn.value) {
        return 'snapback';
    }

    try {
        const validMove = chess.move(move);

        if (validMove) {
            currentTurn.value = chess.turn();
            props.socket.send(JSON.stringify({
                type: 'move',
                move: validMove,
                fen: chess.fen(),
                turn: chess.turn(),
            }));

            handleGameEndings();
        } else {
            props.showSnackbar('Invalid move: Please select a valid move.', 'error');
            return 'snapback';
        }
    } catch (error) {
        return 'snapback';
    }
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
            emit('gameEnding', ending.message);
            break;
        }
    }
};

const updateBoard = data => {
    const { move, fen, turn } = data;
    if (currentTurn.value === move.color) {
        chess.move(move);
        currentTurn.value = chess.turn();
        playerTurn.value = turn;
    }
    board.position(fen);
    handleGameEndings();
};

onMounted(() => {
    loadInitialData();
});

onBeforeUnmount(() => {
    window.removeEventListener('resize', board.resize);
});

defineExpose({
    updateBoard,
    loadInitialData,
});
</script>

<style scoped>
#board {
    margin: 20px auto;
    height: 100%;
}
</style>