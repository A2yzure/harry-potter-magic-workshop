#!/bin/bash

echo "🚀 开始部署哈利波特魔法工坊演示版..."

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 请先安装Node.js: https://nodejs.org"
    exit 1
fi

echo "📦 安装依赖..."
npm install

echo "🔧 构建项目..."
npm run build

echo "✅ 构建完成！dist文件夹已生成"

echo ""
echo "📝 部署选项："
echo "1. GitHub Pages (免费、长期有效)"
echo "2. Vercel (免费、CDN加速)"
echo "3. Netlify (免费、简单)"
echo "4. Cloudflare Pages (免费、快速)"
echo ""
echo "📁 你的静态文件在: dist/"
echo "📄 主页面: dist/index.html"
echo ""

echo "🎯 推荐使用 GitHub Pages："
echo "1. 创建GitHub仓库: https://github.com/new"
echo "2. 仓库名: harry-potter-magic-demo"
echo "3. 上传dist文件夹内容"
echo "4. 设置 -> Pages -> 选择main分支"
echo ""
echo "🌐 部署后访问: https://你的用户名.github.io/harry-potter-magic-demo/"
echo ""
echo "✨ 部署完成！分享链接给朋友吧！"