import selenium
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time
from random import randint
import sys

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
    print(em[:10],'...','%8s'%str(q),'pts,','$%.2f'%(q*5/5250))
    cv+=q

def mainloop(em,pw,PROXY):
    op=webdriver.ChromeOptions()
    if po:
        op.add_argument('--proxy-server=%s'%PROXY)
    b = webdriver.Chrome(chrome_options=op) 
    doSearches(b,30,em,pw) # pc searches
    capabilities={'chromeOptions':{'mobileEmulation':{'deviceName':'Galaxy S III'}}}
    b.start_session(capabilities) 
    doSearches(b,20,em,pw) # mobile searches
    getPoints(b,em)
    b.quit()

def scrapeProxies(qty):
    proxies=[]
    b=webdriver.Chrome()
    b.get('http://www.us-proxy.org')
    b.find_element_by_xpath('//*[@id="proxylisttable"]/thead/tr/th[7]').click()
    b.find_element_by_xpath('//*[@id="proxylisttable"]/thead/tr/th[7]').click()
    time.sleep(1)
    for q in range(0,qty):
        proxies.append(b.find_element_by_xpath('//*[@id="proxylisttable"]/tbody/tr['+str(q+1)+']/td[1]').text+':'+b.find_element_by_xpath('//*[@id="proxylisttable"]/tbody/tr['+str(q+1)+']/td[2]').text)
    b.quit()
    print(qty,'proxies scraped from us-proxy.org')
    return proxies

t0=time.time()
po=0
if len(sys.argv)>1:
    if sys.argv[1]=='-p':
        po=1
num_lines = sum(1 for line in open('words.txt'))
num_accts = sum(1 for line in open('credentials.txt'))
PROXIES=[0]*num_accts
if po:
    PROXIES=scrapeProxies(num_accts)
cv=0
na=0
with open('credentials.txt','r+') as f:
    for elem in f.readlines():
        mainloop(elem.split(',')[0].strip(),elem.split(',')[1].strip(),PROXIES[na])
        na+=1
print('TOTALS .......','%8s'%str(cv),'pts,','$%.2f'%(cv*5/5250))
print(na,'account(s) completed in',time.time()-t0,'seconds.')
