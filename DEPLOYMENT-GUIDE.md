# 哈利波特魔法工坊 - 完整部署指南

## 📋 项目概述
这是一个完整的全栈AI应用，包含：
- **Vue 3前端**：交互式魔法工坊界面
- **Python Flask后端**：提供API服务
- **OpenAI集成**：真正的AI功能（GPT-4、Whisper）
- **演示模式**：无API密钥时自动降级

## 🔑 必需准备

### 1. AI API密钥
- **OpenAI API Key**：https://platform.openai.com/api-keys
- **费用**：约$0.01-0.10/次调用

### 2. 部署平台账户
选择其一：
- **CloudBase**：已连接，推荐
- **Vercel**：免费，全球CDN
- **Railway**：简单易用

## 🚀 部署方案

### 方案A：CloudBase全栈部署（一体化）
**适合**：想要一体化管理的用户

**步骤**：
1. **前端部署**：
   - 构建：`npm run build`
   - 上传 `dist/` 到CloudBase静态托管

2. **后端部署**：
   - 将 `backend/` 部署为云函数
   - 配置环境变量（API密钥）

3. **连接前后端**：
   - 前端API地址指向云函数URL

### 方案B：Vercel全栈部署（免费）
**适合**：预算有限，需要免费方案

**步骤**：
1. **创建Vercel项目**
2. **配置serverless函数**：
   - 创建 `api/` 文件夹
   - 复制backend内容到 `api/`
   - 添加 `vercel.json` 配置路由

3. **部署**：
   - Vercel自动检测并部署
   - 在控制台配置环境变量

### 方案C：分离部署（前端Vercel + 后端Railway）
**适合**：灵活控制，各取所长

**步骤**：
1. **后端部署到Railway**：
   - 上传 `backend/` 文件夹
   - 配置环境变量
   - 获得后端URL：`https://your-backend.up.railway.app`

2. **前端部署到Vercel**：
   - 修改前端API地址为后端URL
   - 部署前端

## 📝 详细配置

### 1. 环境变量配置
创建 `backend/.env` 文件：
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PORT=5000
DEBUG=False
```

### 2. 前端配置修改
修改 `vite.config.ts` 中的API地址：
```javascript
// 生产环境
const apiUrl = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend-url.com' 
  : 'http://localhost:5000';
```

### 3. CORS配置
确保后端允许前端域名访问：
```python
# 在app.py中
CORS(app, origins=["https://your-frontend-domain.com"])
```

## 💰 成本估算

### 免费方案：
- **Vercel**：每月100GB带宽，1000小时函数运行
- **Railway**：每月$5免费额度（约500次API调用）
- **OpenAI**：新用户有$5免费额度

### 付费方案（每月）：
- **OpenAI API**：$10-50（取决于使用量）
- **Vercel Pro**：$20（无限带宽）
- **Railway**：$5-20（按使用量）

## 🛠️ 快速开始（推荐CloudBase）

### 步骤1：构建前端
```bash
cd d:/PythonProject/txtest/harry-potter
npm install
npm run build
```

### 步骤2：准备后端
```bash
cd backend
# 创建.env文件并填入API密钥
```

### 步骤3：部署到CloudBase
1. 在CloudBase控制台创建新环境
2. 上传前端 `dist/` 文件夹到静态托管
3. 上传后端 `backend/` 文件夹到云函数
4. 配置环境变量

### 步骤4：测试
访问CloudBase提供的URL，测试AI功能！

## 📞 技术支持

### 常见问题：
1. **API调用失败**：检查API密钥和余额
2. **CORS错误**：检查后端CORS配置
3. **部署失败**：检查日志，通常为依赖问题

### 获取帮助：
- 查看项目README
- 检查控制台日志
- 联系平台技术支持

## 🎉 完成！
部署完成后，你将获得：
- 一个可分享的网站链接
- 真正的AI魔法体验
- 用户数据持久化
- 长期有效的在线服务

**分享链接示例**：
```
https://harry-potter-magic.vercel.app
或
https://your-domain.tcloudbaseapp.com
```

祝你魔法工坊部署成功！✨