from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
import subprocess

# Chromeのオプション設定
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('user-data-dir=C:/Users/youzo/AppData/Local/Google/Chrome/User Data/Profile 3')

# ChromeDriverの起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# WebDriverWaitの設定
wait = WebDriverWait(driver, 10)

# 特定のライブ放送ページにアクセス
driver.get('https://live.nicovideo.jp/watch/co5738898')
sleep(3)

# オーディエンストークンの取得
script = """
return JSON.parse(
  document.getElementById("embedded-data").getAttribute("data-props")
).player.audienceToken;
"""
audience_token = driver.execute_script(script)

# WebSocket URLの取得
script = """
return JSON.parse(
  document.getElementById("embedded-data").getAttribute("data-props")
).player.websocketUrl;
"""
websocket_url = driver.execute_script(script)

# データをJSファイルに書き出す
with open('nicolive_comment.js', 'w') as f:
    f.write(f"""
const WebSocket = require('ws');

const ws = new WebSocket('{websocket_url}', 'msg.nicovideo.jp#json', {{
  headers: {{
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
  }},
}});

ws.on('open', function open() {{
  ws.send(JSON.stringify({{ "type": "startWatching", "data": {{ "stream": {{ "quality": "abr", "protocol": "hls", "latency": "low", "audienceToken": "{audience_token}" }}, "room": {{ "protocol": "websocket", "commentable": true }} }}, "id": "0" }}));
  setInterval(() => {{
    ws.send(JSON.stringify({{ "type": "postComment", "data": {{ "text": "わこつ～ｗ", "isAnonymous": false }}, "id": "1" }}));
  }}, 300000);  // 5分毎にコメントを送信
}});

ws.on('message', function incoming(data) {{
  console.log(data);
}});
""")

# ChromeDriverの終了
driver.quit()

# JavaScriptファイルの場所を指定
js_file_path = "nicolive_comment.js"

# Node.jsでJavaScriptファイルを実行するコマンドを指定
command = ["node", js_file_path]

# subprocessを使用してコマンドを実行
subprocess.run(command)
