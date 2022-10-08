import time
import re
import ddddocr
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



def login():
    web.get('https://www.xjgbzx.cn/student/student!index.action?menu=2')
    time.sleep(1)
    web.find_element(By.XPATH,'//*[@id="name"]').send_keys("622826198605093133")
    web.find_element(By.XPATH,'//*[@id="password"]').send_keys("Yl888888")
    ocr = ddddocr.DdddOcr()
    img = web.find_element(By.ID,'codeImg1')
    vcode = img.screenshot("test.png") 
    with open('test.png', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    web.find_element(By.XPATH,'//*[@id="imgcode"]').send_keys(res)
    time.sleep(1)
    web.find_element(By.XPATH,'//*[@id="form1"]/div/div[4]/div[1]').click()

def ready():
    web.find_element(By.ID,'nostudy').click()
    time.sleep(1)
    try:
        data = web.find_element(By.XPATH,'//*[@id="right"]/div[4]/div[2]/div/span[1]').text
        lin= re.search( r'共(.*?)行', data)
        lin = int(lin.group(1))
        web.find_element(By.XPATH,'//*[@id="right"]/div[4]/div[2]/div/span[2]/form/input[5]').send_keys('%s'%lin+Keys.ENTER)
        time.sleep(1)
        original_window = web.current_window_handle
        for i in range(2,lin):
            assert len(web.window_handles) == 1
            web.find_element(By.XPATH,'//*[@id="right"]/div[4]/table[3]/tbody/tr[2]/td[3]/a/img').click()
            wait.until(EC.number_of_windows_to_be(2))
            for window_handle in web.window_handles:
                if window_handle != original_window:
                    web.switch_to.window(window_handle)
                    break
            wait.until(EC.title_is("新疆干部在线学习平台"))
            web.close()
            web.switch_to.window(original_window)
            time.sleep(1)
            web.refresh()
    except:
        print("没有未选课程")
        pass

def study():
    web.find_element(By.ID,'study').click()
    original_window = web.current_window_handle
    time.sleep(1)
    data = web.find_element(By.XPATH,'//*[@id="right"]/div[4]/div[2]/div/span[1]').text
    lin= re.search( r'共(.*?)行', data)
    lin = int(lin.group(1))
    for i in range(0,lin):
        try:
            zongxuefen = str(web.find_element(By.XPATH,'//*[@id="xyxx"]/div[3]/span').text)#获取总学分
            bixiu = str(web.find_element(By.XPATH,'//*[@id="xyxx"]/div[4]/span').text)#获取必修学分
            yihuo = str(web.find_element(By.XPATH,'//*[@id="xyxx"]/div[5]/span').text)#获取已获得学分
            kecheng = str(web.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[3]/div[4]/table[3]/tbody/tr[2]/td[1]').text)#获取当前课程名  
            learn1 = str(web.find_element(By.XPATH,'//*[@id="right"]/div[4]/table[3]/tbody/tr[2]/td[2]/span').text)#获取当前课程进度
            print(zongxuefen+bixiu+yihuo+kecheng)
            print("正在学习,学习进度%s"%learn1)
            if learn1 != "100%":
                minutes = web.find_element(By.XPATH,'//*[@id="right"]/div[4]/table[3]/tbody/tr[2]/td[2]/div').get_attribute("title")#获取当前课程学习时长与总时长
                sminute = re.search('(.*?)分钟/',minutes)
                sminute = int(sminute.group(1))
                minute = re.search('分钟/(.*?)分钟',minutes)
                minute = int(minute.group(1))
                waitminute = minute - sminute + 1
                now = datetime.now()
                print("预计需要:%s分钟"%waitminute)
                print("现在时间%s"%now)
                receiver = ("XJ网院学习通知")
                print(receiver)
                text = f"年度总学分：{zongxuefen}分(必修{bixiu}分)\n已获得学分：{yihuo}分\n正在学习：{kecheng} 学习进度：{learn1}\n预计学习：{waitminute}分钟\n现在时间：{now}"
                api = "https://sctapi.ftqq.com/SCT2780TvCwyvV0Vq6V2MQjVdfkm90Of.send" #填入你的api，如果是普通版的前面的域名可能会不一样
                data = {
                        'text':receiver, #标题
                        'desp':text} #内容
                requests.post(api, data = data)
                assert len(web.window_handles) == 1
                time.sleep(10)
                web.find_element(By.XPATH,'//*[@id="right"]/div[4]/table[3]/tbody/tr[2]/td[3]/a/img').click()
                wait.until(EC.number_of_windows_to_be(2))
                for window_handle in web.window_handles:
                    if window_handle != original_window:
                        web.switch_to.window(window_handle)
                        break
                wait.until(EC.title_is("新疆干部在线学习平台"))
                time.sleep(60*waitminute)
                web.close()
                web.switch_to.window(original_window)
                time.sleep(1)
                web.refresh()
            elif learn1 == "100%":
                web.refresh()
            else:
                print("学习完毕")
                pass
        except:
            print("异常结束")
            web.close()
            web.quit()
            return 0
            

if __name__=='__main__':
    chrome_option = Options()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--disable-gpu')
    #driver_url = r"D:\Bin\chromedriver.exe"
    web = webdriver.Chrome(chrome_options=chrome_option)
    wait = WebDriverWait(web, 10)
    #user = input("请输入用户名：")
    #passwd = input("请输入密码：")
    login()
    ready()
    study()
