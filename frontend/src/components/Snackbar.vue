<template>
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="snackbarTimeout">
      {{ snackbarText }}
    </v-snackbar>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const snackbar = ref(false);
  const snackbarText = ref('');
  const snackbarColor = ref('');
  const snackbarTimeout = ref(3000);
  
  const showSnackbar = (message, color = 'info', timeout = 5000) => {
    snackbarText.value = message;
    snackbarColor.value = color;
    snackbarTimeout.value = timeout;
    snackbar.value = true;
  };
  
  defineExpose({
    showSnackbar,
  });
  </script>