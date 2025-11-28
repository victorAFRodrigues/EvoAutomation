from modules.automations.dealernet.helpers import login, procura_fornecedor
from modules.core.automation import Automation
from modules.utils.browser_automation import SeleniumElement
from datetime import datetime
from time import sleep
from json import dumps
from modules.utils.general import Json


# Define variaveis importantes no inicio da execução
today = datetime.now()
year, month, day = today.year, today.month, today.day
date = f'{day:02d}{month:02d}{year:04d}'
SE = SeleniumElement


def execute(data):
    with Automation() as driver:
        def click(by, value):
            SE(driver, by, value).action("click")
            
        def write(by, value, text):
            SE(driver, by, value).action("write", text)

        try:
            login.run(driver)

            # direciona para a tela de inserir manualmente a nota fiscal
            click("xpath", "//button[normalize-space()='Cadastro']")
            click("xpath", "//span[normalize-space()='Pessoas']")
            driver.switch_to.default_content()

            # preenche os campos do filtro
            CNPJ = Json(data).get('CNPJ')
            print(f"Validando fornecedor com CNPJ: {CNPJ}")
            # click('xpath', '//*[@id="vPESSOA_TIPOPESSOA"]/option[3]')  # seleciona pessoa juridica (Em alguns casos não funciona pois o cliente não está cadastrado como juridico, deixei comentado mas é recomendado usar)
            write('xpath', '//*[@id="vPESSOA_DOCIDENTIFICADOR"]', f"{CNPJ}")  #"68774017002244")
            click('xpath', '//*[@id="IMGREFRESH"]')
            sleep(10)
            click('xpath', '//*[@id="IMGREFRESH"]')
            sleep(2)

            # driver.switch_to.default_content()
            Fdata = procura_fornecedor.run(driver)
            if(Fdata):
                return True, Fdata
            else:
                return False,  dumps([
                {
                    "Nome" : "cod_fornecedor", 
                    "Conteudo" : "0"
                },
                {
                    "Nome" : "nome_fantasia", 
                    "Conteudo" : "Nenhum fornecedor encontrado"
                }
            ])

        except Exception as e:
            return False, f"{e}"

