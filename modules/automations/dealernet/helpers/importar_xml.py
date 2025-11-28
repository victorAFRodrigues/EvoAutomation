

from time import sleep
# from modules.utils_old import selenium_element_action, selenium_find_element, selenium_move_to_element
from modules.utils.browser_automation import SeleniumElement




def run(driver, xml_nota_path):
    SE = SeleniumElement
    def click(by, value):
        SE(driver, by, value).action("click")
        
    click('xpath', '//*[@id="IMAGE1"]')
    # driver.switch_to.default_content()
    # click('xpath', '//*[@id="IMAGE2"]')
    sleep(5)
    SE(driver, 'xpath', '//*[@id="IMAGE2"]', 15).action("click")
    # print(xml_nota_path)
    el = SE(driver, 'xpath', '//*[@id="uploadfiles"]', 7).find()
    # print(el)
    el.send_keys(xml_nota_path)

    # # driver.switch_to.default_content()
    # SE(driver, 'xpath', '//*[@id="uploadfiles"]', 7).action('write', xml_nota_path)

    # reseta o contexto de visualização do selenium
    driver.switch_to.default_content()
    click('xpath', '//*[@id="TRN_ENTER"]')

    msg = SE(driver, 'xpath', '//*[@id="TEXTBLOCKDOWNLOAD"]/a/text', 5).find()

    if msg.get_property('innerHTML') != 'Arquivos processados 1 de 1. Clique aqui para Visualizar':
        raise Exception('Arquivo invalido, cancelando execução...')
    
    click('xpath', '//*[@id="TRN_CANCEL"]')

    print('Importação de NFe concluída!')