<template>
    <a class="username" href="https://yushanwang9801.github.io" target="_blank" rel="noopener noreferrer">
    For more project ideas please visit my personal website: 
    <span class="username-text">YushanWang9801</span>
    <span class="username-icon">→</span>
  </a>
  <GameBoard />
</template>

<script>
import GameBoard from './components/GameBoard.vue'

export default {
  name: 'App',
  components: {
    GameBoard
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 20px;
  background-color: #faf8ef;
}

.username {
  color: #00a19c;
}
</style>