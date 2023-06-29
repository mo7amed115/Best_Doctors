from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from multiprocessing import Pool
from datetime import datetime

options = webdriver.ChromeOptions()

# Set options
# options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
# options.add_argument("--disable-gpu")  # Disable GPU acceleration

def scrape_links(page):
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    links = []
    driver = webdriver.Chrome(options=options , desired_capabilities=capa )
    wait = WebDriverWait(driver, 40)
    u = f'https://www.ratemds.com/best-doctors/ast/assiut/chiropractor/?page={page}'
    driver.get(u)
    time.sleep(3)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/div/div[4]/div[1]/div/div[1]/span[2]/a[1]')))
    driver.execute_script("window.stop();")
    link = driver.find_elements(By.XPATH , '//a[@class = "search-item-doctor-name"]')
    for i in link:
        links.append(i.get_attribute("href"))
    driver.quit()
    return links

def process_page(page):
    start_time = datetime.now()
    print(f"Thread {page}: Start")

    links = scrape_links(page)

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Thread {page}: Finish (Duration: {duration})")
    
    return links

if __name__ == '__main__':
    x = input('Enter The Num of Pages : ')
    pages = range(1, int(x)+1)
    pool = Pool(processes=3)  # Create a pool of 5 processes
    results = pool.map(process_page, pages)  # Execute the function concurrently for each page
    pool.close()
    pool.join()

    all_links = [link for result in results for link in result]
    print(f"the Number of Links: {len(all_links)} \n")
    # Save links to a CSV file using pandas
    df = pd.DataFrame({'Link': all_links})
    csv_file = 'links.csv'
    df.to_csv(csv_file, index=False)

    print(f"Links saved to {csv_file}")
    
    
