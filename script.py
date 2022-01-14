from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
import time

GOOGLE_FORM = ''
ZILLOW_URL_WITH_QUERIES = ''
CHROME_DRIVER = Service('')
HEADERS = {
    "Accept-Language": "",
    "User-Agent": ""
}


class RentPricesScraper:
    rent_prices = []
    rent_addresses = []
    rent_urls = []

    def __init__(self, driver, webpage):
        self.driver = webdriver.Chrome(service=driver)
        self.soup = BeautifulSoup(webpage, "html.parser")

    def get_rent_information(self):
        time.sleep(2)
        self.rent_prices = [price.getText() for price in self.soup.select(selector='.list-card-heading .list-card-price')]
        self.rent_addresses = [address.getText() for address in self.soup.select(selector='.list-card-addr')]
        self.rent_urls = [url.get('href') for url in self.soup.find_all(name='a', class_='list-card-link')]
        time.sleep(2)

    def send_rent_information(self):
        for i in range(len(self.rent_addresses)):
            self.driver.get(GOOGLE_FORM)
            time.sleep(2)

            address_field = self.driver.find_element(by='xpath', value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_field = self.driver.find_element(by='xpath', value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            url_field = self.driver.find_element(by='xpath', value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            submit = self.driver.find_element(by='xpath', value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')

            address_field.send_keys(self.rent_addresses[i])
            price_field.send_keys(self.rent_prices[i])
            url_field.send_keys(self.rent_urls[i])
            submit.click()


if __name__ == '__main__':
    response = requests.get(ZILLOW_URL_WITH_QUERIES, headers=HEADERS)
    response_webpage = response.text
    soup = BeautifulSoup(response_webpage, "html.parser")

    scraper = RentPricesScraper(CHROME_DRIVER, response_webpage)
    scraper.get_rent_information()
    scraper.send_rent_information()
