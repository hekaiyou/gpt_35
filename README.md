# GPT-3.5 AI小助手

使用 Python Web 作为后端框架, MongoDB 作为数据库, 以及 OpenAI 的 gpt-3.5 模型 API 作为核心服务, 让你可以通过浏览器与一个强大的自然语言生成模型进行交互。

## 📦 安装

### 前置依赖

- 开发语言: Python >= 3.7
- 数据库: MongoDB >= 4.0

### 操作步骤

1. 下载 [we-fast-api](https://github.com/hekaiyou/we-fast-api) 框架代码, 在终端执行:
   ```shell
   git clone https://github.com/hekaiyou/we-fast-api.git
   ```
2. 创建 Python3 版本的虚拟环境, 在终端执行:
   ```shell
   cd we-fast-api
   python3 -m venv venv
   source venv/bin/activate
   ```
3. 先安装 [we-fast-api](https://github.com/hekaiyou/we-fast-api) 框架依赖, 在终端执行:
   ```shell
   pip install -r requirements.txt
   ```
4. 进入到 `we-fast-api/apis` 目录下, 下载 [gpt_35](https://github.com/hekaiyou/gpt_35) 模块代码, 在终端执行:
   ```shell
   cd apis
   git clone https://github.com/hekaiyou/gpt_35.git
   ```
5. 再安装 [gpt_35](https://github.com/hekaiyou/gpt_35) 模块依赖, 同样在终端执行:
   ```shell
   pip install -r requirements.txt
   ```

## ⚙️ 配置

环境变量读取的优先级排序, 有同名环境变量时, 取优先级高的变量值:

1. 系统环境变量
2. **.env** 文件 (用这个比较方便)
3. 环境变量默认值

| 应用模块 | 配置文件路径 | 描述 |
| ------- | ------- | ------- |
| core | `.env` | MongoDB 连接等关键配置 (应用运行不可缺少的环境变量) |
| bases | `apis/bases/.env` | [we-fast-api](https://github.com/hekaiyou/we-fast-api) 框架的基础环境变量 |
| gpt_35 | `apis/gpt_35/.env` | [gpt_35](https://github.com/hekaiyou/gpt_35) 模块的运行环境变量 |

### .env

在框架根路径下创建 `.env` 配置文件, 参考以下内容设置具体的环境变量:

```bash
MONGO_DB_HOST=127.0.0.1
MONGO_DB_PORT=27017
MONGO_DB_NAME=ai_speedup
```

该目录下支持的全部环境变量参数如下:

| 环境变量 | 描述 | 类型 | 默认值 |
| ------- | ------- | ------- | ------- |
| MONGO_DB_HOST | MongoDB 连接地址 | str | 127.0.0.1 |
| MONGO_DB_PORT | MongoDB 连接端口 | int | 27017 |
| MONGO_DB_NAME | MongoDB 连接数据库 | str | test_database |
| MONGO_DB_USERNAME | MongoDB 连接认证用户 | str |  |
| MONGO_DB_PASSWORD | MongoDB 连接认证密码 | str |  |
| USER_DEFAULT_PERMISSION | 用户未分配角色时的默认权限 | list | [] |
| TOKEN_SECRET_KEY | 令牌的密钥 (生产建议使用 `openssl rand -hex 32` 生成新密钥) | str |  |

*根据数据库是否开启权限管理, 选择性使用 `MONGO_DB_USERNAME` 和 `MONGO_DB_PASSWORD` 变量配置数据库认证信息。*

### apis/bases/.env

在 `apis/bases/` 路径下创建 `.env` 配置文件, 参考以下内容设置具体的环境变量:

```bash
APP_NAME=AI小助手
APP_VERSION=1.0.0
APP_HOST=http://127.0.0.1:8083/
TOKEN_EXPIRE_MINUTE=10080
```

该目录下支持的全部环境变量参数如下:

| 环境变量 | 描述 | 类型 | 默认值 |
| ------- | ------- | ------- | ------- |
| APP_NAME | 服务的标题 | str | WeFastAPI |
| APP_VERSION | 服务的版本号, 通常按照 `A.B.C`(*大版本.新功能发布.小更新*) 规则 | str | 0.0.1 |
| APP_HOST | 服务的地址 | str | http://127.0.0.1:8083/ |
| APP_HOME_PATH | 服务的主页路径 | str | /view/bases/home/ |
| APP_WORKERS_NUM | 服务的工作进程总数 (workers) | int | 1 |
| APP_DOCS | 服务的 Swagger 文档 (生产建议关闭) | bool | True |
| APP_REDOC | 服务的 ReDoc 文档 (生产建议关闭) | bool | True |
| UVICORN_HOST | 单 Uvicorn 监听地址 | str | 0.0.0.0 |
| UVICORN_PORT | 单 Uvicorn 监听端口 | int | 8083 |
| UVICORN_WORKERS | 单 Uvicorn 工作进程 | int | 1 |
| UVICORN_RELOAD | 单 Uvicorn 代码变更重新加载 | bool | False |
| TOKEN_EXPIRE_MINUTE | 令牌的有效时间 (分钟) | int | 720 |
| TOKEN_EXEMPT_IP | 令牌豁免 IP 网络列表 (前面3段) | list | [] |
| TOKEN_EXEMPT_HOST | 令牌豁免 IP 主机列表 (完整4段) | list | [] |
| MAIL_SMTP_HOST | 邮件 SMTP 服务器地址 | str | smtp.163.com |
| MAIL_SMTP_PORT | 邮件 SMTP 服务器端口 | int | 465 |
| MAIL_SMTP_USE_SSL | 邮件 SMTP 使用 SSL 加密 | bool | True |
| MAIL_SMTP_SENDER_NAME | 邮件 SMTP 发件人名称 | str | fromXX |
| MAIL_SMTP_SENDER | 邮件 SMTP 发件人邮箱 | str | from@163.com |
| MAIL_SMTP_PASSWORD | 邮件 SMTP 授权码 | str |  |
| ENABLE_LDAP_AD | 启用 LDAP/AD 认证 | bool | False |
| LDAP_AD_HOST | LDAP/AD 服务器地址 | str | 127.0.0.1 |
| LDAP_AD_BIND_DN | LDAP/AD 绑定用户的 DN | str | Example\\zhangsan |
| LDAP_AD_PASSWORD | LDAP/AD 绑定用户的密码 | str |  |
| LDAP_AD_SEARCH_BASE | LDAP/AD 搜索用户的基础路径 | str | OU=OU,DC=Example,DC=LOCAL |
| LDAP_AD_SEARCH_FILTER | LDAP/AD 搜索用户的过滤器 | str | (sAMAccountName={}) |
| LDAP_AD_EMAIL_SUFFIX | LDAP/AD 企业邮箱后缀 | str | @example.com |
| ENABLE_WECHAT_APP | 启用微信小程序支持 | bool | False |
| WECHAT_APP_ID | 微信小程序唯一标识 | str | wxa123456 |
| WECHAT_APP_SECRET | 微信小程序密钥 | str |  |

### apis/gpt_35/.env

在 `apis/gpt_35/` 路径下创建 `.env` 配置文件, 参考以下内容设置具体的环境变量:

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

该目录下支持的全部环境变量参数如下:

| 环境变量 | 描述 | 类型 | 默认值 |
| ------- | ------- | ------- | ------- |
| OPENAI_API_KEY | OpenAI API key | str |  |

## ✨ 启动

## 👀 预览

RUN pip install -r apis/gpt_35/requirements.txt

docker build -t ai-speedup:latest .

docker run -t -i -v /home/lighthouse/code/we-fast-api/files:/workspace/files -v /home/lighthouse/code/we-fast-api/logs:/workspace/logs -p 8089:8083 --env-file .env --env-file apis/bases/.env --env-file apis/gpt_35/.env ai-speedup:latest

docker run -t -i -d -v /home/lighthouse/code/we-fast-api/files:/workspace/files -v /home/lighthouse/code/we-fast-api/logs:/workspace/logs -p 8089:8083 --env-file .env --env-file apis/bases/.env --env-file apis/gpt_35/.env ai-speedup:latest


# A.B.C 大版本.新功能更新.小修改
docker build -t ai-speedup:0.0.2 .

docker run -t -i -d -v /home/lighthouse/code/we-fast-api/files:/workspace/files -p 8089:8083 --env-file .env --env-file apis/bases/.env --env-file apis/gpt_35/.env ai-speedup:0.0.2



lsof -i:8083
sudo kill -9 $(lsof -i:8083 -t)

bj&QDx%W_&S1CClg
