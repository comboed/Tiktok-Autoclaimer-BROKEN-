#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# apt-get install python3-dev python3-pip -y
# python3 -m pip install colorama discord_webhook pycurl

from discord_webhook import DiscordEmbed, DiscordWebhook
from threading import Thread, Lock
from datetime import datetime
from queue import Queue
from time import sleep

import pycurl
import random
import os

TIKTOK_COLOR = ["F20953", "01F2E9"]
TIKTOK_API_CHECK_PROFILE = "/aweme/v1/user/profile/other/?iid=7035654756384163590&channel=googleplay&app_name=musical_ly&version_code=2215&device_platform=android&device_type=G011A&os_version=7.1.2&user_id="
TIKTOK_API_EDIT_PROFILE = "/aweme/v1/commit/user/?version_name=20.7.5&channel=googleplay&device_platform=android&device_id=7035485364727465477&device_brand=google&aid=1233"

class Util():
    def checkFiles(self):
        if not os.path.exists("data"):
            os.makedirs("data")

            if not os.path.exists("./data/claimed"):
                os.makedirs('./data/claimed')

                if not os.path.exists("./data/banned"):
                    os.makedirs('./data/banned')

            open("./data/sessions.txt", "w+")
            open("./data/usernames.txt", "w+")

            print("[" + RGB(255, 135, 205, "-") + f"] Data folder created!")

            sleep(1)
            exit(1)

        if not os.path.exists("./data/usernames.txt"):
            open("./data/usernames.txt", "w+")

            if not os.path.exists("./data/sessions.txt"):
                open("./data/sessions.txt", "w+")

        if len(open("./data/sessions.txt", "r").read().splitlines()) < 1:
            print("[" + RGB(255, 135, 205, "-") + f"] Please put at least one session in sessions.txt")
            
            sleep(1)
            exit(1)

        if len(open("./data/usernames.txt", "r").read().splitlines()) < 1:
            print("[" + RGB(255, 135, 205, "-") + f"] Please put at least one username in usernames.txt")

            sleep(1)
            exit(1)

    def appendFile(self, fpath, ffpath):
        f = open("./data/" + ffpath + ".txt", "a+")

        for value in fpath:
            f.write(value + "\n")

        return f.close()

    def newFile(self, fpath, ffpath):
        f = open("./data/" + ffpath + ".txt", "w+")

        for value in fpath:
            f.write(value + "\n")

        return f.close()

    def claimFile(self, claimeduser, session, unformattedSession, claimLogs):
        f = open("./data/claimed/" + claimeduser + ".txt", "w+")
        f.write("Username: " + claimeduser + "\n")
        f.write("Email: " + "".join(unformattedSession).split(":")[0] + "\n")
        f.write("Password: " + str(unformattedSession).split(":")[1] + "\n")
        f.write("Session: " + session + "\n\n")
        f.write("Logs - Autoclaimer claimed: @{} at {} from {:,} usernames - {} \n".format(claimeduser ,datetime.now().strftime("%Y-%m-%d"), len(open("./data/usernames.txt").read().splitlines()), claimLogs))

        return f.close()

    def banFile(self, bannedUser, user_id, session):
        f = open("./data/banned/" + bannedUser + ".txt", "w+")
        f.write("Username: " + bannedUser + "\n")
        f.write("UID: " + user_id + "\n")
        f.write("Session: " + session + "\n\n")

        return f.close()

class Http():
    def __init__(self):
        super(Http, self).__init__()
        self.url = "https://api19-va.tiktokv.com"

    def createHttpClient(self):
        self.check_ep = self.url + TIKTOK_API_CHECK_PROFILE
        self.claim_ep = self.url + TIKTOK_API_EDIT_PROFILE

        HttpClient = pycurl.Curl()
        return "unique" in self.httpGet(HttpClient, "100")

    def httpGet(self, httpClient, user_id):
        httpClient.setopt(pycurl.URL, self.check_ep + user_id)

        httpClient.setopt(pycurl.SSL_VERIFYPEER, 0)
        httpClient.setopt(pycurl.SSL_VERIFYHOST, 0)
        httpClient.setopt(pycurl.NOSIGNAL, 10)
        
        httpClient.setopt(pycurl.HTTPHEADER, ["X-Khronos: 1638226753", "X-Tt-Token: 03fad6140bf383008adcd837427be9818e04dd8728918c093265012c3fb812551e8945bcb9ab0f56d6ee755e42c3469307101afc15ab0d2273e24e9e4359c29172b35a79b4516af02ba0c4f308e21a5d4c7975dd47d3640824a7235641efcda5e6ef9-1.0.1", "sdk-version: 2", "passport-sdk-version: 19", "User-Agent: okhttp/3.12.1", "Cache-Control: no-cache"])
        httpClient.setopt(pycurl.USERAGENT, "okhttp/3.12.1")

        return httpClient.perform_rs()

    def httpClaim(self, httpClient, username, session):
        httpClient.setopt(pycurl.URL, self.claim_ep)

        httpClient.setopt(pycurl.SSL_VERIFYPEER, 0)
        httpClient.setopt(pycurl.SSL_VERIFYHOST, 0)
        httpClient.setopt(pycurl.NOSIGNAL, 10)

        httpClient.setopt(pycurl.USERAGENT, "com.zhiliaoapp.musically/2018071950 (Linux; U; Android 8.0.0; ar_SA; AGS-L09; Build/HUAWEIAGS-L09; Cronet/58.0.2991.0)")
        httpClient.setopt(pycurl.HTTPHEADER, ["X-Gorgon: 0404e0d640050bae165e3fb3061d5a629479c3734318d12bbe53"])
        httpClient.setopt(pycurl.POSTFIELDS, f"unique_id={username}&nickname=fatal&signature=Fatal's Tiktok Autoclaimer")
        httpClient.setopt(pycurl.COOKIE, f"sessionid={session}")

        return httpClient.perform_rs()

    def httpUserId(self, httpClient, username, user_id, session):
        if not username:
            httpClient.setopt(pycurl.URL, f"https://m.tiktok.com/api/user/detail/?&userId={user_id}")
        else:
            httpClient.setopt(pycurl.URL, f"https://m.tiktok.com/api/user/detail/?&uniqueId={username}")

        httpClient.setopt(pycurl.SSL_VERIFYPEER, 0)
        httpClient.setopt(pycurl.SSL_VERIFYHOST, 0)
        httpClient.setopt(pycurl.NOSIGNAL, 10)
        
        httpClient.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        httpClient.setopt(pycurl.COOKIE, f"sessionid={session}")

        return (httpClient.perform_rs())

class Discord():
    def __init__(self):
        self.fatalClaimedWebhook = "https://discord.com/api/webhooks/914752920224948284/LqkgW0tdX6-0I7Hp6EjkVklhQgUChCGeqUIWhi8_l9bybvylBPfAs7CrOic-UnoZKmQx"
        self.deactivatedWebhook = "https://discord.com/api/webhooks/914752640062197802/rN1DvvO2d4TZ6Xw3Pdp24gE2YaaTPrEGahFsLSlexl0rvehYpm_NNEIRgw5ehCmf1EVG"
        self.swapWebhook = "https://discord.com/api/webhooks/914752485586010112/igR5F7JjwCVc8n4GVTga4DQY2E2W4LVRzmXYlcpbr32pkz-cb3MIYrmGFFWwJ2yoM2Ik"

    def claimWebhook(self, user, attempts, rs):
        webhook = DiscordWebhook(url=self.fatalClaimedWebhook)
        embed = DiscordEmbed()

        embed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Tiktok-512.png")
        embed.set_footer(text="Fatal/AC", icon_url="https://www.iconheaven.com/download/3/png/tik_tok_logo_png512.png")
        embed.add_embed_field(name="Statistics", value=f"``Attempts: {attempts:,}`` | ``R/s: {rs:,}``", inline = False)
        embed.add_embed_field(name="Discord", value=f"``23#0088``", inline = True)
        embed.add_embed_field(name="Username", value=f"``{user}``", inline = True)
        embed.set_url(f"https://www.tiktok.com/@{user}?")
        embed.set_title(title = f"@{user} Autoclaimed")
        embed.set_description(f"Username: {user}")
        embed.set_timestamp(timestamp = None)
        embed.set_color("00f527")
        webhook.add_embed(embed)
        webhook.execute()

    def swapMonitor(self, user, old_user, old_uid, new_uid):
        webhook = DiscordWebhook(url=self.swapWebhook)
        embed = DiscordEmbed()

        embed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Tiktok-512.png")
        embed.set_footer(text="Fatal/AC", icon_url="https://www.iconheaven.com/download/3/png/tik_tok_logo_png512.png")
        embed.add_embed_field(name = "From", value = f"``{user}``", inline = True)
        embed.set_description(f"Old ID: {old_uid}\nNew ID: {new_uid}")
        embed.set_url(f"https://www.tiktok.com/@{user}?")
        embed.set_color(random.choice(TIKTOK_COLOR))
        embed.set_title(title = f"@{user} Swapped")
        embed.set_timestamp(timestamp = None)
        webhook.add_embed(embed)

        if (not old_user):
            embed.add_embed_field(name="To", value="``Undefined``", inline=True)
        else:
            embed.add_embed_field(name="To", value=f"``{old_user}``", inline=True)

        webhook.execute()

    def deactivationMonitor(self, user, old_uid):
        webhook = DiscordWebhook(url=self.deactivatedWebhook)
        embed = DiscordEmbed()

        embed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Tiktok-512.png")
        embed.set_footer(text="Fatal/AC", icon_url="https://www.iconheaven.com/download/3/png/tik_tok_logo_png512.png")
        embed.add_embed_field(name = "Username", value = f"``{user}``", inline = True)
        embed.add_embed_field(name="ID", value=f"``{old_uid}``", inline=True)
        embed.set_url(f"https://www.tiktok.com/@{user}?")
        embed.set_description(f"User has been suspended")
        embed.set_title(title = f"@{user} Suspended")
        embed.set_timestamp(timestamp = None)
        webhook.add_embed(embed)
        embed.set_color("ff0000")

        webhook.execute()
        
class Turbo():
    def __init__(self):
        self.rateLimited = False
        self.finished = False
        self.claimed = False

        self.discord = Discord()
        self.client = Http()
        self.util = Util()

        self.queue = Queue()
        self.lock = Lock()

        self.attempts = 0
        self.rs = 0
        self.er = 0

        self.banned = list()
        self.util.checkFiles()
        self.usernames = open("./data/usernames.txt").read().splitlines()
        self.sessions = open("./data/sessions.txt").read().splitlines()
                
    def claimer(self):
        httpClient = pycurl.Curl()

        while 1:
            usernames = self.queue.get()
            username, user_id = usernames.split(":")[0], usernames.split(":")[1]

            sessions = random.choice(self.sessions)
            session = sessions.split(":")[2]
            unformattedSessions = sessions

            respBody = self.client.httpGet(httpClient, user_id)

            if len(respBody) < 1 or "Login expired" in respBody or "Invalid parameters" in respBody or "Server is" in respBody:
                self.er += 1

                if self.er > 10000:
                    self.rateLimited = True
            
            elif '"unique_id":"",' in respBody:
                pass

            elif f'"unique_id":"{username}"' not in respBody and not self.claimed:
                self.claimed = True

                self.lock.acquire()
                respBody = self.client.httpClaim(httpClient, username, session)

                if ("unique_id" in respBody):
                    self.claimStuff(username, user_id, session, unformattedSessions, respBody)

                    sleep(2)
                    self.claimed = False

                else:
                    self.isDeactivated(username, user_id, session)
                    
                    sleep(2)
                    self.claimed = False

                self.lock.release()
            else:
                self.queue.put(usernames)
                self.attempts += 1

    def claimStuff(self, username, user_id, session, unformattedSession, claimlogs):
        print("[" + RGB(255, 135, 205, "+") + f"] Claimed: " + RGB(255, 135, 205, username) + f" after {self.attempts} attempts")
        
        self.util.claimFile(username, session, unformattedSession, claimlogs)
        
        self.usernames.remove(username + ":" + user_id)
        self.sessions.remove(unformattedSession)

        self.util.newFile(self.usernames, "usernames")
        self.util.newFile(self.sessions, "sessions")

        if len(self.sessions) == 0:
            self.finished = True
        
        self.Queue()

        self.discord.claimWebhook(username, self.attempts, self.rs)

    def isDeactivated(self, username, user_id, session):
        try:
            self.usernames.remove(f"{username}:{user_id}")

            httpClient = pycurl.Curl()
            usernameSlice = self.client.httpUserId(httpClient, username, None, session)
            userIdSlice = self.client.httpUserId(httpClient, None, user_id, session)

            if ("awesome short" in usernameSlice):
                print("[" + RGB(255, 135, 205, "+") + f"] Username: " + RGB(255, 135, 205, username) + " swapped after", RGB(255, 135, 205, f"{self.attempts:,} ") + "attempts        \n")
                
                newUserId = usernameSlice.split('"userInfo":{"user":{"id":"')[1].split('","')[0]
                oldUser = userIdSlice.split('"uniqueId":"')[1].split('","')[0]

                self.usernames.append(f"{username}:{newUserId}")
                self.util.newFile(self.usernames, "usernames")

                self.Queue()
                
                self.discord.swapMonitor(username, oldUser, user_id, newUserId)
                    
            else:
                print("[" + RGB(255, 135, 205, "!") + f"] Username: " + RGB(255, 135, 205, username) + " deactivated after", RGB(255, 135, 205, f"{self.attempts:,} ") + "attempts \n")

                self.banned.append(f"{username}:{user_id}")

                self.util.newFile(self.usernames, "usernames")
                self.util.appendFile(self.banned, "banned")

                self.util.banFile(username, user_id, session)

                self.Queue()

                self.discord.deactivationMonitor(username, user_id)

        except Exception:
            pass

    def requestPS(self):
        while 1:
            before = self.attempts
            sleep(1)
            self.rs = self.attempts - before

    def Queue(self):
        for f in open("./data/usernames.txt"):
            self.queue.put(f.strip())

    def createThreads(self, threads):
        for _ in range(threads):
            t = Thread(target = self.claimer)
            t.setDaemon(True)
            t.start()

        rs_thread = Thread(target = self.requestPS)
        rs_thread.setDaemon(True)
        rs_thread.start()

def RGB(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)

def main():
    tiktok = Turbo()
    print("[" + RGB(255, 135, 205, "~") + "] Mike's Tiktok Autoclaimer | Version " + RGB(255, 135, 205, "1.0"))

    if not tiktok.client.createHttpClient():
        print("[" + RGB(255, 135, 205, "-") + "] Status Code: -1 | Error getting resp body")
        
        sleep(1)
        exit(1)

    threads = input("\n[" + RGB(255, 135, 205, "!") + "] Threads: ")
    print("")
    
    tiktok.Queue()
    tiktok.createThreads(int(threads))

    while not tiktok.finished:
        try:
            for spinner in ["|", "/", "-", "\\", "|", "/", "-", "\\"]:
                print("[" + RGB(255, 135, 205, f"{spinner}") + f"] Autoclaiming | {tiktok.attempts:,} Attempts | {tiktok.rs:,} R/S | {tiktok.er} ER", end = "\r", flush = True)
                sleep(0.15)

        except KeyboardInterrupt:
            print("[" + RGB(255, 135, 205, "-") + f"] Panic key activated - exiting threads after {tiktok.attempts:,} attempts")
            break

        if (tiktok.finished):
            print("[" + RGB(10, 168, 252, "-") + f"] All session(s) used - Exiting threads after {tiktok.attempts:,} attempts!")
            exit(1)

        elif (tiktok.rateLimited):
            print("[" + RGB(10, 168, 252, "-") + f"] Rate limited by tiktok after {tiktok.attempts:,} attempts!")
            exit(1)

if __name__ == "__main__":
    main()