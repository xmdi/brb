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

def logIn(b,em,pw):
    b.get('https://login.live.com/login.srf') # boot and log in
    b.find_element_by_xpath('//*[@id="i0116"]').send_keys(em)
    b.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    foundel(b,'//*[@id="i0118"]').send_keys(pw)
    b.find_element_by_xpath('//*[@id="idSIButton9"]').click()

def doSearches(b,number):
    b.get('https://www.bing.com')
    for k in range(int(number)): # search
        time.sleep(randint(2,5))
        b.find_element_by_xpath('//*[@id="sb_form_q"]').clear()
        b.find_element_by_xpath('//*[@id="sb_form_q"]').send_keys(getQuery())
    time.sleep(1)

def getPoints(b,flag):
    b.get('https://account.microsoft.com/rewards')
    if flag: # after searches
        global cv
        q=int(b.find_element_by_xpath('//*[@id="dashboard"]/div[2]/div[1]/div/div[1]').text.replace(',','')) 
        print(' %8s'%str(q),'pts',' $%.2f'%(q/1000))
        cv+=q
    else: # before searches
        global iv
        q=int(b.find_element_by_xpath('//*[@id="dashboard"]/div[2]/div[1]/div/div[1]').text.replace(',','')) 
        p=b.find_element_by_xpath('//*[@id="dashboard"]/div[2]/div[3]/div[3]/div/div[3]').text.replace('points','').strip().split('of')
        m=b.find_element_by_xpath('//*[@id="dashboard"]/div[2]/div[3]/div[4]/div/div[3]').text.replace('points','').strip().split('of')
        print('%8s'%str(q),'pts',' %2sp%2sm'%(str(int((int(p[1].strip())-int(p[0].strip()))/5)),str(int((int(m[1].strip())-int(m[0].strip()))/5))),end='',flush=True)
        iv+=q
        return (int(p[1].strip())-int(p[0].strip()))/5,(int(m[1].strip())-int(m[0].strip()))/5

def mainloop(em,pw,PROXY):
    print(em[:10],'...',end='',flush=True)
    op=webdriver.ChromeOptions()
    if po:
        op.add_argument('--proxy-server=%s'%PROXY)
    b=webdriver.Chrome(chrome_options=op) 
    logIn(b,em,pw)
    p,m=getPoints(b,0)
    doSearches(b,p) # pc searches
    capabilities={'chromeOptions':{'mobileEmulation':{'deviceName':'Galaxy S III'}}}
    b.start_session(capabilities) 
    logIn(b,em,pw)
    doSearches(b,m) # mobile searches
    getPoints(b,1)
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
if len(sys.argv)<2:
    print('no credentials file supplied')
    sys.exit()
else:
    credfile=sys.argv[1]
if len(sys.argv)>2:
    if sys.argv[2]=='-p':
        po=1
num_lines = sum(1 for line in open('words.txt'))
num_accts = sum(1 for line in open(credfile))
PROXIES=[0]*num_accts
if po:
    PROXIES=scrapeProxies(num_accts)
cv=0
iv=0
na=0
print('   ACCOUNT    ','   BEFORE ','   TO DO  ','  AFTER ','   CASH ')

with open(credfile,'r+') as f:
    for elem in f.readlines():
        mainloop(elem.split(',')[0].strip(),elem.split(',')[1].strip(),PROXIES[na])
        na+=1
print('TOTALS .......','%8s'%str(cv),'pts,','$%.2f'%(cv*5/5250))
print(na,'account(s) completed in',(time.time()-t0)//1,'seconds.')
