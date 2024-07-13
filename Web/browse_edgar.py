# open all sections in 10-K
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.remote.webelement import WebElement


def open_sections(driver):
    accordion = driver.find_element(By.ID, "menu")
    sleep(2)
    for kid in accordion.find_elements(By.XPATH, "./li"):
        try:
            if "Financial Statements" == kid.text.strip():
                kid.click()
                sleep(1)
        except:
            continue
    print("done clicking")

def open_income_statement(driver) -> WebElement:
    section = None
    table = None
    for text in ['consolidated statements of income', 'consolidated statements of operations', 'statement of income',
                 'income statements', 'consolidated statements of earnings', 'INCOME STATEMENTS']:
        try:
            section = driver.find_element(By.XPATH, f"//a[text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{text}')]]")
            break
        except:
            continue
    # print(section)
    # if section is None:
    #     accordion = driver.find_element(By.ID, "menu")
    #     section = accordion.find_element(By.XPATH, f"//*[text()[contains(.,'INCOME STATEMENTS')]]")
    if section is None:
        raise Exception("No section found")
    section.click()
    for text in ['Revenue', 'Net income', 'Net income (loss)', 'Operating income', 'Operating income (loss)', 'Revenues']:
        try:
            table = driver.find_element(By.XPATH, f"//*[text()='{text}' and not(contains(@class, 'xbrlviewer'))]/ancestor::tbody[1]")
            break
        except:
            continue
    if not table:
        raise Exception("No table found")
    return table