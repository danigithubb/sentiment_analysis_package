from urllib.parse import parse_qs, urlparse
import requests
from bs4 import BeautifulSoup, SoupStrainer
import selenium             
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
import time
import os

### essentially what i need to do is use the input argument 'ticker' to search the url below, navigate through loads of annoying links and searches and eventually
### download all of the 10k filings to 'dest_folder', as HTML files. 

URL = 'https://www.sec.gov/edgar/searchedgar/companysearch'  ##this webpage is the only webpage i need 
WEBDRIVER_WAIT_SECONDS = 20
# page = requests.get(url)

def download_files_10k(ticker, dest_folder): ##the ticker is the stock market ticker that I need to search the page with. it is variable and i'll need to do this process for a few of them 
    driver = webdriver.Chrome()
    # I wrapped everything in a try-catch-finally, so that we can ensure that the driver closes all the 
    #        time, even if an error occurs.
    # You first need to load the URL
    driver.get(URL)
    # Original line: xpathsearchbox = r'//input[@id="edgar-company-person"]'
    # You also don't need to use raw strings here so you can safely remove the "r". I replaced "*"
    #        with "input" as it makes it a bit easier for me to follow along with the flow but "*" is also
    #        completely fine here.
    xpathsearchbox = '//input[@id="edgar-company-person"]' ##trying to find the search bar on that page.
    # Original line: driver.find_element('xpath', xpathsearchbox).send_keys(ticker,Keys.ENTER)
    # Instead of using a string literal "xpath" you can use the constants defined in the By module. 
    #        Not really necessary, but looks prettier. You should also use the WebDriverWait class here to 
    #        wait until the element has loaded on the page so you stop getting NoSuchElementExceptions.
    #        WebDriverWait can wait until certain conditions are met (expected_conditions) and then the 
    #        XPATH will be found on the page. Here we wait a maximum of 20 seconds for the XPATH to exist
    #        on the page.
    WebDriverWait(driver, WEBDRIVER_WAIT_SECONDS).until(EC.presence_of_element_located((By.XPATH, xpathsearchbox))).send_keys(ticker, Keys.ENTER) #searching the website for the input ticker
    tenkfilings = '//*[@id="filingsStart"]/div[2]/div[3]/h5' 
    ##identifying the '10-k (annual reports) and 10-q(quarterly reports)' button 
    # Original line: driver.find_element("xpath", tenkfilings).click()
    # Again we use the WebDriverWait class here, cos this page takes a while to load sometimes...
    WebDriverWait(driver, WEBDRIVER_WAIT_SECONDS).until(EC.element_to_be_clickable((By.XPATH, tenkfilings))).click() ##clicking on said button
    tenkandtenq = '//*[@id="filingsStart"]/div[2]/div[3]/div/button[1]' ##finding the 'view all 10ks and 10-qs'
    #  We don't need to use WebDriverWait here as the page has loaded already
    ###driver.find_element('xpath', tenkandtenq).click()
    WebDriverWait(driver, WEBDRIVER_WAIT_SECONDS).until(EC.element_to_be_clickable((By.XPATH, tenkandtenq))).click() ##clicking on that
    search2 = '//input[@id="searchbox"]' ## finding the 'search tables' bar on the filings page 
    # Original line: onlytenks = driver.find_element(By.XPATH, search2).send_keys('K') ##searching the table with 'K' to bring up only the 10ks
    # We don't need to save the element to a variable anymore as we don't use it
    driver.find_element(By.XPATH, search2).send_keys('10-K') ##searching the table with 'K' to bring up only the 10ks
    time.sleep(1)
    source=driver.page_source
    html  = BeautifulSoup(source, parseOnlyThese=SoupStrainer('table', 'table table-striped table-bordered table-sm small dataTable no-footer dtr-inline' ))
    links = html.findAll('a',{'class':'document-link'})
    full_link=[]
    for i in links:
        full_link.append('https://www.sec.gov'+i.get('href'))
    years=html.findAll('td',{'class':'sorting_1'})
    year_list=[]
    for x in years:
        year_list.append(str(x.text))
    zip_link_and_year=list(zip(full_link,year_list))
    failed_link=[]
    failed_year=[]
    driver2=webdriver.Chrome()
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    for link,year in zip_link_and_year:
        driver2.get(link)
        time.sleep(1)
        try:
            xpath_dropdown=r'//*[@id="menu-dropdown-link"]'
            driver2.find_element("xpath", xpath_dropdown).click()
            time.sleep(1)
            xpath_open_as_html=r'//*[@id="form-information-html"]'
            driver2.find_element("xpath", xpath_open_as_html).click()
            time.sleep(1)
        except:
            failed_link.append(link)
            failed_year.append(year)
        source1=driver2.page_source
        filepath=os.path.join(dest_folder,ticker+'_10-k_'+str(year)+'.html')
        f=open(filepath,'w',encoding='utf-8')
        f.write(source1)
        f.close()
    zip_failed=list(zip(failed_link,failed_year))
    driver1=webdriver.Chrome()
    for link,year in zip_failed:
        driver1.get(link)
        time.sleep(1)
        try:
            xpath_dropdown=r'//*[@id="menu-dropdown-link"]'
            driver1.find_element("xpath", xpath_dropdown).click()
            time.sleep(1)
            xpath_open_as_html=r'//*[@id="form-information-html"]'
            driver1.find_element("xpath", xpath_open_as_html).click()
            time.sleep(1)
        except:
            pass
        source2=driver1.page_source
        filepath=os.path.join(dest_folder,ticker+'_10-k_'+str(year)+'.html')
        f=open(filepath,'w',encoding='utf-8')
        f.write(source2)
        f.close()
