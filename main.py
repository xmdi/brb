import selenium
from selenium import webdriver
import time

def waitel(bb,xpath):
    while(True):
        if (bb.find_element_by_xpath(xpath).is_displayed()):
            return bb.find_element_by_xpath(xpath)
        time.sleep(.1)

def mainloop(em,pw):
    b = webdriver.Chrome()
    b.get('https://login.live.com/login.srf')
    b.find_element_by_xpath('//*[@id="i0116"]').send_keys(em)
    b.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    waitel(b,'//*[@id="i0118"]').send_keys(pw)
    b.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    time.sleep(10)
    b.quit()

with open('credentials.txt','r+') as f:
    for elem in f.readlines():
        mainloop(elem.split(',')[0].strip(),elem.split(',')[1].strip())
