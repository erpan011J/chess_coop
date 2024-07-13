<template>
  <v-container>
    <div class="text-center mb-6 mt-2" style="font-size: 30px;">
      <h2>Chess Coop</h2>
    </div>
    <v-row class="d-flex justify-center align-center" style="height: 70vh;">
      <v-col cols="12" md="6">
        <v-card class="mx-auto" elevation="16">
          <v-card-title>Create or Join Game</v-card-title>
          <v-card-text class="card-content">
            <v-form ref="formRef" @submit.prevent="handleRoomAction">
              <v-text-field v-model="roomName" label="Room Name" required :rules="roomNameRules"></v-text-field>
              <v-text-field v-model="userName" label="User Name" required :rules="userNameRules"></v-text-field>
              <div class="btn-container">
                <v-btn @click="handleCreateRoom" color="primary" class="mr-2">Create</v-btn>
                <v-btn @click="handleJoinRoom" color="primary" class="mr-2">Join</v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Snackbar for displaying errors -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { createRoom, joinRoom } from '@/services/api';

const roomName = ref('');
const userName = ref('');
const router = useRouter();
const formRef = ref('');

const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(3000);

const roomNameRules = [
  (v) => !!v || 'Room Name is required.',
  (v) => /^[a-zA-Z0-9_]+$/.test(v) || 'Room Name must contain only letters, numbers, and underscores, and no spaces or special characters.'
];
const userNameRules = [
  (v) => !!v || 'User Name is required.'
];

const handleCreateRoom = async () => {
  await handleRoomAction('create');
};

const handleJoinRoom = async () => {
  await handleRoomAction('join');
};

const handleRoomAction = async (action) => {
  const  isValid = await formRef.value.validate();
  if (!isValid.valid) {
    return;
  }
  
  try {
    let room;
    if (action === 'create') {
      room = await createRoom(roomName.value, userName.value);
    } else if (action === 'join') {
      room = await joinRoom(roomName.value, userName.value);
    }

    if (room) {
      router.push({ name: 'room', params: { roomname: room } });
    }
  } catch (error) {
    snackbarText.value = error.message;
    snackbarColor.value = 'error';
    snackbar.value = true;
  }
};
</script>

<style scoped>
.card-content {
  padding: 24px;
  text-align: center;
}

.v-card {
  width: 100%;
  min-height: 400px;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 10px;
}

.v-form {
  padding: 20px;
}

.v-card-title {
  text-align: center;
  margin: 20px;
}

.btn-container {
  display: flex;
  justify-content: flex-end;
}
</style>
