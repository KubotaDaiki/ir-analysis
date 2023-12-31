# %%
import requests
from dotenv import load_dotenv
import pandas as pd
import os
import time
from pathlib import Path
import shutil
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")

data_path = Path("../data")
meta_path = data_path / "metadata"

with open(data_path / "irdata_param.json", encoding="utf-8") as f:
    param = json.load(f)

company = param["company"]
doctype = param["docType"]
# %%
csv_list = []
for csv_path in meta_path.glob("*.csv"):
    csv_list.append(pd.read_csv(csv_path, dtype=str))

raw_meta_df = pd.concat(csv_list)
meta_df = raw_meta_df[
    raw_meta_df["edinetCode"].isin(company.keys())
    & raw_meta_df["docTypeCode"].isin(doctype.keys())
]


# %%
def unzip(path, zip_binary):
    with open(path / "tmp.zip", "wb") as f:
        f.write(zip_binary)
    shutil.unpack_archive(path / "tmp.zip", path)


class TmpFolder(object):
    """一時的に使用するフォルダを作成・削除するクラス"""

    def __init__(self, path) -> None:
        self.path = Path(path)

    def __enter__(self):
        os.mkdir(self.path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.path)


# %%

for i, row in meta_df.iterrows():
    url = f'https://api.edinet-fsa.go.jp/api/v2/documents/{row["docID"]}'
    payload = {
        "type": "5",
        "Subscription-Key": API_KEY,
    }
    response = requests.get(url, params=payload)

    export_folder = (
        data_path / "ir" / company[row["edinetCode"]] / doctype[row["docTypeCode"]]
    )
    os.makedirs(export_folder, exist_ok=True)

    with TmpFolder("./tmp") as tmp:
        unzip(tmp.path, response.content)

        files = tmp.path.glob("XBRL_TO_CSV/*")
        file_name = f'{company[row["edinetCode"]]}_{row["periodEnd"]}.csv'
        for file in files:
            if "jpaud" not in file.name:
                shutil.move(file, export_folder / file_name)

    time.sleep(0.5)
    print(f"［完了］ファイル名：{file_name}")
# %%
