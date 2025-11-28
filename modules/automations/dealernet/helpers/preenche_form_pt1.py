from time import sleep
from modules.utils.browser_automation import SeleniumElement
from modules.utils.general import Json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def run(data, driver):
    SE = SeleniumElement

    def click(by, value):
        SE(driver, by, value).action("click")

    def write(by, value, text):
        SE(driver, by, value).action("write", text)

    try:
        
        # grupo de movimento:
        click("css", 'select[id="vNOTAFISCAL_GRUPOMOVIMENTO"] option[value="COM"]')

        # natureza de operação:
        click("xpath", '//*[@id="NATOPE"]')
        click("css", f'select[id="vNOTAFISCAL_NATUREZAOPERACAOCOD"] option[value="{Json(data).get("NATUREZA_OPERACAO")}"]')
        click("xpath", '//*[@id="CONFIRMAR"]')

        # reseta o contexto de visualização do selenium
        driver.switch_to.default_content()

        # tipo de pessoa:
        click('css', 'select[id="vPESSOA_TIPOPESSOA"] option[value="J"]')

        # tipo de documento:
        click("xpath", '//*[@id="TIPODOC"]')
        click("css", f'select[id="vNOTAFISCAL_TIPODOCUMENTOCOD"] option[value="{Json(data).get("TIPO_DOCUMENTO")}"]')
        click("xpath", '//*[@id="CONFIRMAR"]')

        # reseta o contexto de visualização do selenium
        driver.switch_to.default_content()
        
        # demais campos:
        write("css", 'input[id="vNOTAFISCAL_CONTAGERENCIALCOD"]', Json(data).get('CONTA_GERENCIAL')),
        click("xpath", f'//option[normalize-space()="{Json(data).get("DEPARTAMENTO")}"]')
        click("css", f'select[id="vNOTAFISCAL_CONDICAOPAGAMENTOCOD"] option[value="36"]')
        click("css", f'select[id="vAGENTECOBRADOR_CODIGO"] option[value="10"]') 
        click("xpath", '//*[@id="vISUTILIZAREGRATRIBUTOICMSPISCOFINS"]')   
        click("xpath", '//*[@id="IMGPROCESSAR"]')
        sleep(4)
        err = SE(driver, 'xpath', '//*[@id="gxErrorViewer"]/div[1]', timeout=10).find_error_msg()
       
        err_msg = err.get_property('innerHTML').strip()

        if(err_msg == 'Nota Fiscal Processada com Sucesso'):
            print('Primeira parte do formulário de preenchimento da nota concluído!')
            return True
        
    except Exception as e:
            raise Exception(f"Não foi possivel preencher o formulário, erro: {e}")