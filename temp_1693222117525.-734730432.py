import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

faker_opgg_url = 'https://www.op.gg/summoners/kr/Hide%20on%20bush'

driver = webdriver.Safari()

driver.get(faker_opgg_url)
driver.maximize_window()

while True:
    # 게임 로딩, html 코드 변경까지 여유 시간을 3초 가집니다.
    time.sleep(3)
    try:
        # 더보기 버튼 선택을 시도합니다.
        driver.find_element_by_xpath('//*[@id="content-container"]/div[2]/button')
        
    # 에러가 나면(페이지에서 '더 보기' 버튼이 없을 경우) while문을 탈출합니다.
    except Exception as e:
        pass
        break

# 게임이 모두 로딩된 페이지의 html 코드를 faker_total_html로 저장합니다.
faker_total_html = driver.page_source
# string 형태의 html을 파싱합니다.
soup = BeautifulSoup(faker_total_html, 'html.parser')

# 원하는 div 요소를 순차적으로 찾습니다.
div_element = soup.find('div', id='__next')
div_element.find('div', class_='css-1o9et5d e1jlljr10')
div_element = div_element.find('div', class_='css-164r41r e17ux5u10')

# div 요소 안에 포함된 모든 content를 찾습니다.
div_elements = div_element.find_all(class_='content')

# <div 로 시작해서 >로 끝나는 패턴 정규표현식
pattern = r"<div[^>]*>"

# 정규표현식의 조건에 맞는 문장을 찾아 \n문자를 추가합니다.
new_string = re.sub(pattern, lambda match: "\n" + match.group(), str(div_elements))

# string으로 다시 바뀐 문장을 BeautifulSoup으로 파싱합니다.
soup = BeautifulSoup(new_string, 'html.parser')

# dataframe으로 변환하기 위해 파일로 저장합니다.
with open('faker.txt', 'w', encoding='utf-8') as file:
    for element in soup:
        if len(element.text) <= 3:
            continue
        file.write(element.text)