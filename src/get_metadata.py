# %%
import requests
from dotenv import load_dotenv
import pandas as pd
import os
import datetime
import time

load_dotenv()

API_KEY = os.getenv("API_KEY")
meta_path = "../data/metadata.csv"
url = "https://api.edinet-fsa.go.jp/api/v2/documents.json"

columns = [
    "seqNumber",
    "docID",
    "edinetCode",
    "secCode",
    "JCN",
    "filerName",
    "fundCode",
    "ordinanceCode",
    "formCode",
    "docTypeCode",
    "periodStart",
    "periodEnd",
    "submitDateTime",
    "docDescription",
    "issuerEdinetCode",
    "subjectEdinetCode",
    "subsidiaryEdinetCode",
    "currentReportReason",
    "parentDocID",
    "opeDateTime",
    "withdrawalStatus",
    "docInfoEditStatus",
    "disclosureStatus",
    "xbrlFlag",
    "pdfFlag",
    "attachDocFlag",
    "englishDocFlag",
    "csvFlag",
    "legalStatus",
]
# pd.DataFrame(columns=columns).to_csv(meta_path, encoding="utf_8_sig", index=None)

start = datetime.datetime.strptime("2021-12-07", "%Y-%m-%d")
end = datetime.datetime.strptime("2022-12-07", "%Y-%m-%d")
# %%
for date_time in pd.date_range(start, end):
    payload = {
        "date": date_time.date(),
        "type": "2",
        "Subscription-Key": API_KEY,
    }

    response = requests.get(url, params=payload).json()
    pd.DataFrame(response["results"]).to_csv(
        meta_path,
        mode="a",
        header=False,
        index=None,
        encoding="utf_8_sig",
    )
    time.sleep(0.5)
    print(date_time.date())
# %%