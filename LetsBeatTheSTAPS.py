import os
import re
import sys
import time
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from threading import Thread
from queue import Queue
import subprocess
import random

view = 0

messages = [
    "🎉💻 Nombre de vues depuis le lancement : {view} ! 🥳 On fait chauffer les serveurs de YouTube ! 🔥🚀",
    "🚀✨ {view} vues et ça ne fait que commencer ! INSA en force ! 💪🎬",
    "🔥💃 {view} vues ! Les STAPS commencent à sentir la pression... 🕺✨",
    "🎯📈 {view} vues au compteur ! Vous êtes une machine à gagner ! 🤖🏆",
    "🥳🍿 {view} vues ! On bat les records, une vue à la fois ! 🎬💥",
    "💪🌟 {view} vues déjà ?! On est en route pour la légende ! 📜✨",
    "🚨⚡ {view} vues ! Les STAPS demandent un temps mort... mais on continue ! 🏋️‍♂️🔥",
    "🎬🔄 {view} vues enregistrées ! Le marathon des vidéos ne s’arrête jamais ! 🏃‍♀️📺",
    "📊📈 {view} vues ! Le graphique explose, YouTube est impressionné ! 🤯🔥",
    "💃🔥 {view} vues ! Les algorithmes n’en reviennent pas ! 🤖✨",
    "⚡🎉 {view} vues et la victoire est proche ! Go INSA Rouen ! 🚀🏆",
    "🎥📣 {view} vues ! Le bruit court que YouTube surveille... mais on continue ! 👀🔥",
    "🌟🎯 {view} vues ! INSA = Inspiration Nationale de Succès Automatisé ! 🤖🎖️",
    "🕺💥 {view} vues ! Les STAPS veulent se reconvertir en spectateurs. 🍿👀",
    "⚙️🔧 {view} vues ! Ce script est un chef-d'œuvre, tout comme INSA ! 💻🏅",
    "🤖📢 {view} vues ! On fait travailler les processeurs et les points montent ! 💥⚡",
    "🔥🏋️ {view} vues ! YouTube appelle à l’aide... trop de succès ! 📞💻",
    "🎉📺 {view} vues ! Les STAPS peuvent déjà préparer leurs excuses. 🤭🏆",
    "🎯🎬 {view} vues ! On joue dans la ligue des champions. 🚀✨",
    "🚀💥 {view} vues au compteur et toujours en pleine montée ! Go INSA Rouen ! 🏆💙"
]

def afficher_message(view):
    global messages
    message = random.choice(messages)  # Sélectionne un message aléatoire
    print(message.format(view=view))

def get_edge_version():
    """Get the version of the installed Microsoft Edge browser."""
    print("🔍 Checking your Edge browser version...")
    try:
        output = subprocess.check_output(
            ["reg", "query", r"HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon", "/v", "version"],
            text=True
        )
        version_match = re.search(r"version\s+REG_SZ\s+([\d\.]+)", output)
        if version_match:
            version = version_match.group(1)
            print(f"💻 Edge version detected: {version}")
            return version
        else:
            raise ValueError("Unable to determine Edge version.")
    except Exception as e:
        print(f"❌ Error detecting Edge version: {e}")
        sys.exit(1)

def download_edge_driver(browser_version):
    """Download the appropriate Edge WebDriver for the given browser version."""
    print("📡 Preparing to download the Edge WebDriver...")
    major_version = browser_version.split('.')[0]
    driver_version_url = f"https://msedgedriver.azureedge.net/LATEST_RELEASE_{major_version}"
    try:
        # Fetch the exact driver version
        response = requests.get(driver_version_url)
        response.raise_for_status()
        driver_version = response.text.strip()
        print(f"🔧 Matching WebDriver version: {driver_version}")

        # Construct the download URL
        driver_url = f"https://msedgedriver.azureedge.net/{driver_version}/edgedriver_win64.zip"
        driver_zip = "edgedriver.zip"
        extract_path = "./edgedriver_win64"

        # Download the WebDriver
        print("⬇️ Downloading the WebDriver... Hang tight!")
        response = requests.get(driver_url, stream=True)
        response.raise_for_status()
        with open(driver_zip, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Extract the WebDriver
        with zipfile.ZipFile(driver_zip, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        os.remove(driver_zip)  # Clean up
        print("✅ WebDriver is ready to roll!")
        return os.path.join(extract_path, "msedgedriver.exe")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading WebDriver: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error extracting WebDriver: {e}")
        sys.exit(1)

# Queue to manage the video URLs
youtube_urls = [
    "https://www.youtube.com/watch?v=xElhqTDMaRc&t",
    "https://www.youtube.com/watch?v=xElhqTDMaRc&t",
    "https://www.youtube.com/watch?v=xElhqTDMaRc&t",
]

url_queue = Queue()
for url in youtube_urls:
    url_queue.put(url)

def run_session(session_id, edge_driver_path):
    """Run a session for the contest."""
    while True:
        if not url_queue.empty():
            youtube_url = url_queue.get()
            edge_options = Options()
            edge_options.add_argument("--start-maximized")
            edge_options.add_argument("--disable-blink-features=AutomationControlled")

            service = Service(edge_driver_path)
            driver = webdriver.Edge(service=service, options=edge_options)

            try:
                print(f"🎥 Session {session_id}: Starting video {youtube_url}")

                driver.get("https://www.youtube.com")
                socs_cookie = {
                    "name": "SOCS",
                    "value": "CAESEwgDEgk0ODE3Nzk3MjQaAmVuIAEaBgiA_LyaBg",
                    "domain": ".youtube.com",
                    "path": "/"
                }
                driver.add_cookie(socs_cookie)
                driver.get(youtube_url)

                time.sleep(5)

                try:
                    play_button = driver.find_element(By.CLASS_NAME, "ytp-play-button")
                    play_button.click()
                except Exception:
                    print(f"🟢 Session {session_id}: Video is playing.")

                time.sleep(130)
            finally:
                print(f"💨 Session {session_id}: Wrapping up.")
                global view
                view = view + 1
                afficher_message(view)

                driver.quit()
                url_queue.put(youtube_url)
        else:
            print(f"❓ Session {session_id}: No videos found in the queue.")
            time.sleep(10)

def launch_sessions(edge_driver_path):
    for i in range(3):
        time.sleep(i * 45)
        thread = Thread(target=run_session, args=(i + 1, edge_driver_path))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    print("🚀 Let's beat the STAPS!")
    edge_version = get_edge_version()
    edge_driver_path = download_edge_driver(edge_version)
    launch_sessions(edge_driver_path)

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print("🏁 Contest paused. See you at the finish line!")
