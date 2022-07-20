#!/usr/bin/env python3

import schedule
import requests
import sys
from datetime import datetime, date
from playsound import playsound
import time
import config as cfg
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
# import pygame


chrome_binary = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
chrome_webdriver = r"C:/BrowserDrivers/chromedriver.exe"
prayerTimes = []


def playAdhan():
    print("It's prayer time!")
    playsound("sound/adhan.mp3")
    return schedule.CancelJob

def playFajr():
    print("It's prayer time!")
    playsound("sound/fajr.mp3")
    return schedule.CancelJob

def getPrayerTimes():
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

    prayers = soup.find_all("div", class_="prayers")

    for prayer in prayers:
        prayer = prayer.find_all('div', class_="time")
        for pt in prayer:
            pt = pt.find('div').text
            prayerTimes.append(pt)
    
    print(f"""
    Fajr: {prayerTimes[0]}
    Dhuhr: {prayerTimes[1]}
    'Asr: {prayerTimes[2]}
    Maghrib: {prayerTimes[3]}
    'Isha: {prayerTimes[4]}
    """)

    for i, times in enumerate(prayerTimes):
        if i != 0:
            schedule.every().day.at(prayerTimes[i]).do(playAdhan)
        elif i == 0:
            schedule.every().day.at(prayerTimes[i]).do(playFajr)

if __name__ == "__main__":
    getPrayerTimes()
    schedule.every().day.at("00:00").do(getPrayerTimes)

    while True:
        schedule.run_pending()
        time.sleep(1)
