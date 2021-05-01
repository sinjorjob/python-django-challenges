#!/usr/bin/env python
# coding: utf-8

# # スクレイピング基礎

# In[1]:


get_ipython().system('pip install selenium')


# In[2]:


pip install beautifulsoup4


# In[1]:


from selenium import webdriver
import time
import pandas as pd
import os
import datetime


# In[2]:


USER = "test_user"
PASS = "test_pw"


# In[8]:


#Google Chromeを起動
browser = webdriver.Chrome(executable_path = "chromedriver.exe")
#ドライバが見つかるまでの待ち時間を指定
browser.implicitly_wait(3)


# In[9]:


url_login = "https://kino-code.work/membership-login/"
browser.get(url_login)  #指定URLへ遷移する。
time.sleep(3)
print("ログオンページにアクセスしました。")


# ### 要素はChrome⇒検証⇒Select an elementボタンを押して要素のコードをチェック

# In[11]:


#ログオン画面のユーザ名、パスワード欄に自動入力
element = browser.find_element_by_id("swpm_user_name")
element.clear()   #フォームにデフォルト値として値が設定されてる場合があるので一旦クリア
element.send_keys(USER)
element = browser.find_element_by_id("swpm_password")
element.clear()
element.send_keys(PASS)
print("フォームを送信")


# In[12]:


#入力したデータを送信
browser_form = browser.find_element_by_name('swpm-login')   #name属性で検索
time.sleep(3)
browser_form.click()
print("情報を入力してログオンボタンを押しました")


# In[13]:


#ログオン後にアクセス可能なURLへ遷移
url = "https://kino-code.work/member-only/"
time.sleep(3)
browser.get(url)
print(url, ":アクセス完了")


# In[14]:


#ダウンロードボタンをクリック
"""
IDやnameなどの属性がない場合の指定方法
find_element_by_xpathメソッドを使う。
要素は対象の要素を選択した状態⇒右クリック⇒コピー⇒Copy Full xpathで取得できる。
今回は　/html/body/div/div[3]/div/main/article/div/p[2]/button
"""
frm = browser.find_element_by_xpath("/html/body/div/div[3]/div/main/article/div/p[2]/button")
time.sleep(1)
frm.click()
print("ダウンロードボタンをクリックしました。")


# In[2]:





# # htmlの解析

# In[1]:


from bs4 import BeautifulSoup
import urllib.request as req


# In[2]:


html ="""
<html>
    <head>
       <meta charset="utf-8">
       <title>キノコード</title>
    </head>
    <body>
       <h1>こんにちは</h1>
    </body>
</html>
"""


# In[3]:


html


# In[5]:


parse_html = BeautifulSoup(html, 'html.parser')


# In[6]:


print(parse_html)


# In[7]:


print(parse_html.prettify())


# In[8]:


url = "https://kino-code.work/python-scraping/"
response = req.urlopen(url)


# In[9]:


parse_html = BeautifulSoup(response,'html.parser')


# In[10]:


parse_html


# In[11]:


print(parse_html.title)


# In[12]:


print(parse_html.title.string)


# In[13]:


#aタグをすべて取得
print(parse_html.find_all('a'))


# In[14]:


title_lists = parse_html.find_all('a')


# In[15]:


title_lists[1:10]


# In[17]:


#文字列のみ取得
title_lists[10].string


# In[18]:


#href属性のみ取得
title_lists[10].attrs['href']


# In[20]:


#タイトルとURLのリストを取得する
title_list = []
url_list = []
for i in title_lists:
    title_list.append(i.string)
    url_list.append(i.attrs['href'])


# In[24]:


title_list


# In[25]:


url_list


# In[28]:


import pandas as pd
df_title_url = pd.DataFrame({'title': title_list, 'URL': url_list})


# In[29]:


df_title_url


# In[35]:


#欠損値を覗く
#how=any 欠損値が1つでもあれば行を削除
# now = allだとすべての列がNULLだった時に削除する。
df_notnull = df_title_url.dropna(how='any')


# In[36]:


df_notnull


# In[37]:


# titleに「Python超入門コース」が含まれる行だけ抽出
df_notnull['title'].str.contains('Python超入門コース')


# In[38]:


df_notnull[df_notnull['title'].str.contains('Python超入門コース')]


# In[39]:


df_contain_python = df_notnull[df_notnull['title'].str.contains('Python超入門コース')]


# In[40]:


df_contain_python


# In[42]:


df_contain_python.to_csv('output.csv',encoding='shift-jis')


# In[43]:


# .pyに変換
import subprocess
subprocess.run(['jupyter', 'nbconvert', '--to', 'script', '*.ipynb'])
get_ipython().system('jupyter nbconvert --to script スクレイピング基礎.ipynb')


# In[ ]:





# In[ ]:




