from modules.automations.dealernet.helpers import login, preenche_capa_nf_servico, preenche_item, preenche_parcelas, preenche_rateio
from modules.core.automation import Automation
from modules.utils.browser_automation import SeleniumElement
from datetime import datetime

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

        def move_to(by, value):
            SE(driver, by, value).action("move_to")


        try:
            login.run(driver)

            # direciona para a tela de inserir manualmente a nota fiscal
            click("xpath", "//button[normalize-space()='Produtos']")
            move_to("xpath", "//span[normalize-space()='Nota Fiscal']")
            click("xpath", "//span[normalize-space()='NF Entrada Item Avulso']")

            preenche_capa_nf_servico.run(driver, data)

            preenche_item.run(driver, data)
            
            preenche_parcelas.run(driver, data)

            driver.switch_to.default_content()

            preenche_rateio.run(driver, data)

            SE(driver, "xpath", '//*[@id="CONFIRMA"]', timeout=8).action("click")
            driver.switch_to.default_content()

            success_popup = SE(driver, "css", '#DVELOP_CONFIRMPANELContainer_ConfirmPanel > div.Body', timeout=10)
            popup_msg = success_popup.find().get_property('innerText')
            if('gerada corretamente com o seguinte status: Pendente.' in popup_msg):
                # path = '//*[@id="DVELOP_CONFIRMPANELContainer_ConfirmPanel"]/div[3]/span/button'
                path = '#DVELOP_CONFIRMPANELContainer_ConfirmPanel > div.Footer > span > button'
                click('css', path)
                return True, f"A nota fiscal com o id {Json(data).get('NUMERO_NF')} foi inserida com sucesso!"
            
            else:
                return False, "Erro ao cadastrar a nota, verifique os dados e tente novamente."

        except Exception as e:
            print(f"An error occurred: {e}")


