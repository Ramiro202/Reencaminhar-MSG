
from os import system
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService



dados = {} 
class WhatsApp:
    def __init__(self) -> None:
        chrome_options = Options()
        self.url = "https://web.whatsapp.com/"

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-cache")
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--user-data-dir=selenium")
        chrome_options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 20)

    @staticmethod
    def paste_content(driver, el, content):
        # Para colar o conteudo 
        driver.execute_script(
            f'''
            const text = `{content}`;
            const dataTransfer = new DataTransfer();
            dataTransfer.setData('text', text);
            const event = new ClipboardEvent('paste', {{
            clipboardData: dataTransfer,
            bubbles: true
            }});
            arguments[0].dispatchEvent(event)
            ''',
            el)
    
    def start(self) -> None:

        self.driver.get(self.url)
        while len(self.driver.find_elements(By.XPATH, "//div[@id='side']")) < 1:
            sleep(2)
        print("!BOT ESTÁ ONLINE!")
    
    def mandar_mensagem(self, msg):
        # Pega todos os grupos que fazes parte
        grupos = self.driver.find_elements(
            By.XPATH, "//div[@class='lhggkp7q ln8gz9je rx9719la']")
        for num, grupo in enumerate(grupos):
            nome = grupo.find_elements(By.XPATH, "//div[@class='_21S-L']")[num]
            # print(nome.text)

            if nome.text == "RamirOo Ngando":
                # print(f"Grupo => {nome.text} encontrado")

                grupo.click()
                message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
                message_box = self.wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))

                self.paste_content(self.driver, message_box, msg)
                # Adicione uma pausa de 0.5 segundo entre as linhas
                sleep(0.5)
                 # Envie a mensagem
                message_box.send_keys(Keys.ENTER)
        sleep(2)
        # Atualizar a página
        # self.driver.refresh()
    
    def tem_nova_msg(self):
        grupos = self.driver.find_elements(
            By.XPATH, "//div[@class='lhggkp7q ln8gz9je rx9719la']")
        for num, grupo in enumerate(grupos):
            nome = grupo.find_elements(By.XPATH, "//div[@class='_21S-L']")[num]

            if nome.text == "RamirOo Ngando":
                print(f"Grupo => {nome.text} encontrado")

                spans = nome.find_elements(By.XPATH, "//span[@class='aprpv14t']")[num]
                
                if spans:
                    # Obtenha a cor do texto
                    cor_do_texto = spans.value_of_css_property('color')
                    # print(f'A cor do texto é: {cor_do_texto}')
                    return True
