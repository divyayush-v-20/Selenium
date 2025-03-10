from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "https://www.netflix.com/tudum/top10"

driver = webdriver.Chrome()
driver.get(url)

target_class = "td.title span.rank"

try:
    elems = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, target_class))
    )

    for elem in elems:
        content = elem.find_element(By.XPATH, "..")
        print(content.text)

except Exception as e:
    print(f"Error: {e}")


time.sleep(2)
driver.close()