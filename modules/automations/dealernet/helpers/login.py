# Libs imports
from modules.utils.general import DotEnv
from modules.utils.browser_automation import SeleniumElement
from time import sleep

# Logic to start/access the application
def run(driver):
    # Define variaveis importantes no inicio da execução
    SE = SeleniumElement

    def click(by, value):
        SE(driver, by, value).action("click")

    def write(by, value, text):
        SE(driver, by, value).action("write", text)

    try: 

        driver.get(DotEnv().get("SYSTEM_URL"))
        # driver.delete_all_cookies()
        # sleep(15)
        # Realiza o login no sistema
        write("xpath", '//*[@id="vUSUARIO_IDENTIFICADORALTERNATIVO"]', DotEnv().get("USER"))
        write("xpath", '//*[@id="vUSUARIOSENHA_SENHA"]', DotEnv().get("PASSWORD"))
        click("xpath", '//*[@id="IMAGE3"]')

        el = SE(driver, "xpath", '//*[@id="W0038TABLECENTRO"]', timeout=5).find() # verifica a tela inicial do sistema
        if not el:
            errText = SE(driver, "xpath", '//*[@id="gxErrorViewer"]/div', timeout=4).find()
            if errText:
                raise Exception(f"{errText.get_property('innerText')}")
            elif "** A senha deverá ter um caracter MAIÚSCULO," in SE(driver, "xpath", '//*[@id="TEXTBLOCK1"]', timeout=5).find().get_property('innerText'): 
                raise Exception(f"Sistema solicita troca de senha.")
            
        driver.switch_to.default_content()

    except Exception as e:
        raise Exception(f"Não foi possivel fazer login no sistema, Erro: {e}")