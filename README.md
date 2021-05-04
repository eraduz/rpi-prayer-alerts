# RPi Prayer Alerts

This application is made specifically for the Raspberry Pi. The idea behind this is so I can get notified for the prayer times, initially this was realised on my iOS device, using [Shortcuts](https://support.apple.com/guide/shortcuts/welcome/ios), but with time I noticed it lacked functionality, such as custom alarms and automatisation.
## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

What things you need and what to install and how to install them on your own RPi

#### Hardware
* A Raspberry Pi (any). This is the one I [have](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)

#### Software

* [Git](https://git-scm.com/)
* [Ubuntu](https://releases.ubuntu.com/20.04/)
* Python3 with pip
* [Gstreamer](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c) 

### Installing

A step by step series of examples that tell you how to start using the application.

In your RPi environment, firstly clone the repository, using HTTPS or SSH
```bash
# The following command is to clone the repository using HTTPS
git clone https://github.com/eraduz/rpi-prayer-alerts.git

# The following comment is to clone the repository using SSH (recommended)
git clone git@github.com:eraduz/rpi-prayer-alerts.git
```

When you succesfully cloned the repository, change the directory to the repository using: `cd rpi-prayer-alerts/`, then you're in the right folder, install the necessary packages that's inside the requirements.txt file

```bash
python3 -m pip install -r requirements.txt
```

And now you can run the file by using: `python3 main.py` or since I have integrated [Shebang](https://www.wikiwand.com/en/Shebang_(Unix)) you can also do `./main.py`
but you would have to the file executable by running: `chmod +x main.py`.

### Make it run on boot (Recommended)

Because this application isn't supposed to be just for a one-time run event, rather it's supposed to be ran on boot, and as background process - namely that's the whole point of the app. 

Firstly, create a new service called adhan.
```bash
sudo nano /etc/systemd/system/adhan.service 
```

When you're in that file copy and paste this
```bash
[Unit]
Description=Adhan player
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/home/<your username>/rpi-prayer-alerts/
User=<your username>
ExecStart=/usr/bin/python3 -u /home/<your username>/rpi-prayer-alerts/main.py

[Install]
WantedBy=multi-user.target
```

Then reload systemctl by running: `systemctl daemon-reload`, enable the service by running: `sudo systemctl enable adhan.service`, then start the service by running `sudo systemctl start adhan.service` and finally reboot your system by running: `sudo reboot` and then when it's rebooted, check its status by running: `sudo systemctl status adhan.service`

## Built With

* [Python](https://www.python.org/) - The programming language used
* [Git](https://git-scm.com/) - The version control system used

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details