from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def scrape_blog_details(url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(30)

    while True:
        driver.get(url)
        scroll(driver, 5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        blogs = soup.find_all('article', class_='blog-item')

        data = []
        for blog in blogs:
            title = blog.find('h6').find('a').text
            date = blog.find('div', class_='bd-item').find('span').text
            image_url = blog.find('a', class_='rocket-lazyload')['data-bg']
            likes_count = blog.find('a', class_='zilla-likes').find('span').text

            data.append([title, date, image_url, likes_count])

        with open('blog_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Date", "Image URL", "Likes Count"])
            writer.writerows(data)

        try:
            next_page = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'next page-numbers')))
            url = next_page.get_attribute('href')
        except:
            break

    driver.quit()

def scroll(driver, timeout):
    scroll_pause_time = timeout
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scrape_blog_details('https://rategain.com/blog')
