import requests
import bs4
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service



ZILLOW_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22usersSearchTerm%22%3A%22Tulsa%2C%20OK%22%2C%22mapBounds%22%3A%7B%22west%22%3A-96.34433682247351%2C%22east%22%3A-95.39676602169226%2C%22south%22%3A35.68402987816865%2C%22north%22%3A36.41018987853664%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D"

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc1LMXWv4_DZoD9Vrjy6JzDnjaDzAcN-ZfJHjYKbfRCj1oDig/viewform?usp=sf_link"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service("/Users/ethanwilliams/Development/chromedriver_mac_arm64/chromedriver")
driver = webdriver.Chrome(options=chrome_options)

headers = {
  "Accept-Language": "en-US,en;q=0.9",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
response = requests.get(ZILLOW_URL, headers=headers)
zillow_webpage = response.text
soup = bs4.BeautifulSoup(zillow_webpage, "html.parser")

links = []
prices = []
addresses = []

web_links = soup.find_all(name="a", class_="property-card-link")
web_prices = soup.find_all(name="span", class_="srp__sc-16e8gqd-1 jLQjry")
web_addersses = soup.find_all(name="address")


for idx, link in enumerate(web_links):
  if idx % 2 == 0:
    tail = link.get("href")
    links.append(f"https://www.zillow.com{tail}")

for price in web_prices:
  curr_price = price.getText().split("+")[0]
  prices.append(curr_price)

for address in web_addersses:
  addresses.append(address.getText())

print(len(links))
print(len(prices))
print(len(addresses))

for idx in range(len(links)):
  driver.get(GOOGLE_FORM_URL)
  time.sleep(3)
  link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
  price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
  address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')

  address_input.send_keys(addresses[idx])
  price_input.send_keys(prices[idx])
  link_input.send_keys(links[idx])

  submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
  submit_button.click()

