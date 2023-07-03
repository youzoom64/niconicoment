from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chromeのオプション設定
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # GPUを無効にする
options.add_argument("--user-data-dir=C:\\Users\\youzo\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")  # 特定のプロフィールを使用

# ChromeDriverの起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ニコニコ動画のログインページにアクセス
driver.get('https://account.nicovideo.jp/login/')

# WebDriverWaitのインスタンス生成
wait = WebDriverWait(driver, 10)  # 最大で10秒間待つように設定

# 特定のライブ放送ページにアクセス
driver.get('https://live.nicovideo.jp/watch/co5738898')
sleep(3)  # ページ読み込み待ち

# オーディエンストークンの取得
script = """
return JSON.parse(
  document.getElementById("embedded-data").getAttribute("data-props")
).player.audienceToken;
"""
audience_token = driver.execute_script(script)

print(audience_token)  # 取得したオーディエンストークンを出力

# ChromeDriverの終了
driver.quit()
