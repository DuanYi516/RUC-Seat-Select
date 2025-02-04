import time
import ddddocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化 WebDriver
service = Service('C:/Program Files/Google/Chrome/Application/chromedriver.exe')

options = webdriver.ChromeOptions()
options=webdriver.ChromeOptions()

options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')  # 无头模式
options.add_argument('--ignore-certificate-errors') # 忽略证书错误
# 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 忽略 DevTools listening on ws://127.0.0.1... 提示
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=service, options=options)
date = time.strftime("%Y-%m-%d", time.localtime())
# 输入学工号和密码座位号
STUDENT_ID = 2023200660#str(input("请输入学工号："))
PASSWORD = 'dyv5r1u6c'#str(input("请输入密码："))
SEAT = '211'#str(input("请输入座位号："))
#TODO: 输入学工号和密码、日期、座位号
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
    
    time.sleep(2)
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='gridcell' and text()='5']"))).click()
    #TODO:选择日期（网页源代码：
    # <div role="gridcell" tabindex="-1" class="van-calendar_day">"5"<div class="van-calendar__bottom-info" style>可约</div></div>）
    
    
    
    # 确保浮窗可见
    calendar_modal = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'calenderModal')]"))
    )
    print('  -已打开日期选择浮窗')
    # 使用显式等待，确保元素可见且可点击
    date_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='gridcell' and contains(@class, 'van-calendar__day')]//div[text()='5']"))
    )
    print(date_element.get_attribute("class"))
    date_element.click()
    print('6/8已选择日期')



    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='确定']]"))).click()
    print("7/8点击“确定”")

    #TODO：添加判断，如果座位被其他人选了，就发出警告
    if WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{SEAT}']")).get_attribute("class") == ""):
        print(f"警告：{SEAT}号座位已被其他人选了")
        assert False
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{SEAT}']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='确定']"))).click()
    print(f"8/8已选择{SEAT}号座位并点击“确定”")
    
    ocr = ddddocr.DdddOcr()
    captcha_img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@class='verifyCodeCon']")))
    captcha_base64 = captcha_img.get_attribute("src").split(",")[1]
    captcha_code = ocr.classification(captcha_base64)
    print(f'  -验证码识别成功，结果为{captcha_code}')
    print("测试完成")
    exit()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='inputCode']//input"))).send_keys(captcha_code)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='验证']"))).click()
    print("7/8已输入验证码")
    
    print(f"成功预约{date}的{SEAT}号座位🥳🥳🥳欢迎开启美好一天的学习")

except:#Exception as e
    # print(f"发生错误：{e}")
    pass
    # print("脚本执行失败")
finally:
    driver.quit()
    print("已关闭浏览器,脚本执行完毕")