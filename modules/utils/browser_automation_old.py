from time import sleep
from random import uniform
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class SeleniumElement:
    """
    Browser Automations:

    Construtor:
        - driver: WebDriver
        - by (str): Tipo de busca ("id", "xpath", "name", "css", "class", "tag")
        - value (str): Valor da busca
        - timeout (int): Tempo de espera em segundos

    Métodos: 
        - find
        - find_many
        - action
    """

    __BY_MAP = {
        "id": By.ID,
        "xpath": By.XPATH,
        "name": By.NAME,
        "css": By.CSS_SELECTOR,
        "class": By.CLASS_NAME,
        "tag": By.TAG_NAME
    }


    def __init__(self, driver, by, value, timeout=2):
        self.__driver = driver
        self.__by = by
        self.__value = value
        self.__timeout = timeout


    def find(self):
        # Faz a busca da propriedade By com base no valor fornecido no construtor
        by = self.__BY_MAP.get(self.__by.lower(), self.__by)
        
        # Tenta encontrar o elemento no contexto atual
        try: 
            if isinstance(self.__driver, WebDriver):
                # then find the element
                element = WebDriverWait(self.__driver, self.__timeout).until(
                    EC.visibility_of_element_located((by, self.__value))
                )

            else:
                element = self.__driver.find_element(by, self.__value)

            return element

        except TimeoutException:
            pass

        iframes = self.__driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            self.__driver.switch_to.frame(iframe)

            try:

                self.__timeout = 0  # evita espera desnecessária em iframes aninhados

                element = self.find()

                if element:
                    # print(f"Elemento: {element} foi encontrado!")
                    return element
            
            except TimeoutException:
                self.__driver.switch_to.parent_frame()
                pass
        
        # Se chegou aqui, não encontrou em lugar nenhum
        raise TimeoutException(f"Elemento: '{self.__value}' não encontrado")

    
    def find_many(self):

        by = self.__BY_MAP.get(self.__by.lower(), self.__by)

        elements_found = []

        try:
            elements = WebDriverWait(self.__driver, self.__timeout).until(
                EC.presence_of_all_elements_located((by, self.__value))
            )
            elements_found.extend(elements)

        except TimeoutException:
            pass

        iframes = self.__driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            self.__driver.switch_to.frame(iframe)

            try:
                self.__timeout = 0
                element = self.find_many()

                if element:
                    elements_found.extend(element)
                    
            except TimeoutException:

                self.__driver.switch_to.parent_frame()

                pass  # não achou nesse iframe, tenta o próximo

        # 3. Se chegou aqui, não encontrou em lugar nenhum
        if elements_found:
            self.__timeout = 2
            return elements_found
        else:
            raise TimeoutException(f"Elemento(s) '{self.__value}' não encontrado(s) em nenhum iframe.")
    
   
    def find_error_msg(self):
        # Faz a busca da propriedade By com base no valor fornecido no construtor
        by = self.__BY_MAP.get(self.__by.lower(), self.__by)
        
        # Tenta encontrar o elemento no contexto atual
        try: 
            if isinstance(self.__driver, WebDriver):
                # then find the element
                element = WebDriverWait(self.__driver, self.__timeout).until(
                    EC.presence_of_element_located((by, self.__value))
                )

            else:
                element = self.__driver.find_element(by, self.__value)

            return element

        except TimeoutException:
            pass

        iframes = self.__driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            self.__driver.switch_to.frame(iframe)

            try:

                self.__timeout = 0  # evita espera desnecessária em iframes aninhados

                element = self.find()

                if element:
                    # print(f"Elemento: {element} foi encontrado!")
                    return element
            
            except TimeoutException:
                self.__driver.switch_to.parent_frame()
                pass

        # Se chegou aqui, não encontrou em lugar nenhum
        raise TimeoutException(f"A o elemento: '{self.__value}' não foi encontrado em nenhum iframe..")


    def action(self, action, text=None):

        element = self.find()

        if element is None:
            print("Element not found, cannot perform action.")
            return False
        
        action = action.lower().strip()
        
        try:
            if action == "click":
                element.click()

            elif action == "write" and text is not None:
                
                element.clear()
                sleep(0.5)
                element.click()

                for char in text:
                    element.send_keys(char)
                    sleep(uniform(0.01, 0.03))

            elif action == "press" and text is not None:
                element.send_keys(text)

            elif action == "void":
                return ""
            
            elif action == "move_to":
                actions = ActionChains(self.__driver)
                actions.move_to_element(element).perform()
            
            else:
                print(f"Unsupported action: {action}")
                return False
            
            return True
        except Exception as e:
            print(f"Error performing {action} on element: {e}")
            return False
        
        finally:
            # A cada ação ele reseta o contexto para o default, o que pode piorar a performance da automação levando em conta que alguns elementos estão no mesmo contexto.

            # self.__driver.switch_to.default_content() 
            pass

class SeleniumBrowserOptions:
    """
    Classe para configurar opções do Selenium WebDriver.
    """
    def __init__(self):
        pass

    def chrome(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        # options.add_argument("--headless=new")
        # options.add_experimental_option("useAutomationExtension", False)

        service = Service()

        return options, service