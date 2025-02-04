import time
import json
import ddddocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("config.json", "r") as f:
    config = json.load(f)
    STUDENT_ID = config["STUDENT_ID"]
    PASSWORD = config["PASSWORD"]
    SEAT = config["SEAT"]
    CHROMEDRIVER_PATH = config["CHROMEDRIVER_PATH"]

# 初始化 WebDriver
service = Service(CHROMEDRIVER_PATH)

options = webdriver.ChromeOptions()
options=webdriver.ChromeOptions()

options.add_argument('--ignore-ssl-errors')
#options.add_argument('--headless')  # 无头模式
options.add_argument('--ignore-certificate-errors') # 忽略证书错误
# 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 忽略 DevTools listening on ws://127.0.0.1... 提示
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=service, options=options)
date = time.strftime("%Y-%m-%d", time.localtime())

driver.get("https://m.ruc.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fm.ruc.edu.cn%2Fsite%2FapplicationSquare%2Findex%3Fsid%3D23")
    
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='学工号']"))).send_keys(STUDENT_ID)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='密码']"))).send_keys(PASSWORD)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn"))).click()
print("1/4已进入网站并登录成功")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='立德研学中心']"))).click()
print("2/4已选择“立德研学中心”")
    
time.sleep(6)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='我知道了']"))).click()
print("3/4已点击“我知道了”")   
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tabbar-word-wrap') and contains(text(), '预约记录')]"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='结束使用']"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., '确认')]"))).click()
print("4/4已输入验证码")
print(f"{date}的{SEAT}号座位已被释放，妈妈再也不用担心我被封号啦🥳🥳🥳")