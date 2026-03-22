# 哈利波特魔法工坊部署指南

## 方案一：GitHub Pages（最简单、免费、长期有效）

### 步骤1：创建GitHub仓库
1. 访问 https://github.com/new
2. 仓库名：`harry-potter-magic-workshop`
3. 设置为公开仓库
4. 点击创建

### 步骤2：上传代码到GitHub
在项目目录中运行：

```bash
# 1. 初始化git
git init
git add .
git commit -m "Initial commit"

# 2. 连接到GitHub仓库
git remote add origin https://github.com/你的用户名/harry-potter-magic-workshop.git

# 3. 推送代码
git branch -M main
git push -u origin main
```

### 步骤3：启用GitHub Pages
1. 进入仓库页面 → Settings → Pages
2. Source选择：**Deploy from a branch**
3. Branch选择：`main`，文件夹选择：`/(root)`
4. 点击Save

等待几分钟，访问：`https://你的用户名.github.io/harry-potter-magic-workshop/`

## 方案二：Vercel（更专业、CDN加速）

### 步骤1：部署到Vercel
1. 访问 https://vercel.com
2. 用GitHub账号登录
3. 点击"New Project"
4. 导入你的GitHub仓库
5. Vercel会自动检测Vue项目并配置
6. 点击"Deploy"

部署完成后获得链接：`https://harry-potter-magic-workshop.vercel.app`

## 方案三：Netlify（同样简单免费）

### 步骤1：部署到Netlify
1. 访问 https://app.netlify.com
2. 拖拽 `dist` 文件夹到上传区域
3. 或连接GitHub仓库自动部署

获得链接：`https://随机名称.netlify.app`

## 网站特点：
- ✅ 纯静态网站，无需服务器
- ✅ 演示模式：所有AI功能使用本地模拟数据
- ✅ 长期有效（只要平台存在）
- ✅ 全球CDN加速
- ✅ 自动HTTPS
- ✅ 完全免费

## 分享链接格式：
将部署后的链接分享给朋友：
```
https://你的用户名.github.io/harry-potter-magic-workshop/
或
https://harry-potter-magic-workshop.vercel.app
```

## 注意事项：
1. **AI功能是演示模式**：使用本地模拟数据，不是真正的AI
2. **所有数据存储在浏览器本地**：清空浏览器缓存会丢失数据
3. **完全免费**：这些平台对个人项目免费
4. **长期有效**：只要你不删除仓库，链接一直有效