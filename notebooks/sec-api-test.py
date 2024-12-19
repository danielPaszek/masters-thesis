from sec_api import XbrlApi
from dotenv import load_dotenv
import os

load_dotenv()
SEC_API_KEY = os.getenv("SEC_API_KEY")

xbrlApi = XbrlApi(SEC_API_KEY)

# 10-K HTM File URL example
htm_url="https://www.sec.gov/Archives/edgar/data/1526520/000095017024016553/0000950170-24-016553-index.htm"
xbrl_json = xbrlApi.xbrl_to_json(htm_url=htm_url)
print(xbrl_json)