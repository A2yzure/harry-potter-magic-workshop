import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  base: '/harry-potter-magic-workshop/', // 部署到GitHub Pages子路径
  server: {
    port: 3000
    // 移除代理配置，纯静态部署不需要连接后端
  }
})
