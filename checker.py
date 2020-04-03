import logging
import os
import requests
import time

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlencode, quote_plus

logger = logging.getLogger("checker")
logger.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

opts = Options()
opts.headless = True
logging.info("Starte FireFox")
browser = Firefox(options=opts)

#Setzen der Variablen
url = os.environ.get('URL')
picturepath = os.environ.get('PICTUREPATH', '/tmp/home')
telegrambotkey = os.environ.get('TELEGRAMBOTKEY')
chatid = os.environ.get('CHATID')
xpath = os.environ.get('XPATH')
statustext = os.environ.get('STATUSTEXT')

logging.info("Oeffne Startseite")

# Startseite
browser.get(url)
time.sleep(30)
try:
    browser.get_screenshot_as_file(picturepath + "/1.png")
except WebDriverException:
    logging.info("Bild 1 konnte nicht gespeichert werden.")

status = browser.find_element_by_xpath(xpath).text

browser.quit()

if status != statustext:
    text = 'Produktstatus ist jetzt: "' + status + '"'
    payload = {'chat_id': chatid, 'text': text}
    result = urlencode(payload, quote_via=quote_plus)
    r = requests.get("https://api.telegram.org/" + telegrambotkey + "/sendMessage?" + result)
    logging.info(r.json())

    payload = {'chat_id': chatid, 'text': url}
    result = urlencode(payload, quote_via=quote_plus)
    r = requests.get("https://api.telegram.org/" + telegrambotkey + "/sendMessage?" + result)
    logging.info(r.json())


exit(0)