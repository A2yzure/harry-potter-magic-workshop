# 哈利波特魔法工坊 - AI 互动体验平台

基于《哈利波特》系列电影官方授权素材，结合当前成熟的 AI 技术，为粉丝打造沉浸式魔法世界互动体验。

## 🎯 项目特点

- **魔杖个性定制**：AI 分析性格生成专属魔杖
- **霍格沃茨分院测试**：与分院帽对话，找到学院归属
- **魔法咒语学习**：语音识别，练习咒语发音
- **角色互动对话**：与邓布利多、斯内普等角色深入交流
- **谜题闯关游戏**：挑战经典谜题，测试魔法智慧

## 🛠️ 技术栈

### 前端
- Vue 3 + Composition API
- TDesign Vue Next 组件库
- Tailwind CSS
- Vue Router + Pinia

### 后端
- Python Flask
- OpenAI API (GPT-4o-mini, Whisper, DALL-E)
- Anthropic Claude API (可选)
- JSON 文件存储

## 📦 安装与运行

### 前端

```bash
cd harry-potter
npm install
npm run dev
```

访问：http://localhost:3000

### 后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
python app_updated.py
```

访问：http://localhost:5000

## 🔑 环境变量配置

在 `backend/.env` 文件中配置：

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
PORT=5000
DEBUG=True
```

## 📁 项目结构

```
harry-potter/
├── src/
│   ├── views/           # 页面组件
│   ├── stores/          # Pinia 状态管理
│   ├── router/          # 路由配置
│   ├── App.vue          # 主应用组件
│   └── main.ts          # 入口文件
├── backend/
│   ├── app.py           # Flask API (基础版)
│   ├── app_updated.py   # Flask API (完整版)
│   ├── ai_services.py   # AI 服务集成
│   ├── database.py      # 数据持久化
│   ├── requirements.txt # Python 依赖
│   └── .env.example     # 环境变量模板
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

## 🎨 核心功能

### 1. 魔杖个性定制

通过性格测试问答，AI 生成专属魔杖：
- 木材类型：冬青木、山毛榉木、橡木、紫杉木等
- 杖芯：凤凰羽毛、龙神经、独角兽毛、雷鸟尾羽
- 长度与弹性：基于答案自动计算

### 2. 霍格沃茨分院测试

与分院帽多轮对话，最终分配学院：
- 格兰芬多：勇敢、无畏
- 斯莱特林：野心、智慧
- 拉文克劳：智慧、才智
- 赫奇帕奇：忠诚、勤劳

### 3. 魔法咒语学习

语音识别技术，练习咒语发音：
- 荧光闪烁 (Lumos)
- 缴械咒 (Expelliarmus)
- 昏迷咒 (Stupefy)
- 护盾咒 (Protego)
- 漂浮咒 (Wingardium Leviosa)
- 召唤咒 (Accio)

### 4. 角色互动对话

基于 RAG 架构的角色对话：
- 阿白思·邓布利多
- 西弗勒斯·斯内普
- 赫敏·格兰杰
- 伏地魔

### 5. 谜题闯关游戏

7 个经典谜题关卡：
- 三头犬的谜题
- 飞马谜题
- 魔药谜题
- 镜子谜题
- 时间谜题
- 死亡圣器谜题
- 爱的谜题

## 🌐 部署

### 前端部署

```bash
npm run build
# 将 dist 目录部署到静态服务器
```

### 后端部署

使用 Docker 部署：

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
EXPOSE 5000
CMD ["python", "app_updated.py"]
```

## 📄 版权声明

本项目仅用于学习和演示目的。所有《哈利波特》相关素材版权归 Warner Bros. 所有。

如需用于商业用途，请获取官方授权。

## 📄 API 文档

### 用户相关

- `GET /api/user?userId=xxx` - 获取用户数据
- `POST /api/user` - 创建用户
- `PUT /api/user?userId=xxx` - 更新用户数据

### 魔杖相关

- `POST /api/wand/generate` - 生成魔杖
- `POST /api/wand/save` - 保存魔杖

### 分院相关

- `POST /api/sorting/chat` - 分院帽对话

### 咒语相关

- `POST /api/spells/unlock` - 解锁咒语
- `POST /api/spells/recognize` - 识别咒语发音

### 角色相关

- `POST /api/characters/chat` - 角色对话

### 谜题相关

- `POST /api/puzzles/check` - 检查谜题答案
- `POST /api/puzzles/progress` - 更新谜题进度

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题，请提交 Issue。

---

**魔法工坊 - 让魔法触手可及** ✨
