from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-extensions')
options.add_argument('enable-automation')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
# options.add_argument('--log-level=3')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
url = 'https://statusinvest.com.br/acoes/bbas3'

driver.get(url)

sleep(3)

acao = driver.find_element(By.XPATH, '//*[@id="main-header"]/div[2]/div/div[1]/div/ol/li[3]/a/span')
pl = driver.find_element(By.XPATH, '//*[@id="indicators-section"]/div[2]/div/div[1]/div/div[4]/div/div/strong')
cotacao = driver.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div/div[1]/div/div[1]/div/div[1]/strong')
dy = driver.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div/div[1]/div/div[4]/div/div[1]/strong')

print(f'{acao.text}\nValor atual: {cotacao.text}\nD.Y%: {dy.text}\nP/L: {pl.text}')
