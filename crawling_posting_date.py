# 필요한 패키지를 불러왔습니다.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import re

# 크롬을 열고 전체화면으로 전환 인프런 사이트를 엽니다.
driver = webdriver.Chrome()
driver.maximize_window()

# 추출할 데이터를 담을 리스트를 생성합니다.
want_list = ['it-programming', 'game-dev-all','data-science', 'it', 'business/task-automation', 'hardware']
list_data = []

# 개발/프로그래밍

def inflearn_crawling(x):
    page = 1
    for i in range(1,10000):

        title1=driver.find_element(
            By.XPATH, f'//*[@id="courses_section"]/div/div/div/main/div[4]/div/div[1]/div/a/div[2]/div[1]').text
        driver.get(f'https://www.inflearn.com/courses/{x}?order=seq&page={i}')
        time.sleep(1)
        
        title2=driver.find_element(
            By.XPATH, f'//*[@id="courses_section"]/div/div/div/main/div[4]/div/div[1]/div/a/div[2]/div[1]').text
        
        if page >=2:
            if title1 == title2:
                break
            else:
                pass
            
        page +=1
        

        for i in range(1,25):
            try:
                try:
                    driver.find_element(By.XPATH, f'//*[@id="courses_section"]/div/div/div/main/div[4]/div/div[{i}]/div/a/div[2]/span').is_displayed()
                except:
                    # 가격
                    class_price = driver.find_element(By.XPATH, f'//*[@id="courses_section"]/div/div/div/main/div[4]/div/div[{i}]/div/a/div[2]/div[4]').text

                    # 항목 클릭
                    try :
                        element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="courses_section"]/div/div/div/main/div[4]/div/div[{i}]/div/a/div[1]/figure/img')))
                        driver.execute_script("arguments[0].click();", element)                          
                    except :
                        element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="courses_section"]/div/div/div/main/div[4]/div/div[{i}]/div/a/div[1]/section/video')))
                        driver.execute_script("arguments[0].click();", element)

                    time.sleep(1)

                    # 강좌명
                    class_name = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[1]/div[1]/div/div/div[2]/div[2]/h1').text
                    
                    # 강좌 게시일
                    class_update_date = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[1]/div/section[4]/div/span[1]').text
                    
                    # 강의생 수
                    class_stunum = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[1]/div[1]/div/div/div[2]/div[3]/span[2]/strong').text
                    
                    # 평점
                    try :
                        class_grade = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[1]/div[1]/div/div/div[2]/div[3]/span[1]/strong').text
                    except :
                        class_grade = '0'
                        pass

                    # 난이도
                    class_level = driver.find_element(By.XPATH, '//*[@id="description"]/h2[1]/strong[1]').text

                    # 강의 총 시간
                    if "D" in driver.find_element(By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[2]/aside/div[2]/div/div[1]').text :
                        class_time = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[2]/aside/div[2]/div[1]/div[3]/div/div[2]').text

                    elif "신규" in driver.find_element(By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[2]/aside/div[2]/div/div[1]').text:
                        class_time = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[2]/aside/div[2]/div[1]/div[3]/div/div[2]').text

                    elif "할인" in driver.find_element(By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[2]/aside/div[2]/div/div[1]').text:
                        class_time = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[2]/aside/div[2]/div[1]/div[3]/div/div[2]').text

                    else :
                        class_time = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[2]/aside/div[2]/div[1]/div[2]/div/div[2]').text


                    list_data.append([class_name,class_stunum, class_price, class_grade, class_level, class_time, class_update_date])

                    driver.back()
                    time.sleep(1)
            except NoSuchElementException as e:
                break

# 정의한 함수를 불러와 크롤링을 시작합니다.
for i in want_list:
    driver.get(f'https://www.inflearn.com/courses/{i}?order=seq')
    inflearn_crawling(i)

df = pd.DataFrame(list_data)
df.to_csv('데이터 전처리 전1.csv', index=False)
