from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-extensions')
# options.add_argument('enable-automation')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
options.add_argument('--log-level=3')

service = Service(ChromeDriverManager().install())


class WebscrapingInvest():
    def __init__(self, ativo):
        self.driver = webdriver.Chrome(service=service, options=options)
        self.ativo = ativo.lower()
        self.url_acao = 'https://statusinvest.com.br/acoes/'
        self.url_fundo = 'https://statusinvest.com.br/fundos-imobiliarios/'
        self.url = ''

    def is_fii(self):
        return self.ativo[-2::] == '11'
    
    def is_acao(self):
        return self.ativo[-1::] == '4' and not self.is_fii()

    def get_info(self):
        self.url = self.url_fundo + self.ativo if self.is_fii() else self.url_acao + self.ativo
        self.driver.get(self.url)
        sleep(1)
        if self.is_acao():
            acao = self.driver.find_element(By.XPATH, '/html/body/main/header/div[2]/div/div[1]/h1')
            pvp = self.driver.find_element(By.XPATH, '//*[@id="indicators-section"]//h3[contains(text(), "P/VP")]/../../div//strong')
            pl = self.driver.find_element(By.XPATH, '//*[@id="indicators-section"]//h3[contains(text(), "P/L")]/../../div//strong')
            cotacao = self.driver.find_element(By.XPATH, '//h3[contains(text(), "Valor atual")]/../../div//strong')
            dy = self.driver.find_element(By.XPATH, '//*[@id="indicators-section"]//h3[contains(text(), "D.Y")]/../../div//strong')
        
            return {
                'tipo': 'acao',
                'acao': acao.text,
                'cotacao': cotacao.text,
                'dy': dy.text,
                'pvp': pvp.text,
                'pl': pl.text
            }
        if self.is_fii():
            fundo = self.driver.find_element(By.XPATH, '//*[@id="main-header"]/div[2]/div/div[1]/h1')
            dy = self.driver.find_element(By.XPATH, '//h3[contains(text(), "Dividend Yield")]/../../div//strong')
            pvp = self.driver.find_element(By.XPATH, '//h3[contains(text(), "P/VP")]/../../div//strong')
            cotacao = self.driver.find_element(By.XPATH, '//h3[contains(text(), "Valor atual")]/../../div//strong')

            return {
                'tipo': 'fii',
                'cotacao': cotacao.text,
                'fundo': fundo.text,
                'dy': dy.text,
                'pvp': pvp.text
            }
        return None
    
    def close(self):
        self.driver.close()