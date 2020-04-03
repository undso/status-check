import os
import requests
import time

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlencode, quote_plus

opts = Options()
opts.headless = True
print('Starte Firefox')
browser = Firefox(options=opts)

#Setzen der Variablen
url = os.environ.get('URL')
picturepath = os.environ.get('PICTUREPATH', '/tmp/home')
telegrambotkey = os.environ.get('TELEGRAMBOTKEY')
chatid = os.environ.get('CHATID')
xpath = os.environ.get('XPATH')
statustext = os.environ.get('STATUSTEXT')

print('Öffne URL')
browser.get(url)
time.sleep(30)
try:
    browser.get_screenshot_as_file(picturepath + '/1.png')
except WebDriverException:
    print('Bild konnte nicht gespeichert werden.')

status = browser.find_element_by_xpath(xpath).text

browser.quit()

if status != statustext:
    text = 'Produktstatus ist jetzt: "' + status + '"'
    payload = {'chat_id': chatid, 'text': text}
    result = urlencode(payload, quote_via=quote_plus)
    r = requests.get("https://api.telegram.org/" + telegrambotkey + "/sendMessage?" + result)
    print(r.json())

    payload = {'chat_id': chatid, 'text': url}
    result = urlencode(payload, quote_via=quote_plus)
    r = requests.get("https://api.telegram.org/" + telegrambotkey + "/sendMessage?" + result)
    print(r.json())


exit(0)