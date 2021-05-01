"""
７　難易度★★☆☆☆
処理の経過が分かりやすいようにログファイルを出力してみましょう
ログファイルとは：ツールがいつどのように動作したかを後から確認するために重要なテキストファイルです。 
ライブラリを用いることもできますが、テキストファイルを出力する処理で簡単に実現できるので、試してみましょう。 
(今何件目、エラー内容、等を表示)
"""

import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import sys
import pandas as pd
import datetime
import logging


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

    

def main(search_keyword):
    #ログファイルへのロギングの設定
    # mm/dd/yyyy hh:mm:ss message
    now = datetime.datetime.now()
    logfile = 'execution_log_' + search_keyword + "_" + now.strftime('%Y%m%d_%H%M%S') + '.log'
    logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y%H%M%S %I:%M:%S %p')

    driver = set_driver("chromedriver.exe", False)
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
    except:
        #ポップアップがない場合などでエラーになったらエラーにせずパスして後続を処理
        pass

    # 検索窓に検索文字列を入力
    search_keyword = search_keyword
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

        try:
            #～～～～企業内容を取得:start～～～～
            #検索ワードによって.cassetteRecruitRecommend__nameのケースがあるのでこの場合の情報も取り込む
            first_company_data = driver.find_elements_by_css_selector(".cassetteRecruitRecommend__name")
            
            if first_company_data:
                #会社情報に"|"がないケースがあるので分岐処理を入れる
                if "|" in first_company_data[0].text:
                    company_list.append(first_company_data[0].text.split("|")[0])
                else:
                    company_list.append(first_company_data[0].text)


            #.cassetteRecruit__name部分の会社情報を取得
            company_data =  driver.find_elements_by_css_selector(".cassetteRecruit__name")
            
            print(f"{count}ページ目のデータ{len(company_data)}件を検索しています.....")
            logging.info(f"【正常】{count}ページ目のデータ{len(company_data)}件を検索しています.....")
            for company in company_data:
                #会社情報に"|"がないケースがあるので分岐処理を入れる
                if "|" in company.text:
                    company_list.append(company.text.split("|")[0])
                else:
                    company_list.append(company.text)
            #～～～～企業内容を取得:emd～～～～
        except Exception as e:
            print(f"【異常】企業情報の収集でエラーが発生しました。")
            print(f"エラー内容:{e}")
            logging.info(f"企業情報の収集でエラーが発生しました。")
            logging.info('[異常]エラー内容:%s', str(e.args))
            logging.exception('エラー詳細: %s', e)
            
        #勤務地と給与、初年度年収を取得
        try:
            table_list =  driver.find_elements_by_css_selector(".tableCondition")

            for table in table_list:
                work_location_list.append(table.find_elements_by_tag_name("td")[2].text)  #勤務地をリストに追加
                salary_list.append(table.find_elements_by_tag_name("td")[3].text)  #給与をリストに追加
                try:
                    initial_annual_income.append(table.find_elements_by_tag_name("td")[4].text)    #初年度年収をリストに追加
            
                except:
                    initial_annual_income.append("初年度年収のデータなし")   #初年度年収データがない場合その旨をリストに追加
        except Exception as e:
            print(f"勤務地、給与、初年度年収の収集でエラーが発生しました。")
            print(f"エラー内容:{e}")
            logging.info(f"勤務地、給与、初年度年収の収集でエラーが発生しました。")
            logging.info('[異常]エラー内容:%s', str(e.args))
            logging.exception('エラー詳細: %s', e)

        try:
            next_page = driver.find_element_by_class_name("iconFont--arrowLeft")
            next_page_link = next_page.get_attribute("href")
            count += 1
            driver.get(next_page_link)  #次のページへ遷移
            time.sleep(3)
        except:
            print("最終ページまで検索完了")
            logging.info("【正常】最終ページまで検索が完了しました")
            break

    #取得したデータ数のチェック 
    print(f"company_list:{len(company_list)}")
    print(f"work_location_list:{len( work_location_list)}")
    print(f"salary_list:{len(salary_list)}")
    print(f"initial_annual_income:{len(initial_annual_income)}")

    #リストデータをDataframeに変換
    logging.info("【正常】CSVファイルへの書き込み処理を開始します。")
    df = pd.DataFrame(
        {"企業名":company_list, 
        "勤務地": work_location_list, 
        "給与": salary_list, 
        "初年度年収": initial_annual_income
        })
    #csv保存
    now = datetime.datetime.now()
    filename = 'result_' + search_keyword + "_" + now.strftime('%Y%m%d_%H%M%S') + '.csv'
    try:
        df.to_csv(filename, encoding="utf-8-sig", index=None)
        logging.info("【正常】CSVへの書き込み処理が正常終了しました。")
    except Exception as e:
        logging.info("【異常】CSVへの書き込み処理が異常終了しました。")
        logging.info('[異常]エラー内容:%s', str(e.args))
        logging.exception('エラー詳細: %s', e)
 
    driver.quit()
    logging.info("【正常】処理が終了しました。")


if __name__ == "__main__":
    #コマンドの引数を取得
    args = sys.argv
    if len(args) > 2 or ( 0 < len(args) < 2):
        print("検索ワードを引数に指定してください\n検索ワードは1つのみ指定してください")
        exit()
    else:
        #検索ワードを取得
        search_keyword = sys.argv[1]
        main(search_keyword)