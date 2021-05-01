"""
１　難易度★★☆☆☆
会社名を取得して画面にprint文で表示してみましょう。
"""

import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import sys


# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)


# main処理
def main():

    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    
    # 検索窓に入力
    search_keyword = "高収入"
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
    first_company_name = name_list[0].text.split("|")[0]
    print("1番目の会社名は【{}】です。".format(first_company_name))
    #seleniumの終了
    driver.quit()
        


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    
    main()
