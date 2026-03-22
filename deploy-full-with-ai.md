# 哈利波特魔法工坊 - 完整AI功能部署指南

## 项目特点：
- ✅ **真正的AI功能**：使用OpenAI GPT-4、Whisper、DALL-E
- ✅ **优雅降级**：无API密钥时使用演示模式
- ✅ **全栈应用**：Vue前端 + Python后端
- ✅ **数据持久化**：JSON文件存储用户数据

## 部署前准备：

### 1. 获取AI API密钥
**必需**：
- [OpenAI API Key](https://platform.openai.com/api-keys) - 用于所有对话和生成功能

**可选**：
- [Anthropic Claude API Key](https://console.anthropic.com) - 备用AI服务
- [Pinecone API Key](https://www.pinecone.io) - 向量数据库（高级功能）

### 2. 准备环境变量
创建 `backend/.env` 文件：
```env
# OpenAI API Key（必需）
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic API Key（可选）
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Pinecone API Key（可选）
PINECONE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PINECONE_ENVIRONMENT=gcp-starter

# Flask配置
PORT=5000
DEBUG=False
```

## 部署方案选择：

### 方案一：CloudBase部署（推荐，你已连接）
**优点**：一体化管理，适合腾讯云生态

**步骤**：
1. **前端部署**：静态网站托管
2. **后端部署**：云函数（Python 3.11）
3. **环境变量**：在CloudBase控制台配置
4. **数据库**：使用CloudBase NoSQL数据库

### 方案二：Vercel全栈部署
**优点**：免费额度充足，全球CDN

**步骤**：
1. 创建 `api/` 文件夹，将backend内容放入
2. 创建 `vercel.json` 配置路由
3. 在Vercel控制台配置环境变量
4. 连接GitHub仓库自动部署

### 方案三：Railway/Heroku部署
**优点**：简单，专注后端部署

**步骤**：
1. 后端部署到Railway/Heroku
2. 前端部署到Vercel/Netlify
3. 配置CORS和API地址

## 详细部署步骤（以方案一：CloudBase为例）：

### 步骤1：检查CloudBase环境



<｜DSML｜function_calls>
<｜DSML｜invoke name="invoke_integration">
<｜DSML｜parameter