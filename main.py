import schedule
import requests
import sys
from datetime import datetime, date
from playsound import playsound
import time
import config as cfg

r = requests.get(cfg.url)


def playAdhan():
    print("It's prayer time!")
    playsound(f"sound/beep.mp3")


def getPrayerTimes():
    print('-------------------------------------------')
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
        f"'Isha: {prayer_times[5]}\n ")

    for t in prayer_times:
        schedule.every().day.at(t).do(playAdhan)

    print(prayer_times)


if __name__ == "__main__":
    if r.status_code == 200:
        getPrayerTimes()
        schedule.every().day.at("00:00").do(getPrayerTimes)
    else:
        sys.exit(f"Something went wrong, API returned status code: {r.status_code}")

    while True:
        schedule.run_pending()
        time.sleep(1)
