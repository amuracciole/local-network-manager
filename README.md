# Local Network Manager
This script helps you keep track of your home network. 
With this script you can :
- Keep track of connected devices and create white lists.
- Make constant checks of the public IP and changes
- Make constant check of upload and download speed
- Periodically monitor that the most important devices within the network are active
- Send email alarms in case something fail or any suspicious activity

You should install scapy, requests, ping3, speedtest-cli


## Keys :key:
Plese add you own keys and paths in config.py file
- EMAIL_FROM -> Mail that sends the notifications
- EMAIL_TO -> Mail where notifications are received
- EMAIL_PASS -> This is not your email account password, is a "key" obtained in your email settings to allow you send messages from external API
- PUBLICIP_PATH -> Complete path that you save the current public IP
- SPEE_PATH -> Complete path that you save the uplink and downlink speed
- whitelist -> This is the whitelist. You must include all known devices. Devices that are not in the list are automatically unknownd devices (suspicius)
- important_ips -> List with all relevants IPs. These IPs are important for you and should be monitorized


## Email :email:
Allows you to send an email with a notification once bot make an operation. This is a second way to save a history

## Crontab :stopwatch:
You MUST include the following line in you crontab file to run the script every day at 4:00 AM (You can schedule as you wish)

**Note: In case you have devices (like Iphones with "Private Wi-Fi address) I will recommend you to disable that feature for your WiFi networkto avoid false-positives alerts. At the end of the day that is a known network, so it is not necessary to hide your real MAC address**

0 4 * * * *project path*

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/amuracciole)