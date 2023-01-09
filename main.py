from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('enable-automation')
options.add_argument('--disable-browser-side-navigation')
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--log-level=3')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
url = 'https://statusinvest.com.br/acoes/petr4'

driver.get(url)