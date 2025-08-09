# Vercel部署Django项目指南

## 📋 前置要求

1. **Vercel账户**: 在 [vercel.com](https://vercel.com) 注册账户
2. **Node.js**: 安装Node.js (推荐v16+)
3. **Git**: 确保项目在Git仓库中

## 🚀 部署步骤

### 方法1: 使用Vercel CLI (推荐)

#### 1. 安装Vercel CLI
```bash
npm install -g vercel
```

#### 2. 登录Vercel
```bash
vercel login
```

#### 3. 部署项目
```bash
# 在项目根目录执行
vercel --prod
```

#### 4. 使用部署脚本
```bash
# 给脚本执行权限
chmod +x deploy-vercel.sh

# 运行部署脚本
./deploy-vercel.sh
```

### 方法2: 通过Vercel Dashboard

1. 访问 [vercel.com/dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 导入您的Git仓库
4. 配置项目设置
5. 点击 "Deploy"

## ⚙️ 配置说明

### vercel.json
- `builds`: 指定构建配置
- `routes`: 配置路由规则
- `env`: 设置环境变量

### 环境变量
在Vercel Dashboard中设置以下环境变量：
- `DEBUG`: False
- `SECRET_KEY`: 您的Django密钥
- `ALLOWED_HOSTS`: .vercel.app,.now.sh
- `DATABASE_URL`: 数据库连接字符串

## 🔧 注意事项

### 1. 数据库限制
- Vercel不支持持久化文件系统
- SQLite数据库在每次部署后会重置
- 建议使用外部数据库服务

### 2. 静态文件
- 静态文件会自动处理
- 确保在settings.py中正确配置STATIC_ROOT

### 3. 依赖包
- 某些包可能不兼容Vercel环境
- 已移除gunicorn、redis、celery等包

## 🌐 访问应用

部署成功后，您会获得一个类似这样的URL：
```
https://your-project-name.vercel.app
```

## 📝 常见问题

### Q: 部署失败怎么办？
A: 检查vercel.json配置和requirements.txt依赖

### Q: 数据库连接失败？
A: 使用外部数据库服务，如PlanetScale、Supabase等

### Q: 静态文件无法加载？
A: 确保STATIC_ROOT配置正确

## 🔄 更新部署

每次推送代码到Git仓库后，Vercel会自动重新部署。

## 📚 更多资源

- [Vercel官方文档](https://vercel.com/docs)
- [Django部署最佳实践](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Vercel Python运行时](https://vercel.com/docs/runtimes#python)
