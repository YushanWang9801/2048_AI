import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  base: '/2048_AI/', // 替换为你的仓库名
  plugins: [vue()] // 或 vue()
});
