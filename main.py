#!/usr/bin/env python3

import schedule
import requests
import sys
from datetime import datetime, date
from playsound import playsound
import time
import config as cfg


def playAdhan():
    print("It's prayer time!")
    playsound("sound/adhan.mp3")
    return schedule.CancelJob


def getPrayerTimes():
    r = requests.get(cfg.url)
    if r.status_code != 200:
        sys.exit(f"Something went wrong, API returned status code: {r.status_code}", 1)

    
    times = r.json()["times"]
    prayer_times = []

    currentMonth = str(datetime.now().month)
    currentDay = str(datetime.now().day)

    print(f"Date of today: {date.today()}")

    for period, prayers in times[currentMonth][currentDay].items():
        prayer_times.append(prayers['t'])

    print("Retrieved prayer times!")
    print(
        f"Fajr: {prayer_times[0]}\n"
        f"Shuruq: {prayer_times[1]}\n"
        f"Dhuhr: {prayer_times[2]}\n"
        f"'Asr: {prayer_times[3]}\n"
        f"Maghrib: {prayer_times[4]}\n"
        f"'Isha: {prayer_times[5]}")

    for i in range(0, len(prayer_times)):
        if i != 1:
            schedule.every().day.at(prayer_times[i]).do(playAdhan)


if __name__ == "__main__":
    getPrayerTimes()
    schedule.every().day.at("00:00").do(getPrayerTimes)

    while True:
        schedule.run_pending()
        time.sleep(1)
