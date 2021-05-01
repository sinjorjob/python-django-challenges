"""
３　難易度★★★☆☆
２ページ目以降の情報も含めて取得できるようにしてみましょう

～～～ 実行結果例～～～

1ページ目のデータ50件を検索しています.....
2ページ目のデータ50件を検索しています.....
3ページ目のデータ50件を検索しています.....
4ページ目のデータ50件を検索しています.....
5ページ目のデータ50件を検索しています.....
6ページ目のデータ50件を検索しています.....
7ページ目のデータ50件を検索しています.....
8ページ目のデータ50件を検索しています.....
9ページ目のデータ50件を検索しています.....
10ページ目のデータ50件を検索しています.....
11ページ目のデータ50件を検索しています.....
12ページ目のデータ27件を検索しています.....
最終ページまで検索完了
company_list:577
work_location_list:577
salary_list:577
initial_annual_income:577

会社名:株式会社アール・エム
勤務地：《希望以外の転勤なし／UIターン歓迎》 大阪・東京・福岡・名古屋の各拠点のいずれかに配属します。…
給与：月給25万円＋インセンティブからスタート ※固定残業代5万5900円(40時間分)含む。時間超過分は追加支給…
初年度年収：400万円～700万円

==============================================================================================================
会社名:株式会社ジーアフター
勤務地：《駅チカ「西船橋駅」より徒歩5分》 千葉県船橋市葛飾町2-380-5 第2ヤマゲンビル3階
給与：月給26万5000円〜 ※経験や年齢、スキル等を考慮の上、当社規定により決定致します ※上記の月給には時…
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
    
    
    count = 1   #ページ数カウント用
    company_list =[]    #会社名の格納先
    work_location_list = []   #勤務地の格納先
    salary_list = []    #給与の格納先
    initial_annual_income =[]   #初年度年収の格納先


    #次ページが存在する限りループ
    while True:
        #企業内容を取得
        #会社名は　i.text.split(" | " )[0]　　で取得
        company_data =  driver.find_elements_by_css_selector(".cassetteRecruit__name")
        print(f"{count}ページ目のデータ{len(company_data)}件を検索しています.....")
        for company in company_data:
            company_list.append(company.text.split("|")[0])

        #勤務地と給与、初年度年収を取得
        table_list =  driver.find_elements_by_css_selector(".tableCondition")

        for table in table_list:
            work_location_list.append(table.find_elements_by_tag_name("td")[2].text)  #勤務地をリストに追加
            salary_list.append(table.find_elements_by_tag_name("td")[3].text)  #給与をリストに追加
            try:
                initial_annual_income.append(table.find_elements_by_tag_name("td")[4].text)    #初年度年収をリストに追加
        
            except:
                initial_annual_income.append("初年度年収のデータなし")   #初年度年収データがない場合その旨をリストに追加

        try:
            next_page = driver.find_element_by_class_name("iconFont--arrowLeft")
            next_page_link = next_page.get_attribute("href")
            driver.get(next_page_link)  #次のページへ遷移
            count += 1
            time.sleep(3)
        except:
            print("最終ページまで検索完了")
            break

    #取得したデータ数のチェック 
    print(f"company_list:{len(company_list)}")
    print(f"work_location_list:{len( work_location_list)}")
    print(f"salary_list:{len(salary_list)}")
    print(f"initial_annual_income:{len(initial_annual_income)}")


    #最初の10件だけ表示
    for i, (company, location, salary, income) in enumerate(zip(company_list, work_location_list, salary_list, initial_annual_income)):
        if i < 10:
            print(f"会社名:{company}\n勤務地：{location}\n給与：{salary}\n初年度年収：{income}\n")
            print("="*110)
    driver.quit()

if __name__ == "__main__":
    
    main()