import selenium
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time
from random import randint

def waitel(b,xpath):
    while(True):
        if (b.find_element_by_xpath(xpath).is_displayed()):
            return b.find_element_by_xpath(xpath)
        time.sleep(.1)

def foundel(b,xpath):
    found=False
    while not found:
        try: 
            return waitel(b,xpath)
        except StaleElementReferenceException:
            time.sleep(.1)

def getQuery():
    nw=randint(2,4)//2
    str=''
    for w in range(0,nw): 
        n=randint(0,num_lines-1)
        with open('words.txt') as fp:
            for i, line in enumerate(fp):
                if i==n:
                    str+=line+' '
    return str
 
def doSearches(b,number,em,pw):
    b.get('https://login.live.com/login.srf') # boot and log in
    b.find_element_by_xpath('//*[@id="i0116"]').send_keys(em)
    b.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    foundel(b,'//*[@id="i0118"]').send_keys(pw)
    b.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    b.get('https://www.bing.com')
    for k in range(number): # search
        time.sleep(randint(2,5))
        b.find_element_by_xpath('//*[@id="sb_form_q"]').clear()
        b.find_element_by_xpath('//*[@id="sb_form_q"]').send_keys(getQuery())
        #b.find_element_by_xpath('//*[@id="sb_form_go"]').click()
    time.sleep(1)

def getPoints(b,em):
    global cv
    b.get('https://account.microsoft.com/rewards')
    q=int(b.find_element_by_xpath('//*[@id="dashboard"]/div[2]/div[1]/div/div[1]').text.replace(',',''))
    print(em[:10],'...','%8s'%str(q),'pts,','$%.2f'%(q/5250))
    cv+=q

def mainloop(em,pw):
    b = webdriver.Chrome() 
    doSearches(b,30,em,pw) # pc searches
    capabilities={'chromeOptions':{'mobileEmulation':{'deviceName':'Nexus 7'}}}
    b.start_session(capabilities) 
    doSearches(b,20,em,pw) # mobile searches
    getPoints(b,em)
    b.quit()

t0=time.time()
num_lines = sum(1 for line in open('words.txt'))
cv=0
na=0
with open('credentials.txt','r+') as f:
    for elem in f.readlines():
        mainloop(elem.split(',')[0].strip(),elem.split(',')[1].strip())
        na+=1
print('TOTALS .......','%8s'%str(cv),'pts,','$%.2f'%(cv/5250))
print(na,'account(s) completed in',time.time()-t0,'seconds.')
