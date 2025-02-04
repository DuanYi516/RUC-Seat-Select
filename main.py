import time
import json
import ddddocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 获取当前日期的日
day = time.strftime("%d", time.localtime())
if day.startswith("0"):day = day[1:]
day=str(int(day)+1)

with open("config.json", "r") as f:
    config = json.load(f)
    STUDENT_ID = config["STUDENT_ID"]
    PASSWORD = config["PASSWORD"]
    SEAT = config["SEAT"]
    CHROMEDRIVER_PATH = config["CHROMEDRIVER_PATH"]

service = Service(CHROMEDRIVER_PATH)

options = webdriver.ChromeOptions()
options=webdriver.ChromeOptions()

options.add_argument('--ignore-ssl-errors')
# options.add_argument('--headless')  # 无头模式
options.add_argument('--ignore-certificate-errors') # 忽略证书错误
# 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 忽略 DevTools listening on ws://127.0.0.1... 提示
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(375, 812)

tommorow = time.strftime("%Y-%m-%d", time.localtime(time.time()+86400))
#TODO：每日7：00：00±5s内自动运行
try:
    driver.get("https://m.ruc.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fm.ruc.edu.cn%2Fsite%2FapplicationSquare%2Findex%3Fsid%3D23")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='学工号']"))).send_keys(STUDENT_ID)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='密码']"))).send_keys(PASSWORD)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn"))).click()
    print("1/8已进入网站并登录成功")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='立德研学中心']"))).click()
    print("2/8已选择“立德研学中心”")
    
    time.sleep(6)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='我知道了']"))).click()
    print("3/8已点击“我知道了”")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tabbar-word-wrap') and contains(text(), '预约选座')]"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'room-name') and text()='研学中心学生工位（14层）']"))).click()
    print("4/8已选择“研学中心学生工位（14层）”")
    
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='gridcell' and text()='{day}']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='确定']]"))).click()
    print("5/8已选择日期点击“确定”")

    #TODO：添加判断，如果座位被其他人选了，就发出警告
    if 0:
        print(f"警告：{SEAT}号座位已被其他人选了")
        assert False
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{SEAT}']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='确定']"))).click()
    print(f"6/8已选择{SEAT}号座位并点击“确定”")
    
    ocr = ddddocr.DdddOcr()
    captcha_img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@class='verifyCodeCon']")))
    captcha_base64 = captcha_img.get_attribute("src").split(",")[1]
    captcha_code = ocr.classification(captcha_base64)
    print(f' └─验证码识别成功，结果为{captcha_code}')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='inputCode']//input"))).send_keys(captcha_code)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='验证']"))).click()
    print("7/8已输入验证码")
    
    print(f"8/8成功预约{tommorow}的{SEAT}号座位🥳🥳🥳欢迎开启美好一天的学习")

except RuntimeError as e:
    print(f"发生错误：{e}")
    print("脚本执行失败")
finally:
    driver.quit()
    print("已关闭浏览器,脚本执行完毕")