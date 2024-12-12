# open all sections in 10-K
from selenium.common import ElementNotInteractableException
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
    textKeyword = ''
    for text in [
        'consolidated and sector income statement', 'consolidated and sector income statements',
        'consolidated and sectors income statements', 'consolidated and sectors income statement',
        'consolidated and sector statement of operations', 'consolidated and sector statement of operation',
        'consolidated and combined statements of earnings', 'consolidated and combined statement of earnings',
        'consolidated statements of operations and comprehensive income',
        'consolidated statements of loss',
        'consolidated condensed statements of income',
        'consolidated statements of operations and comprehensive income (loss)',
        'consolidated statements of (loss) income',
        'consolidated statements of income',
        'consolidated statements of operations',
        'consoldiated statements of operations', # yep, typo
        'consolidated statements of earnings',
        'consolidated statement of operations',
        'statements of consolidated earnings',
        'statements of consolidated income',
        'statements of consolidated (loss) income',
        'consolidated statement of (loss) income',
        'statement of consolidated income',
        'consolidated statements of comprehensive earnings',
        'consolidated statements of condensed earnings',
        'consolidated statement of income', 'statement of consolidated operations',
        'INCOME STATEMENTS', 'statement of income',
        'consolidated results of operations',
        'statements of consolidated operations',
        'statement of consolidated operations',
        'statement of earnings (loss)',
        'consolidated income statement',
        'consolidated income statements',
        'statement of earnings',
        'statements of earnings',
        'consolidated statements of comprehensive earnings',
        'consolidated comprehensive statements of earnings',
        'consolidated statement of earnings',
        'income statements',
    ]:
        try:
            section = driver.find_element(By.XPATH,
                                          f"//a[text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{text}')]]")
            textKeyword = text
            break
        except:
            continue
    if section is None:
        print('No section found')
        # Has to be last. AYI has statement under this, but most have some other stuff we don't want
        fallbacks = [
            # 'loss',
            'consolidated statements of comprehensive income',
        ]
        for fallback in fallbacks:
            try:
                section = driver.find_element(By.XPATH,
                                              f"//a[text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{fallback}')]]")
                print("Using fallback. Check if it is correct data")
                break
            except:
                continue
        if section is None:
            print("Fallback failed")
            return None
    try:
        section.click()
    except ElementNotInteractableException:
        print('Element not interactable')
        print(textKeyword)

    for text in [
        'Revenue', 'Net income', 'Net income (loss)', 'Operating income', 'Operating income (loss)',
        'Revenues', 'Revenues:', 'Total Revenue', 'Total Revenues', 'Total revenue', 'Total revenues',
        'Sales', 'Sales:'
        'Total sales', 'Total Sales', 'Total sales:', 'Total Sales:'
        'Net revenue', 'Net revenues', 'Net Revenues', 'Net Revenues:', 'Net revenue:', 'Net Revenue:'
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
        'Net Income', 'Net Income:'
        'OPERATING INCOME', 'OPERATING INCOME:',
        'Operating Income', 'Operating Income:',
        'Operating Revenue:', 'Operating Revenue',
        'Operating Expense:', 'Operating Expense',
        'Operating expense:', 'Operating expense',
        'operating expense:', 'operating expense',
        'Total operating revenues', 'Total operating revenues:',
        'Total operating revenue', 'Total operating revenue:',
        'Operating Revenues and Other', 'Operating Revenues and Other:',
        'Net Operating Revenues and Other', 'Net Operating Revenues and Other:',
        'Net Operating Revenues', 'Net Operating Revenues:',
        'Operating revenue', 'Operating revenue:',
        'Revenues and other income', 'Revenues and other income:',
        'Interest Income', 'Interest Income:', 'Interest income:', 'Interest income',
        'Net Income (Loss)', 'Net income (loss)', 'net income (loss)',
        'Net Income (Loss):', 'Net income (loss):', 'net income (loss):',
        'General and administrative', 'General and administrative:',
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
