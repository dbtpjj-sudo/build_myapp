from playwright.sync_api import sync_playwright
from facility_filter import get_target_facilities
from line_messaging import send_line
from parse_availability import parse_availability
import csv
import json

# ==========================
# 設定
# ==========================

# なりッシュ！
# USER_ID = "00162047"
# PASSWORD = "narissyu3287Nana"

# 札幌バドミントン社会人サークル
# USER_ID = "00167751"
# PASSWORD = "msd16949"

# 山岡家ファミリー
USER_ID = "00166903"
PASSWORD = "msd16949"

DISTRICTS = [
    "豊平区",
    "白石区",
    "厚別区",
    "清田区",
]

# TARGET_DAY = "15"


# ==========================
# ログイン
# ==========================

def login(page):
    # page.goto("https://yoyaku.harp.lg.jp/sapporo/")
    page.goto("https://yoyaku.sapporo-sports.or.jp/")
    page.wait_for_load_state("networkidle")
    # page.get_by_role("link", name="登録がお済みの方 ログイン").click()
    page.locator("text=ログイン").first.click()
    page.get_by_role("textbox", name="利用者番号").fill(USER_ID)
    page.get_by_role("textbox", name="パスワード").fill(PASSWORD)
    # page.get_by_role("button", name="ログイン").click()
    page.goto("https://yoyaku.sapporo-sports.or.jp/web/login")

# ==========================
# 空き情報
# ==========================

def check_school(page, school):

    fc = school["fc"]

    url = (
        f"https://yoyaku.harp.lg.jp/sapporo/"
        f"FacilityAvailability/GetDay/011002/{fc}"
    )

    data = {
        # "startDate": "2026-07-31",
        # "endDate": "2026-07-31"
    }

    print("URL:", url)
    print("POST:", data)

    response = page.request.post(
        url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    print(response.text()[:1000])
    print(f"\n=== {school['学校名']} ===")
    print("STATUS:", response.status)
    print(response.headers.get("content-type"))

    # HTMLならスキップ
    if "text/html" in response.headers.get("content-type", "").lower():
        print(f"{school['学校名']}: APIなし → スキップ")
        return None

    if response.status != 200:
        print("取得失敗")
        return None

    try:
        day_data = response.json()
    except Exception:
        print("JSON変換失敗")
        print(response.text()[:200])
        return None

    # JSON保存
    filename = f"day_result_{school['学校名']}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(day_data, f, ensure_ascii=False, indent=2)

    print("day_result.json 保存完了")

    return day_data


# ==========================
# メイン処理
# ==========================

def main():

    facilities, today_setting = get_target_facilities()
    print("取得件数:", len(facilities))

    all_results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login(page)
        
        # 全学校をチェック
        for facility in facilities:

            day_data = check_school(page, facility)

            if day_data is not None:

                results = parse_availability(
                    day_data,
                    facility["fc"],
                    today_setting
                )

                # 学校名・施設コードを追加
                for r in results:
                    r["school"] = facility["学校名"]
                    r["fc"] = facility["fc"]

                all_results.extend(results)


        # 日付 → 学校名 → 開始時間で並び替え
        all_results.sort(
            key=lambda x: (
                x["date"],
                x["school"],
                x["start"]
            )
        )


        # ===== まとめてLINE通知 =====
        if all_results:

            msg = "🏸 空き発見！\n\n"

            current_date = None


            for r in all_results:

                # 日付が変わった場合だけ表示
                if r["date"] != current_date:

                    current_date = r["date"]

                    msg += (
                        f"\n📅 {current_date}\n"
                        "====================\n"
                    )


                reserve_url = (
                    f"https://yoyaku.harp.lg.jp/sapporo/FacilityAvailability/Index/011002/{r['fc']}"
                )

                msg += (
                    f"🏫 {r['school']}\n"
                    f"⏰ {r['start']}〜{r['end']}\n"
                    f"🔗 {reserve_url}\n"
                    "----------------------\n"
                )


            send_line(msg)

        else:
            print("空きなし")


        browser.close()


if __name__ == "__main__":
    main()