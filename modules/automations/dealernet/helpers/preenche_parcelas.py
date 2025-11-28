from selenium.common.exceptions import NoSuchElementException
from modules.utils.browser_automation import SeleniumElement
from modules.utils.general import Json
from time import sleep

def run(driver, data):
    SE = SeleniumElement

    def click(by, value):
        SE(driver, by, value).action("click")


    try:
        click("xpath", '//*[@id="PARCELA"]')
        click("xpath", '//*[@id="INSERT"]')
        # driver.switch_to.default_content()
        # popup = SE(driver, "xpath", '//*[@id="gxp0_b"]', 20).find()
        # print(popup)
        i = 0

        parcelas = Json(data).get('PARCELAS')

        for pItem in parcelas:
            sleep(1)
            print(f"Preenchendo parcela {i + 1} de {len(parcelas)}")
            parcela = Json(pItem["Conteudo"])
            
            # encontra as linhas da tabela de parcelas
            rows = SE(driver, "xpath", '//*[@id="GridparcelaContainerTbl"]/tbody/tr', 20).find_many() # SE(table, "css", 'tr').find_many()
              
            # preenche os campos da parcela
            SE(rows[i], "css", 'td[colindex="17"] div input').action("write", parcela.get('data_vencimento'))
            SE(rows[i], "css", 'td[colindex="19"] input').action("write", parcela.get('valor'))
            SE(rows[i], "css", 'td[colindex="20"] select option[value="'+parcela.get('tipo_titulo')+'"]').action("click")


            # verfica se há mais de uma parcela para cadastrar
            if len(parcelas) > 1 and i < len(parcelas) - 1:
                i += 1

                # clica para inserir uma nova parcela
                click("xpath", '//*[@id="INSERT"]')
                print('rodando processo de cadastro de parcelas novamente...')
                
        click("xpath", '//*[@id="BTNCONFIRMAR"]')
        print('parcelas cadastradas com sucesso!')
        return True

    except NoSuchElementException:
        print("Estrutura da tabela não encontrada ou alterada.")
        return False
    

    
