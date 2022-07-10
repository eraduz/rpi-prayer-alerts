from datetime import datetime
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import requests
import json
import config as cfg
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.service import Service
from lxml import etree
import schedule
from playsound import playsound
import time
import pygame

pygame.init()
pygame.mixer.init()

chrome_binary = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
chrome_webdriver = r"C:/BrowserDrivers/chromedriver.exe"

options = Options()
options.headless = True
options.binary_location = chrome_binary
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
driver = webdriver.Chrome(chrome_webdriver, options=options)
driver.get(cfg.url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

# <div class="time"> </div>
prayers = soup.find_all("div", class_="prayers")

prayerTimes = []
now = datetime.now()
current_time = now.strftime("%H:%M")

for prayer in prayers:
    prayer = prayer.find_all('div', class_="time")
    for pt in prayer:
        pt = pt.find('div').text
        prayerTimes.append(pt)

tree = etree.HTML(str(soup), etree.HTMLParser())


dateHijri = tree.xpath('//*[@id="hijriDate"]/span')[0].text
dateGreg = tree.xpath('//*[@id="gregorianDate"]')[0].text

def playAdhan():
    sound = pygame.mixer.Sound(r"./sound/adhan.wav")
    sound.set_volume(0.75)
    sound.play()
    
def playAdhanFajr():
    sound = pygame.mixer.Sound(r"./sound/fajr.wav")
    sound.set_volume(0.5)
    sound.play()        
        
if __name__ == '__main__':       
    print(f"""
    {dateHijri}
    {dateGreg}
    Het is nu: {current_time}

    Fajr: {prayerTimes[0]}
    Dhuhr: {prayerTimes[1]}
    'Asr: {prayerTimes[2]}
    Maghrib: {prayerTimes[3]}
    'Isha: {prayerTimes[4]}
    """)
    for i, times in enumerate(prayerTimes):
        if current_time != prayerTimes[0] and i != 0:
            schedule.every().day.at(prayerTimes[i]).do(playAdhan)
        else:
            schedule.every().day.at(prayerTimes[i]).do(playAdhanFajr)

    while True:
        schedule.run_pending()
        time.sleep(1)




