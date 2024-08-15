# open all sections in 10-K
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.remote.webelement import WebElement


def open_sections(driver):
    accordion = driver.find_element(By.ID, "menu")
    sleep(1)
    for kid in accordion.find_elements(By.XPATH, "./li"):
        try:
            if "Financial Statements" == kid.text.strip():
                kid.click()
                sleep(1)
        except:
            continue

def open_income_statement(driver) -> WebElement | None:
    section = None
    table = None
    for text in ['consolidated statements of income', 'consolidated statements of operations', 'statement of income',
                 'income statements', 'consolidated statements of earnings', 'INCOME STATEMENTS',
                 'consolidated statement of earnings', 'consolidated statement of operations',
                 'consolidated statement of income',
                 ]:
        try:
            section = driver.find_element(By.XPATH, f"//a[text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{text}')]]")
            break
        except:
            continue
    if section is None:
        print('No section found')
        # Has to be last. AYI has statement under this, but most have some other stuff we don't want
        fallback = 'consolidated statements of comprehensive income'
        try:
            section = driver.find_element(By.XPATH, f"//a[text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{fallback}')]]")
            print("Using fallback. Check if it is correct data")
        except:
            print("Fallback failed")
            return None

    section.click()
    for text in ['Revenue', 'Net income', 'Net income (loss)', 'Operating income', 'Operating income (loss)',
                 'Revenues', 'Revenues:', 'Total Revenue', 'Total revenue', 'Net revenue', 'Net revenues', 'Net Revenues', 'Net Revenue',
                 'Net sales', 'Net sales:', 'Net Sales',
                 'Net Sales:', 'Gross profit', 'Gross Profit']:
        try:
            table = driver.find_element(By.XPATH, f"//*[text()='{text}' and not(contains(@class, 'xbrlviewer'))]/ancestor::tbody[1]")
            break
        except:
            continue
    if not table:
        raise Exception("No table found")
    return table