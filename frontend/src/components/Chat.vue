<template>
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
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const props = defineProps(['userName', 'socket']);
  
  const chatMessages = ref([]);
  const chatInput = ref('');
  
  const sendChatMessage = () => {
    if (chatInput.value.trim() !== '') {
      const message = {
        user: props.userName,
        text: chatInput.value.trim(),
      };
      props.socket.send(JSON.stringify({
        type: 'chat',
        message: message,
      }));
      chatInput.value = '';
    }
  };
  
  const addMessage = (message) => {
    chatMessages.value.push(message);
  };
  
  const addSystemMessage = (message) => {
    chatMessages.value.push({
      user: 'System',
      text: message,
      isSystem: true,
    });
  };
  
  defineExpose({
    addMessage,
    addSystemMessage,
  });
  </script>
  
  <style scoped>
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