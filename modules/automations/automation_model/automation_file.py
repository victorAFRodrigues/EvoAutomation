from modules.automations.dealernet.helpers import login, preenche_capa_nf_servico, preenche_item, preenche_parcelas, preenche_rateio,quit_automation
from modules.core.automation import Automation
from modules.utils.browser_automation import SeleniumElement
from time import sleep
from selenium import webdriver
from datetime import datetime

today = datetime.now()
year, month, day = today.year, today.month, today.day
date = f'{day:02d}{month:02d}{year:04d}'


def execute(data):
    # Define variaveis importantes no inicio da execução
    today = datetime.now()
    year, month, day = today.year, today.month, today.day
    date = f'{day:02d}{month:02d}{year:04d}'

    SE = SeleniumElement

    with Automation() as driver:
        driver.get("https://google.com")
        sleep(255)

if __name__ == "__main__":
    execute('')