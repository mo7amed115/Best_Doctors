from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from multiprocessing import Pool
from datetime import datetime
import pandas as pd

data = pd.read_csv('Links.csv')

dic_list = []
url_data = data['urls'].tolist()
url_data = url_data[:50]

def scrape_data(u):
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=capa)
    wait = WebDriverWait(driver, 50)
    driver.get(u)
    time.sleep(3)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[1]/div/div/div/div[1]/div/div/div[2]/h1')))
    driver.execute_script("window.stop();")
    try:
        name = driver.find_element(By.XPATH, '//h1[@itemprop="name"]').text
        special = driver.find_element(By.XPATH, '//div[@class="search-item-info"]').text
    except:
        pass
    try:
        phone = driver.find_element(By.XPATH, '//meta[@itemprop="telephone"]').get_attribute('content')
    except:
        phone = 'Unavailable'
    dic = {"Name": name, 'Speciality': special, 'Phone': phone}
    driver.quit()
    return dic

def process_page(url):
    start_time = datetime.now()
    session_number = url_data.index(url) + 1  # Get the session number based on the index
    print(f"Thread {session_number}: Start")

    dic = scrape_data(url)

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Thread {session_number}: Finish (Duration: {duration})")

    return dic

if __name__ == '__main__':
    pool = Pool(processes=5)
    results = pool.map(process_page, url_data)
    pool.close()
    pool.join()

    df = pd.DataFrame(results)  # Convert the list of dictionaries to a DataFrame
    df.to_csv('output.csv', index=False)  # Save the DataFrame to a CSV file
    print("saved file !")

