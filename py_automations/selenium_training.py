
# Brother HL-L8360CDW Status

# import requests

# link = "http://192.168.5.252/general/status.html"
# link_values = requests.get(link)

# start_split = 'id="moni_data"><span class='
# end_split = '</span></div>'

# split_values = link_values.text.split(start_split)[1].split(end_split)[0].split('>')

# print(split_values)
# print('Done')

# HP Lixo

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from time import sleep


chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--headless')
chrome = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
chrome.get('https://192.168.5.124/sws/index.html')

delay = 7
try:
    element = WebDriverWait(chrome, delay).until(
        expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'sobre o produto')))
    
        # expected_conditions.presence_of_element_located((By.ID, 'ext-comp-1018')))

    print('Wait done')
except TimeoutException:
    print('Could not load')


while True:
    # ext-comp-1044
    # ext-gen266
    # ext-comp-1022
    # ext-gen563
    # ext-comp-1020

    element = chrome.find_element(By.PARTIAL_LINK_TEXT, 'Status:')

    value = element.text
    print(value)

    sleep(1)
    inicio_button = chrome.find_element(By.PARTIAL_LINK_TEXT, 'Início')
    inicio_button.click()
    sleep(5)

sleep(1)
button_info = chrome.find_element(By.ID, 'ext-gen220')
print(button_info.text)
button_info.click()

chrome.quit()
