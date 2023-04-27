#!/usr/bin/env python3

from scapy.all import ARP, Ether, srp
import os
import requests
import smtplib
from email.mime.text import MIMEText
import config
import subprocess
from datetime import date
import ping3
import datetime

def getCurrentPublicIP():
    ip_request = requests.get('https://api.ipify.org').text
    alertPublicIP(ip_request)
    addLineInFile(ip_request,"publicip")
    print("\nPUBLIC IP:\n" + str(ip_request))

def alertPublicIP(current_ip):
    last_ip=readLastValue(config.PUBLICIP_PATH)[:-1]

    if current_ip != last_ip:
        # Envio de una alerta por correo electronico
        subject = "ALETR: Public IP changed!"
        body = "The public IP address has changed to {}.".format(current_ip)
        sendEmail(subject, body)

def sendEmail(subject, body):
    source_email = config.EMAIL_FROM
    key = config.EMAIL_PASS
    detination_email =config.EMAIL_TO

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = source_email
    msg['To'] = detination_email

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(source_email,key)
    server.sendmail(source_email,detination_email,msg.as_string())

    server.quit()

def addLineInFile(text, file):
    if(file=="publicip"):
        file_object = open(config.PUBLICIP_PATH, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()
    elif(file=="speed"):
        file_object = open(config.SPEED_PATH, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()

def readLastValue(file):
    with open(file, 'r') as f:
        for line in f:
            pass
        last_line = line
    return(last_line)

def scanNetwork():
    # IP address of the network to be scanned
    target_ip = "192.168.1.0/24"

    # Create an ARP request to scan the network
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # Send ARP request and receive response
    result = srp(packet, timeout=3, verbose=0)[0]

    # Create a list of detected equipment
    devices = []
    for received in result:
        devices.append({'ip': received.answer.payload.psrc, 'mac': received.answer.payload.hwsrc})
    
    # Print connected devices
    print("DEVICES CONNECTED TO THE NETWORK:")

    for device in devices:
        try:
            print(f"IP: {device['ip']}, MAC: {device['mac']},   Name: {config.whitelist[device['mac']]}")
        except:
            msg=f"Unknown device connected to the network with \nIP: {device['ip']} \nMAC: {device['mac']}"
            sendEmail("Unknown device connected to the network",msg)

def speedTest():
    process = subprocess.Popen(["speedtest-cli", "--simple"], stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error is not None:
        print("Error running speedtest-cli:", error)
    else:
        output = output.decode('utf-8')
        lines = output.strip().split('\n')
        ping = float(lines[0].split(' ')[1])
        download = float(lines[1].split(' ')[1])
        upload = float(lines[2].split(' ')[1])
        today = str(date.today())
        hour = datetime.datetime.now().time().strftime("%H:%M:%S")
        print("\nSPEED TEST:")
        msg = "Date: {}, Hour: {}, Ping: {:.2f} ms, Download: {:.2f} Mbps, Upload: {:.2f} Mbps".format(today, hour, ping, download, upload)
        print(msg)
        addLineInFile(msg,"speed")

def monitorImportantIps(list):
    print("\nMONITORING IMPORTANT IPs:")
    for ip in list:
        response_time = ping3.ping(ip)
        if response_time is not False:
            print('IP address {} is reachable'.format(ip))
        else:
            if ip == "8.8.8.8":
                msg="No internet connection"
                subject="No internet connection"
            else:
                if format(ip) == "8.8.8.8":
                    msg='IP address {} is not reachable'.format(ip)
                else:
                    device_name = config.important_ips[ip]
                    msg='Device: {} (IP address: {}) is not reachable.'.format(device_name,ip)

                subject="Device not reachable!"
            print(subject, msg)
            sendEmail(subject, msg)

def cleanLines(file1, file2):
    max=200
    with open(file1, "r+") as file:
        lines = file.readlines()
        if len(lines) > max:
            file.seek(0)
            file.writelines(lines[1:])
            file.truncate()
    with open(file2, "r+") as file:
        lines = file.readlines()
        if len(lines) > max:
            file.seek(0)
            file.writelines(lines[1:])
            file.truncate()

    
########## PROGRAM ##########
os.system('clear')
scanNetwork()
getCurrentPublicIP()
speedTest()
monitorImportantIps(config.important_ips.keys())
cleanLines(config.PUBLICIP_PATH, config.SPEED_PATH)