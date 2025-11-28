# Libs imports
from modules.utils.browser_automation import SeleniumElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep

def run(driver):
    SE = SeleniumElement

    try:
        driver.switch_to.default_content()
        # Pega todas as linhas da tabela
        rows = SE(driver, 'css', '#GridContainerTbl tbody tr', 5).find_many()
        # print(rows)
        sleep(5)

        edit = SE(driver, 'xpath', '//*[@id="vUPDATE_0001"]', 10).find()
        # print(edit)

        for row in rows:
            # print(row.get_attribute('innerHTML'))
            status = SE(row, "css", 'td[colindex="11"] span').find()
            
            if status.get_property('innerHTML').strip().lower() == 'pendente':
                SE(row, "css", 'td[colindex="1"] input').action("click")

                print('nota selecionada, direcionando para a tela de preenchimento da capa da nota...')
                return True
        
        # print("Nenhuma nota 'pendente' estava disponível")
        # return False
        raise Exception("Nenhuma nota 'pendente' estava disponível")

    except NoSuchElementException:
        raise Exception("Estrutura da tabela não encontrada ou alterada.")
        # return False
