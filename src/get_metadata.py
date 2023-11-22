# %%
import requests
from dotenv import load_dotenv
import pandas as pd
import os
import datetime
import time
from pathlib import Path
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")
data_path = Path("../data")
meta_path = data_path / "metadata"
url = "https://api.edinet-fsa.go.jp/api/v2/documents.json"


with open(data_path / "metadata_param.json", encoding="utf-8") as f:
    param = json.load(f)

start = datetime.datetime.strptime(param["start"], "%Y-%m-%d")
end = datetime.datetime.strptime(param["end"], "%Y-%m-%d")


# %%
for date in pd.date_range(start, end):
    payload = {
        "date": date.date(),
        "type": "2",
        "Subscription-Key": API_KEY,
    }

    response = requests.get(url, params=payload).json()

    print(date.date())
    if response["metadata"]["status"] == "404":
        print(f"[404] 日付がapi対象範囲外だと考えられます\n")
        continue

    results = response["results"]
    if results == []:
        print(f"[200] レスポンスが空なため、書き込まれませんでした\n")
    else:
        pd.DataFrame(results).to_csv(
            meta_path / f"{date.date()}.csv",
            index=None,
            encoding="utf_8_sig",
        )
        print(f"[200] 正常に書き込まれました\n")
    time.sleep(0.5)
# %%
