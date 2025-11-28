# Libs imports
from time import sleep
from modules.utils.browser_automation import SeleniumElement
from modules.utils.general import Json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

# Logic to quit/close the application
def run(driver, data):
    SE = SeleniumElement
    
    def click(by, value):
        SE(driver, by, value).action("click")

    def write(by, value, text):
        SE(driver, by, value).action("write", text)

    def clickAndWrite(by, value, text, timeout=4):
        el = SE(driver, by, value, timeout).find()
        el.click()
        actions = ActionChains(driver)
        actions.key_down(Keys.SHIFT)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.key_up(Keys.SHIFT)
        actions.perform()
        el.send_keys(text)
    try: 
        
        click('xpath', '//*[@id="ITEMAVULSO"]')
        # driver.switch_to.default_content()
        clickAndWrite('xpath', '//*[@id="vNOTAFISCALITEM_ITEMAVULSOCOD"]', '12', 8)
        
        write('xpath', '//*[@id="vNOTAFISCALITEM_OBSERVACAO"]', Json(data).get('OBSERVACAO')) # write('xpath', '//*[@id="vNOTAFISCALITEM_OBSERVACAO"]', Json(data).get('DESCRICAO'))
        clickAndWrite('xpath', '//*[@id="vNOTAFISCALITEM_CONTAGERENCIALCOD"]', Json(data).get('CONTA_GERENCIAL')) # write('xpath', '//*[@id="vNOTAFISCALITEM_CONTAGERENCIALCOD"]', Json(data).get('CONTA_GERENCIAL'))
        click("css", 'select[id="vNOTAFISCALITEM_DEPARTAMENTOCOD"] option[value="'+Json(data).get("DEPARTAMENTO")+'"]')

        write('xpath', '//*[@id="vNOTAFISCALITEM_QTDE"]', '1') # write('xpath', '//*[@id="vNOTAFISCALITEM_QTDE"]', '1')

        click("css", 'select[id="vNOTAFISCALITEM_UNIDADECOD"] option[value="1"]')

        write('xpath', '//*[@id="vNOTAFISCALITEM_VALORUNITARIO"]', Json(data).get('VALOR_TOTAL')) # write('xpath', '//*[@id="vNOTAFISCALITEM_VALORUNITARIO"]', Json(data).get('VALOR_TOTAL'))
        click('xpath', '//*[@id="CONFIRMAR"]')

        
    except Exception as e:
        raise Exception(f"Não foi possivel cadastrar o item, erro: {e}")
