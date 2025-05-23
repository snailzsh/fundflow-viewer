# 行业板块资金净流入排行榜

这是一个基于Flask的Web应用，用于展示行业板块资金净流入排行榜数据。

## 功能特点

- 展示今日、5日、10日行业板块资金净流入排行
- 支持按各种指标排序
- 支持搜索筛选
- 支持自动刷新数据
- 支持导出Excel和CSV格式

## 部署指南

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 本地运行

```bash
python app.py
```

### 3. 生产环境部署

#### 使用Gunicorn (Linux/macOS)

```bash
pip install gunicorn
gunicorn wsgi:app
```

#### 使用Waitress (Windows)

```bash
pip install waitress
waitress-serve --port=8000 wsgi:app
```

#### 使用Docker

1. 创建Dockerfile:

```
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
```

2. 构建并运行Docker镜像:

```bash
docker build -t fund-flow-rank .
docker run -p 8000:8000 fund-flow-rank
```

#### 使用云平台部署

1. **Heroku**:
   - 安装Heroku CLI
   - 登录: `heroku login`
   - 创建应用: `heroku create fund-flow-rank`
   - 推送代码: `git push heroku main`

2. **阿里云/腾讯云等**:
   - 创建云服务器实例
   - 安装Python环境
   - 上传代码并安装依赖
   - 使用Gunicorn或Waitress运行应用
   - 配置Nginx作为反向代理

## 注意事项

- 生产环境中请关闭debug模式
- 建议使用反向代理(如Nginx)提供静态文件服务
- 定期检查数据源是否可用 