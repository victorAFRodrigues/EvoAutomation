from modules.automations.dealernet.helpers import login, preenche_capa_nf_produto, preenche_parcelas, preenche_rateio, seleciona_nota, preenche_form_pt1, categoriza_produtos, importar_xml, seleciona_nf_xmltable
from modules.core.automation import Automation
from modules.utils.general import Xml, Json
from time import sleep
from calendar import monthrange
from selenium import webdriver
from datetime import datetime 
from modules.utils.browser_automation import SeleniumBrowserOptions, SeleniumElement



def execute(data):
    with Automation() as driver:
        # Define variaveis importantes no inicio da execução
        json = Json(data)
        xml_nota_path =  Xml(
            json.get("NFEXML_CONTENT"), 
            json.get("NFEXML_FILENAME")
        ).generate() 

        # date
        today = datetime.now()
        year, month = today.year, today.month
        first_month_day = f'01/{month:02d}/{str(year)[-2:]}'
        last_month_day = f'{monthrange(year, month)[1]:02d}/{month:02d}/{str(year)[-2:]}'

        SE = SeleniumElement
        def click(by, value):
            SE(driver, by, value).action("click")

        def write(by, value, text):
            SE(driver, by, value).action("write", text)

        def move_to(by, value):
            SE(driver, by, value).action("move_to")

        try:            
            login.run(driver)

            # direciona para a tela de importar o XML da nota fiscal
            SE(driver, 'xpath', "//button[normalize-space()='Integração']", timeout=5).action("click")
            move_to("xpath", "//span[normalize-space()='XML - Importação']")
            click("xpath", "//span[normalize-space()='Nota Fiscal de Item Avulso']")

            sleep(2)
            
            # roda a automação de importação de XML da nf
            importar_xml.run(driver, xml_nota_path)

            # preenche o campo data emissão inicial e final para filtrar a nota
            write("xpath", '//*[@id="vINTEGRACAOXMLNF_DATAEMISSAOINICIAL"]', json.get('DATA_EMISSAO'))
            write("xpath", '//*[@id="vINTEGRACAOXMLNF_DATAEMISSAOFINAL"]', last_month_day) 
            sleep(4) 
            click('xpath', '//*[@id="IMAGE2"]')     
            driver.switch_to.default_content() 

            # seleciona a nota importada na tabela
            seleciona_nf_xmltable.run(driver, data)

            # roda a automação de categorização dos produtos da nf
            categoriza_produtos.run(driver, data)
            driver.switch_to.default_content() 

            # roda a automação de preenchimento do primeiro formulario de cadastro da nf
            preenche_form_pt1.run(data, driver)
            driver.switch_to.default_content() 

            # direciona para a tela de inserir manualmente a nota fiscal
            click("xpath", "//button[normalize-space()='Produtos']")
            move_to("xpath", "//span[normalize-space()='Nota Fiscal']")
            click("xpath", "//span[normalize-space()='NF Entrada Item Avulso']")

            # filtra e seleciona a nota importada
            write("xpath", '//*[@id="vNOTAFISCAL_NUMERO"]', json.get('NUMERO_NF'))
            click("css", 'select[id="vNOTAFISCAL_STATUS"] option[value="PEN"]')
            click("xpath", '//*[@id="IMGREFRESH"]')
            # driver.switch_to.parent_frame()  
            seleciona_nota.run(driver)

            preenche_capa_nf_produto.run(driver, data)

            preenche_parcelas.run(driver, data)
            driver.switch_to.default_content()

            preenche_rateio.run(driver, data)
            
            SE(driver, "xpath", '//*[@id="CONFIRMA"]', timeout=8).action("click")
            driver.switch_to.default_content()

            success_popup = SE(driver, "css", '#DVELOP_CONFIRMPANELContainer_ConfirmPanel > div.Body', timeout=10)

            if('gerada corretamente com o seguinte status: Pendente.' in success_popup.find().get_property('innerText')):
                # path = '//*[@id="DVELOP_CONFIRMPANELContainer_ConfirmPanel"]/div[3]/span/button'
                path = '#DVELOP_CONFIRMPANELContainer_ConfirmPanel > div.Footer > span > button'
                click('css', path)
                return True, f'A nota fiscal com o id {Json(data).get("NUMERO_NF")} foi inserida com sucesso!'
            
            else:
                return False, "Erro ao cadastrar a nota, verifique os dados e tente novamente."

        except Exception as e:
            return False, f"{e}"


