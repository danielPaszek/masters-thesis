# open all sections in 10-K
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.remote.webelement import WebElement


def open_sections(driver):
    try:
        accordion = driver.find_element(By.ID, "menu")
    except:
        print("SOMETHING WENT WRONG!!!!!!!!")
        print(driver.current_url)
        print("UWAGA!!!!!!!!!!!!!!!!!!!!")
        return False

    sleep(1)
    clicked = 0
    for kid in accordion.find_elements(By.XPATH, "./li"):
        try:
            if "Financial Statements" == kid.text.strip():
                kid.click()
                clicked += 1
                sleep(1)
        except:
            continue
    if clicked != 0:
        return True

    for kid in accordion.find_elements(By.XPATH, "./li"):
        try:
            if "Reports" == kid.text.strip():
                kid.click()
                clicked += 1
                sleep(1)
        except:
            continue
    if clicked != 0:
        return True
    print("No financial statements found")
    return False

def open_income_statement(driver) -> WebElement | None:
    section = None
    table = None
    for text in [
        'consolidated statements of operations and comprehensive income (loss)',
        'consolidated statements of income', 'consolidated statements of operations',
        'consolidated statement of earnings', 'consolidated statement of operations',
        'consolidated statement of income', 'statement of consolidated operations',
        'statements of consolidated earnings',
        'income statements', 'consolidated statements of earnings',
        'INCOME STATEMENTS', 'statement of income',
        'consolidated results of operations',
                 ]:
        try:
            section = driver.find_element(By.XPATH,
                                          f"//a[text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{text}')]]")
            break
        except:
            continue
    if section is None:
        print('No section found')
        # Has to be last. AYI has statement under this, but most have some other stuff we don't want
        fallback = 'consolidated statements of comprehensive income'
        try:
            section = driver.find_element(By.XPATH,
                                          f"//a[text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{fallback}')]]")
            print("Using fallback. Check if it is correct data")
        except:
            print("Fallback failed")
            return None

    section.click()
    for text in [
        'Revenue', 'Net income', 'Net income (loss)', 'Operating income', 'Operating income (loss)',
        'Revenues', 'Revenues:', 'Total Revenue', 'Total Revenues', 'Total revenue', 'Total revenues',
        'Total sales', 'Total Sales', 'Total sales:', 'Total Sales:'
        'Net revenue', 'Net revenues', 'Net Revenues', 'Net Revenues:',
        'Net Revenue', 'Net sales', 'Net sales:', 'Net Sales',
        'Cost of Sales', 'Cost of sales', 'Cost of Sales:', 'Cost of sales:',
        'Operating Revenues', 'Operating Revenues:', 'Operating revenues', 'Operating revenues:',
        'Net Sales:', 'Gross profit', 'Gross Profit', 'Total non-interest revenues', 'Total non-interest Revenues',
        'Earnings per Common Share', 'Earnings per common share', 'Earnings per common Share',
        'REVENUES', 'REVENUES:', 'REVENUE', 'REVENUE:',
        'Net earnings', 'net earnings', 'Net earnings:', 'net earnings:',
        'NET EARNINGS', 'NET EARNINGS ', 'SALES AND OPERATING REVENUES:',
        'TOTAL COST OF SALES', 'TOTAL COST OF SALES:',
        'Sales and revenues:', 'Sales and revenues', 'Total net revenues', 'Total net revenues:',
        'Revenues and Other Income', 'Costs and Other Deductions',
        'NET SALES:', 'NET SALES',
        'NET INCOME', 'NET INCOME:',
        'OPERATING INCOME', 'OPERATING INCOME:'
    ]:
        try:
            table = driver.find_element(By.XPATH,
                                        f"//*[text()='{text}' and not(contains(@class, 'xbrlviewer'))]/ancestor::tbody[1]")
            break
        except:
            continue
    if not table:
        raise Exception("No table found")
    return table
