# Libs imports
from json import dumps
from random import randint, uniform
from time import sleep
from modules.utils.browser_automation import SeleniumElement
from selenium.common.exceptions import NoSuchElementException

# Logic to quit/close the application
def run(driver):
    SE = SeleniumElement

    def get(driver, by, value):
        return SE(driver, by, value).find().get_property('innerHTML')

    try:
        # Pega todas as linhas da tabela
        row = SE(driver, 'xpath', '//*[@id="GridContainerRow_0001"]', 5).find()

        # driver.switch_to.default_content()
        # verifica se a linha existe
        if row:
            payload = dumps([
                {
                    "Nome" : "cod_fornecedor", 
                    "Conteudo" : get(row, "css", 'td[colindex="2"] span').strip()
                },
                {
                    "Nome" : "nome_fantasia", 
                    "Conteudo" : get(row, "css", 'td[colindex="4"] span').strip()
                }
            ])
            return payload
        
    except NoSuchElementException:
        print("nenhum fornecedor encontrado.")
        return False
