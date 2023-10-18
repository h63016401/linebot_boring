# linebot_boring
Linebot 無聊機器人拿來測試自己喜歡的東西使用

常用網站:

建立 Messaging API 頻道：https://developers.line.biz/zh-hant/docs/messaging-api/getting-started/

LINE Develpers console：https://developers.line.biz/console/

申請一個 LINE Simple Beacon Hardware ID:https://manager.line.biz/beacon/register

Arduino Esp32 S3「額外的開發板管理員網址」，將 https://dl.espressif.com/dl/package_esp32_index.json 

相關應用可以參考這個:https://hackmd.io/@taichunmin/chatbot-tw-202002?print-pdf#/

## 快速上手

1. 下載專案

    git clone https://github.com/h63016401/linebot_boring.git

    cd linebot_boring

2. 一鍵啟動

    docker-compose up -d

3. 登入管理介面

當docker容器跑起來後， 連接到7200 port

但Line bot需要DNS網址跟HTTPS認證需要處理