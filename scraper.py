from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import csv

# Read links
with open("links.txt", "r") as f:
    links = [line.strip() for line in f if line.strip()]

email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

results = []

for url in links:
    print("Checking:", url)
    driver.get(url)
    time.sleep(4)  # wait for JS render

    html = driver.page_source
    emails = set(re.findall(email_pattern, html))

    if emails:
        for e in emails:
            results.append([url, e])
    else:
        results.append([url, "No Email Found"])

driver.quit()

with open("emails.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Email"])
    writer.writerows(results)

print("DONE — emails.csv generated")
