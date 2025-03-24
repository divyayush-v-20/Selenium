from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from urllib.parse import urljoin, urlparse
import os
from bs4 import BeautifulSoup

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url, driver):
    urls = set()
    domain_name = urlparse(url).netloc
    try:
        driver.get(url)
        time.sleep(2) 
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for a_tag in soup.find_all("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if is_valid(href) and domain_name in href:
                urls.add(href)
        return urls
    except Exception as e:
        print(f"Error getting links from {url}: {e}")
        return urls

def scrape_and_save(url, driver, output_dir):
    try:
        driver.get(url)
        time.sleep(2) 
        soup = BeautifulSoup(driver.page_source, "html.parser")
        text_content = soup.get_text(separator='\n', strip=True) 
        filename = os.path.join(output_dir, urlparse(url).path.replace("/", "_") + ".txt")
        if not filename.endswith(".txt"):
            filename += ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text_content)
        print(f"Scraped and saved: {url} to {filename}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def crawl_and_scrape(start_url, output_dir, max_depth=2): 

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    driver = webdriver.Chrome()
    visited_urls = set()
    urls_to_visit = [(start_url, 0)]  

    while urls_to_visit:
        current_url, depth = urls_to_visit.pop(0)

        if current_url in visited_urls or depth > max_depth:
            continue

        visited_urls.add(current_url)
        scrape_and_save(current_url, driver, output_dir)

        links = get_all_website_links(current_url, driver)
        for link in links:
            if link not in visited_urls:
                urls_to_visit.append((link, depth + 1))

    driver.quit()

# start_url = "https://www.fm99.lt" 
# start_url = "https://kma.kkbox.com/charts/weekly/newrelease?terr=hk&lang=tc&cate=320"
start_url = "https://open.spotify.com/playlist/37i9dQZF1DX2nX8HgBDmgL"
output_directory = "scraped_data"

crawl_and_scrape(start_url, output_directory)
