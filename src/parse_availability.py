print("★★ 新しいparse_availability.py読込 ★★")

from line_messaging import send_line


def parse_availability(data, fc, today_setting):

    # 取得失敗・対象外施設対策
    if not data:
        return []

    if not data.get("rooms"):
        return []

    if not data.get("timeFrames"):
        return []

    time_map = {}

    # 時間帯情報取得
    for t in data.get("timeFrames") or []:
        for tf in t.get("usageTimeFrames", []):
            time_map[tf["usageTimeFrameId"]] = {
                "start": tf.get("usageStartTime"),
                "end": tf.get("usageEndTime"),
            }

    results = []
    seen_slots = set()

    allowed_ranges = {
        (start, end)
        for start, end in today_setting["time_ranges"]
    }
    
    # 空き情報確認
    for room in data.get("rooms") or []:
        for court in room.get("courts", []):
            for day in court.get("dayBooks", []):

                date = day["usageDate"][:10]

                for usage in day.get("usageTimes", []):
                    print("★★確認★★", usage)
                    
                    frame_id = usage["usageTimeFrameId"]

                    # 日付＋時間帯で重複チェック
                    slot_key = (date, frame_id)

                    if slot_key in seen_slots:
                        continue

                    seen_slots.add(slot_key)

                    print(
                    "status:",
                    usage["statusType"],
                    "frame:",
                    frame_id,
                    "ALL:",
                    usage
                    )

                    print(usage)

                    # U01だけ空き扱い
                    if usage["statusType"] == "U01":

                        t = time_map.get(frame_id)

                        if not t:
                            continue

                        # config.jsonで指定した時間帯だけ対象
                        if (t["start"], t["end"]) not in allowed_ranges:
                            continue

                        results.append({
                            "room": room["roomName"],
                            "court": court["courtName"],
                            "date": date,
                            "start": t["start"],
                            "end": t["end"]
                        })
            # print("空き件数:", len(results))

    # 空きがあった場合LINE通知
    # if results:

    #     # ★ここに予約URLを作るコードを追記★
    #     # reserve_url = f"https://yoyaku.harp.lg.jp/sapporo/FacilityAvailability/Index/011002/{fc}"
    #     reserve_url = "https://yoyaku.harp.lg.jp/sapporo/"
    #     msg = "🏸 空き発見！\n\n"

    #     # ★ここを予約URL付きの整形に変更★
    #     for r in results:
    #         msg += (
    #             f"🏫 {r['room']}（{r['court']}）\n"
    #             f"📅 {r['date']}\n"
    #             f"⏰ {r['start']}〜{r['end']}\n"
    #             f"🔗 予約ページ：{reserve_url}\n"
    #             "----------------------\n"
    #         )

    #     send_line(msg)
    # # 空きがない場合は通知なし

    return results