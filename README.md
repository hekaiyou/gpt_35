# GPT-3.5 AI小助手

使用 Python Web 作为后端框架, MongoDB 作为数据库, 以及 OpenAI 的 gpt-3.5 模型 API 作为核心服务, 让你可以通过浏览器与一个强大的自然语言生成模型进行交互。

## 📦 安装

1. 下载 [we-fast-api](https://github.com/hekaiyou/we-fast-api) 框架代码, 在终端执行:
   ```shell
   git clone https://github.com/hekaiyou/we-fast-api.git
   ```
2. 先安装 [we-fast-api](https://github.com/hekaiyou/we-fast-api) 框架依赖, 在终端执行:
   ```
   pip install -r requirements.txt
   ```
3. 进入到 `we-fast-api/apis` 目录下, 下载 [gpt_35](https://github.com/hekaiyou/gpt_35) 模块代码, 在终端执行:
   ```shell
   cd we-fast-api/apis
   git clone https://github.com/hekaiyou/gpt_35.git
   ```
4. 再安装 [gpt_35](https://github.com/hekaiyou/gpt_35) 模块依赖, 同样在终端执行:
   ```
   pip install -r requirements.txt
   ```

## ⚙️ 应用配置

| 应用模块 | 配置文件路径 | 环境变量描述 |
| ------- | ------- | ------- |
| core | `.env` | MongoDB 连接等关键配置 (应用运行不可缺少的环境变量) |
| bases | `apis/bases/.env`   | [we-fast-api](https://github.com/hekaiyou/we-fast-api) 框架的基础配置 |
| gpt_35 | `apis/gpt_35/.env` | [gpt_35](https://github.com/hekaiyou/gpt_35) 模块的运行配置 |
