# Libs imports
from modules.utils.browser_automation import SeleniumElement
from selenium.common.exceptions import NoSuchElementException
from modules.utils.general import Json

# Logic to quit/close the application
def run(driver, data):
    SE = SeleniumElement

    nf_file_name = Json(data).get("NFEXML_FILENAME")
    nf_file_name = nf_file_name.replace('.xml','')

    try:
        # Pega todas as linhas da tabela
        # rows = SE(driver, "xpath", '//*[@id="GridIntxmlContainerTbl"]/tbody/tr', 3).find_many()
        # Anteriormente estava com id GridIntxmlContainerTbl

        rows = SE(driver, "xpath", '//*[@id="GridxmlContainerTbl"]/tbody/tr', 10).find_many()
        print(rows)

        SE(driver, 'xpath', '//*[@id="span_vINTEGRACAOXMLNF_CLIENTE_0001"]', 10).find()
        
        for row in rows:
            file_name_col = SE(row, "css", 'td[colindex="6"] span').find()
            
            if nf_file_name in file_name_col.get_property('innerHTML'):
                SE(row, "css", 'td[colindex="10"] a img[title="Atualizar dados Itens Avulsos da NF"]').action('click')
                print(f"XML encontrado e selecionado: {nf_file_name}")
                return True
        
        print(f"Nenhum XML encontrado com o nome: {nf_file_name}")
        return False

    except NoSuchElementException:
        print("Estrutura da tabela não encontrada ou alterada.")
        return False
    
