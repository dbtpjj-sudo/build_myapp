import json
import pandas as pd
from datetime import datetime

# 曜日変換
WEEKDAY_MAP = {
    0: "月",
    1: "火",
    2: "水",
    3: "木",
    4: "金",
    5: "土",
    6: "日",
}


def get_target_facilities():

    # config読込
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    # 今日の曜日
    today = WEEKDAY_MAP[datetime.now().weekday()]

    # 今日の設定を取得
    today_setting = None

    for s in config["schedule"]:
        if today in s["weekdays"]:
            today_setting = s
            break

    if today_setting is None:
        print(f"{today} の設定がありません")
        return []

    print("今日の曜日:", today)
    print("対象区:", today_setting["districts"])

    # 学校マスタ読込
    df = pd.read_csv(
        "school_master.csv",
        dtype={"fc": str}
    )

    # 対象区だけ抽出
    target = df[
        df["地区"].isin(today_setting["districts"])
    ]

    facilities = target[
        ["fi", "fc", "学校名"]
    ].to_dict("records")

    return facilities, today_setting

if __name__ == "__main__":
    facilities = get_target_facilities()

    print(f"取得件数: {len(facilities)}")

    for f in facilities:
        print(f)