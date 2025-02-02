import time
import ddddocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
date = '2025-02-02'
seat = '211'
#TODO: 输入学工号和密码、日期、座位号
#TODO：每日7：00：00±5s内自动运行
try:
    # 一、进入网站并登录
    driver.get("https://m.ruc.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fm.ruc.edu.cn%2Fsite%2FapplicationSquare%2Findex%3Fsid%3D23");print("已进入网站")
    # 等待用户名输入框加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='学工号']"))).send_keys("2023200660")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='密码']"))).send_keys("dyv5r1u6c")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn"))).click();print("登录成功")

    # 二、选择“预约专区”中的“立德研学中心”
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='预约专区']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='立德研学中心']"))).click();print("已选择“立德研学中心”")
    # 三、等待6秒后点击“我知道了”
    time.sleep(6)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='我知道了']"))).click();print("已点击“我知道了”")

    # 四、点击“预约记录”然后点击“预约选座”
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tabbar-word-wrap') and contains(text(), '预约记录')]"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'button-wrap') and text()='预约选座']"))).click();print("已点击“预约记录、预约选座”")

    # 五、点击“研学中心学生工位(14层)”
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'room-name') and text()='研学中心学生工位（14层）']"))).click();print("已点击“研学中心学生工位（14层）”")

    # 六、选择日期并点击“确定”
    time.sleep(2)
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='van-calendar__day' and div[@class='van-calendar__bottom-info' and text()='可约'] and text()='2']"))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='van-calendar__day' and .//div[@class='van-calendar__bottom-info' and text()='可约'] and .//div[text()='2']]"))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'van-button') and contains(@class, 'van-calendar__confirm') and text()='确定']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='确定']]"))).click();print("已选择日期并点击“确定”")
    # 七、选择211号座位
    #TODO：添加判断，如果座位被其他人选了，就发出警告
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{seat}']"))).click();print(f"已选择{seat}号座位")
    # 八、点击“确定”
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='确定']"))).click();print("已点击“确定”")
    # 九、验证码
    ocr = ddddocr.DdddOcr()
    captcha_img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@class='verifyCodeCon']")))
    captcha_base64 = captcha_img.get_attribute("src").split(",")[1]
    captcha_code = ocr.classification(captcha_base64)
    
    # 输入验证码
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class='inputCode']"))).send_keys(captcha_code)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='验证']"))).click();print("已输入验证码")

    print(f"程序执行完毕，成功预约{date}的{seat}号座位")
finally:
    # 关闭 WebDriver
    driver.quit()
    print("已关闭浏览器")