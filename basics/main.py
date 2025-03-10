from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
# driver.get(f"https://www.amazon.in/s?k=macbook&crid=OMT4TP52VB7&sprefix=macboo%2Caps%2C706&ref=nb_sb_noss_2")
# driver.get("https://fm99.lt/top-10/")
driver.get("https://charts.spotify.com/home")

# elem = driver.find_element(By.CLASS_NAME, "puisg-row")
elem = driver.find_element(By.CLASS_NAME, "ChartsHomeEntries__Title-kmpj2i-2 jCURRv")
print(elem.text)

# print(driver.title)

time.sleep(1)
driver.close()