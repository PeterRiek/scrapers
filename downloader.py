import os
import requests
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import sys
import json


load_dotenv()

LOGIN_URL = "https://blumenwiese.xyz"
TARGET_URL = "https://blumenwiese.xyz/files"
DOWNLOAD_FOLDER = "downloaded_pdfs"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # Suppress most logs: 0 = ALL, 3 = ERROR
options.add_experimental_option("excludeSwitches", ["enable-logging"])

def is_pdf_link(url, session):
    try:
        head = session.head(url, allow_redirects=True, timeout=10)
        content_type = head.headers.get("Content-Type", "")
        return "application/pdf" in content_type.lower()
    except Exception as e:
        print(f"[Check Failed] {url}: {e}")
        return False

def download_pdf(url, filename, download_folder,session):
    try:
        response = session.get(url, stream=True, timeout=15)
        if response.status_code == 200:
            if not filename.lower().endswith(".pdf"):
                filename += ".pdf"
            filepath = os.path.join(download_folder, filename)
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filepath}")
        else:
            print(f"Failed to download {url}")
    except Exception as e:
        print(f"[Download Error] {url}: {e}")


def main():
    driver = webdriver.Chrome(options=options)
    driver.get(LOGIN_URL)
    print("Log in using your browser and afterwards press enter to start.")
    input()
    driver.get(TARGET_URL)

    with open("data.json") as jsonfile:
        data = json.load(jsonfile)

    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    while True:
        print("Enter a section tag for which to start the bulk download.\n(Enter \"exit\" to quit)")
        tag = input()
        if tag == "exit":
            break
        print(f"Starting download for tag: \"{tag}\"...")
        count = 0
        for e in data:
            if tag in e["sections"]:
                if not is_pdf_link(e["url"], session): continue
                download_folder =  os.path.join(DOWNLOAD_FOLDER, *e["sections"])
                os.makedirs(download_folder, exist_ok=True)
                download_pdf(
                    url=e["url"],
                    filename=e["text"],
                    download_folder=download_folder,
                    session=session
                )
                count += 1
        print(f"Done downloading {count} items!")


if __name__ == "__main__":
    main()