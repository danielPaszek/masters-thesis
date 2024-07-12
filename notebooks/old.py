# FIRST ATTEMPT
def openModalAndScrape(element):
    element.click()
    modal = driver.find_element(By.XPATH, f'//*[@id="taxonomy-modal-carousel-page-1"]/tbody')
    children = modal.find_elements(By.XPATH, './tr')
    data = {}
    print("scraping tag")
    for kid in children:
        tag = kid.find_element(By.XPATH, './th')
        value = kid.find_element(By.XPATH, './td/div')
        data[tag.text] = value.text
    return data

def takeImportant(data: dict, results: dict):
    other = []
    for key in data.keys():
        if key == 'Fact':
            results[key].append(data[key])
        elif key == 'Period':
            results[key].append(data[key])
        elif key not in ['Type', 'Format', 'Sign', 'Balance', 'Decimals', 'Scale', 'Measure', 'Tag']:
            other.append(key + ' - ' + data[key])
    results['other'].append(json.dumps(other))
    return results

url = 'https://www.sec.gov/ixviewer/ix.html?doc=/Archives/edgar/data/1326801/000132680124000012/meta-20231231.htm'

driver = webdriver.Chrome()
driver.get(url)
ticker = driver.find_element(By.NAME, "dei:TradingSymbol")
print(ticker.text)

revenues = driver.find_elements(By.NAME, "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax")
results = {
    'Fact': [],
    'Period': [],
    'other': []
}
for revenue in revenues:
    data = openModalAndScrape(revenue)
    results = takeImportant(data, results)


df = pd.DataFrame(results)
df.head()





driver = webdriver.Chrome()
# url_no_support = 'https://www.sec.gov/Archives/edgar/data/320193/000162828017000717/a10-qq1201712312016.htm' # 2018?
url_no_support = 'https://www.sec.gov/Archives/edgar/data/320193/000110465906084288/a06-25759_210k.htm' # 2006
driver.get(url_no_support)
#%%
cash_title = driver.find_element(By.XPATH, "//*[contains(text(), 'CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS')]")
print(cash_title.text)
print(cash_title.tag_name)
table = cash_title.find_element(By.XPATH, "../following::div/div/table/tbody")

#%%
cash_title = driver.find_element(By.XPATH, "//*[contains(text(), 'Net income')]/ancestor::tbody[1]")
lines = []
for child in cash_title.find_elements(By.XPATH, "./tr"):
    line = []
    for td in child.find_elements(By.XPATH, "./td"):
        text = td.text.strip()
        if text:
            line.append(td.text)
    lines.append(line)
lines