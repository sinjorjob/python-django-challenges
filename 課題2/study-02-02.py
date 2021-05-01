"""
課題２　難易度★★★☆☆
for文を使って、１ページ内の全ての情報を取得できるように改造してみましょう
"""

import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import sys


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

    

def main():
    driver = set_driver("chromedriver.exe", False)
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    
    # 検索窓に入力
    search_keyword = "高収入"
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    #企業内容を取得
    company_list =[]
    company_data =  driver.find_elements_by_css_selector(".cassetteRecruit__name")
    for company in company_data:
        #会社名は「|」で分割後の要素0を取得
        company_list.append(company.text.split("|")[0])
    #勤務地と給与、初年度年収を取得(table要素内に格納されている)
    table_list =  driver.find_elements_by_css_selector(".tableCondition")

    work_location_list = []
    salary_list = []
    initial_annual_income =[]
    for table in table_list:
        work_location_list.append(table.find_elements_by_tag_name("td")[2].text)  #勤務地を取得
        salary_list.append(table.find_elements_by_tag_name("td")[3].text)  #給与を取得
        #初年度年収はデータがない場合があるので例外処理で回避
        try:
            initial_annual_income.append(table.find_elements_by_tag_name("td")[4].text) #初年度年収を取得
        except:
            initial_annual_income.append("初年度年収のデータなし")   #初年度年収データがない場合その旨をリストに追加
    

    #取得結果を表示
    for company, location, salary, income in zip(company_list, work_location_list, salary_list, initial_annual_income):
        print(f"会社名:{company}\n勤務地：{location}\n給与：{salary}\n初年度年収：{income}\n")
        print("="*110)
    #seleniumの終了
    driver.quit()


if __name__ == "__main__":
    
    main()