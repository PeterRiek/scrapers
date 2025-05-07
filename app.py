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

def get_items(root_element: WebElement, limit=10):
    href_elements = root_element.find_elements(By.XPATH, '//a[starts-with(@href, "/files/download/")]')
    items = []
    for idx, elem in enumerate(href_elements):
        if limit > 0 and idx >= limit:
            break

        # Start from current element and collect all parent .accordion-item titles
        titles = []
        current_elem = elem
        while True:
            try:
                section = current_elem.find_element(By.XPATH, "./ancestor::*[contains(@class, 'accordion-item')][1]")
                title_elem = section.find_element(By.CSS_SELECTOR, ".accordion-title")
                titles.append(title_elem.get_attribute("textContent").strip())
                current_elem = section  # Move up for next ancestor
            except:
                break  # No more ancestors

        items.append({
            "text": elem.get_attribute("textContent").strip(),
            "url": elem.get_attribute("href"),
            "sections": list(reversed(titles))  # Top-down order
        })

    return items
        
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

if __name__ == "__main__":
        
    driver = webdriver.Chrome(options=options)

    driver.get(LOGIN_URL)
    input("Press enter to navigate to target")

    driver.get(TARGET_URL)

    input("Press enter to index")

    limit = -1

    items = get_items(driver, limit=limit)

    with open("data.json", "w") as jsonfile:
        jsonobj = json.dumps(items, indent=4)
        jsonfile.write(jsonobj)
    

    input("Press enter to download")


    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    for i in items:
        if (is_pdf_link(url=i["url"], session=session)):
            download_folder = os.path.join(DOWNLOAD_FOLDER, i["section"])
            os.makedirs(download_folder, exist_ok=True)
            download_pdf(
                url=i["url"],
                filename=i["text"],
                download_folder=download_folder,
                session=session
            )

    input("Press enter to quit")

    driver.quit()
