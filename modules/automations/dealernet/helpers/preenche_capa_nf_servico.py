from datetime import datetime
from modules.utils.general import Json
from modules.utils.browser_automation import SeleniumElement



def run(driver, data):
    # Define variaveis importantes no inicio da execução
    today = datetime.now()

    year, month, day = today.year, today.month, today.day

    date = f'{day:02d}{month:02d}{year:04d}'

    SE = SeleniumElement

    def click(by, value):
        SE(driver, by, value).action("click")

    def write(by, value, text):
        SE(driver, by, value).action("write", text)
        

    try: 
        # insere uma nova nf
        click("xpath", '//*[@id="INSERT"]')

        # reseta o contexto de visualização do selenium
        driver.switch_to.default_content()

        # preenche linha 1 do formulario
        write("xpath", '//*[@id="vNOTAFISCAL_NUMERO"]', Json(data).get('NUMERO_NF'))
        write("xpath", '//*[@id="vNOTAFISCAL_SERIE"]', Json(data).get('SERIE'))
        write("xpath", '//*[@id="vNOTAFISCAL_DATAMOVIMENTO"]', date)

        # preenche linha 2 do formulario
        write("xpath", '//*[@id="vNOTAFISCAL_DATAEMISSAOD"]', Json(data).get('DATA_EMISSAO'))
        write("xpath", '//*[@id="vNOTAFISCAL_DATACHEGADA"]', date)

        # preenche linha 3 do formulario
        click("css", 'select[id="vNOTAFISCAL_GRUPOMOVIMENTO"] option[value="COM"]')

        # preenche linha 4 do formulario
        write("xpath", '//*[@id="vNOTAFISCAL_PESSOACOD"]', Json(data).get('FORNECEDOR_COD'))
        click("css", 'select[id="vNOTAFISCAL_DEPARTAMENTOCOD"] option[value="'+Json(data).get("DEPARTAMENTO")+'"]')

        # preenche linha 5 do formulario
        click("xpath", '//*[@id="NATOPE"]')
        # driver.switch_to.default_content()
        click("css", 'select[id="vNOTAFISCAL_NATUREZAOPERACAOCOD"] option[value="'+Json(data).get("NATUREZA_OPERACAO")+'"]') # 50 | 18 | 49 | 161
        click("xpath", '//*[@id="CONFIRMAR"]') 
        driver.switch_to.default_content()
        write("xpath", '//*[@id="vNOTAFISCAL_CONTAGERENCIALCOD"]', Json(data).get("CONTA_GERENCIAL"))
        click("css", 'select[id="vNOTAFISCAL_INDICADORPRESENCA"] option[value="0"]')
        driver.switch_to.default_content()

        # preenche linha 6 do formulario
        click('xpath', '//*[@id="TIPODOC"]')
        click("css", 'select[id="vNOTAFISCAL_TIPODOCUMENTOCOD"] option[value="'+Json(data).get("TIPO_DOCUMENTO")+'"]') # 36 | outros
        click("xpath", '//*[@id="CONFIRMAR"]')
        driver.switch_to.default_content()

        # preenche condição de pagamento e agente cobrador
        click("css", 'select[id="vNOTAFISCAL_CONDICAOPAGAMENTOCOD"] option[value="'+Json(data).get("CONDICAO_PAGAMENTO")+'"]')
        driver.switch_to.default_content()
        click("css", 'select[id="vAGENTECOBRADOR_CODIGO"] option[value="10"]')

        # preenche os demais campos da capa da nota
        write("xpath", '//*[@id="vNOTAFISCAL_OBSERVACAO"]', Json(data).get('OBSERVACAO'))
        write("xpath", '//*[@id="vNOTAFISCAL_VALORTOTALDIGITADO"]', Json(data).get('VALOR_TOTAL'))

        if (Json(data).get('CODIGO_VERIFICACAO') != ''):
            write("xpath", '//*[@id="vNOTAFISCAL_CODIGOVERIFICACAO"]', Json(data).get('CODIGO_VERIFICACAO'))

        

        print("Capa da nota preenchida com sucesso!")
        return True
        
    except Exception as e:
        raise Exception(f"Não foi possivel preencher a capa da nota, erro: {e}")
