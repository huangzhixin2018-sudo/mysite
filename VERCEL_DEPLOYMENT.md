# Vercel部署Django项目指南

## 🚨 重要修复

**问题已修复！** 现在可以正常部署了。

### 修复内容：
- ✅ 将`mysite/wsgi.py`中的`application`改为`app`
- ✅ 更新`settings.py`中的`WSGI_APPLICATION`配置
- ✅ 添加Vercel部署所需的静态文件配置
- ✅ 删除多余的`vercel_wsgi.py`文件
- ✅ **新增：配置PostgreSQL数据库支持，解决SQLite问题**

## 🗄️ 数据库配置（重要！）

### 问题说明：
Vercel不支持SQLite数据库，因为：
- Vercel是无状态环境，无法持久化文件
- SQLite需要文件系统写入权限
- 每次部署后数据会丢失

### 解决方案：使用PostgreSQL
1. **免费PostgreSQL服务**：
   - [Neon](https://neon.tech) - 免费层可用
   - [Supabase](https://supabase.com) - 免费层可用
   - [PlanetScale](https://planetscale.com) - 免费层可用

2. **获取数据库连接字符串**：
   ```
   postgresql://username:password@host:port/database_name
   ```

## 📋 前置要求

1. **Vercel账户**: 在 [vercel.com](https://vercel.com) 注册账户
2. **Node.js**: 安装Node.js (推荐v16+)
3. **Python**: 确保Python环境正常
4. **PostgreSQL数据库**: 获取免费数据库服务

## 🚀 部署步骤

### 1. 设置PostgreSQL数据库

```bash
# 1. 注册免费PostgreSQL服务（如Neon）
# 2. 获取数据库连接字符串
# 3. 在Vercel Dashboard中设置环境变量
```

### 2. 使用部署脚本 (推荐)

```bash
# 给脚本执行权限
chmod +x deploy-vercel.sh

# 运行部署脚本
./deploy-vercel.sh
```

### 3. 手动部署

```bash
# 1. 安装Vercel CLI
npm install -g vercel

# 2. 登录Vercel
vercel login

# 3. 收集静态文件
python manage.py collectstatic --noinput

# 4. 部署到生产环境
vercel --prod
```

## ⚙️ 配置说明

### 关键文件：
- `mysite/wsgi.py` - 导出`app`变量 ✅
- `vercel.json` - Vercel路由配置 ✅
- `requirements-vercel.txt` - 生产环境依赖 ✅
- `vercel.env` - 环境变量配置 ✅

### 环境变量（在Vercel Dashboard中设置）：
- `DEBUG`: False
- `SECRET_KEY`: 您的Django密钥
- `ALLOWED_HOSTS`: .vercel.app,.now.sh
- `DATABASE_URL`: PostgreSQL连接字符串（重要！）

## 🔧 部署后检查

1. **访问应用**: 检查部署URL是否正常
2. **查看日志**: 在Vercel Dashboard中查看部署日志
3. **测试功能**: 确保主要功能正常工作
4. **数据库连接**: 确保PostgreSQL连接正常

## 🌐 访问应用

部署成功后，您会获得一个类似这样的URL：
```
https://your-project-name.vercel.app
```

## 📝 常见问题

### Q: 部署失败怎么办？
A: 检查Vercel Dashboard的部署日志，确保所有配置正确

### Q: 静态文件无法加载？
A: 确保运行了`python manage.py collectstatic --noinput`

### Q: 数据库连接失败？
A: 确保设置了正确的`DATABASE_URL`环境变量

### Q: SQLite错误？
A: Vercel不支持SQLite，必须使用PostgreSQL或其他云数据库

## 🔄 更新部署

每次推送代码到Git仓库后，Vercel会自动重新部署。

## 🆓 免费PostgreSQL服务推荐

1. **Neon** - 免费层：3GB存储，每月1000万行读取
2. **Supabase** - 免费层：500MB存储，每月2GB带宽
3. **PlanetScale** - 免费层：1GB存储，每月10亿行读取

**现在可以正常部署了！记得配置PostgreSQL数据库！** 🎉
