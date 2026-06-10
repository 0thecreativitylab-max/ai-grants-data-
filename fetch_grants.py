import os, json, urllib.request, urllib.parse, datetime
key = os.environ["DATA_GO_KR_KEY"]
base = "https://apis.data.go.kr/B552735/kisedKstartUpService01/getAnnouncementInformation01"
AI_KW = ["ai","인공지능","sw","소프트웨어","디지털","데이터","빅데이터","자동화","콘텐츠","영상","ict","클라우드","메타버스","dx","ax","바우처"]
rows = []

for page in range(1, 6):
    q = urllib.parse.urlencode({"serviceKey": key, "returnType": "json", "perPage": 100, "page": page})
    url = f"{base}?{q}&cond%5Brcrt_prgs_yn%3A%3AEQ%5D=Y"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.load(r)
    except Exception as e:
        print("ERR page", page, e); break
    items = data.get("data", [])
    if not items: break
    for it in items:
        text = f"{it.get('biz_pbanc_nm','')}} {it.get('supt_biz_clsfc','')}} {it.get('intg_pbanc_biz_nm','')}}".lower()
        if any(k in text for k in AI_KW):
            rows.append({
                "공고명": it.get("biz_pbanc_nm"), 
                "기관": it.get("pbanc_ntrp_nm"),
                "분야": it.get("supt_biz_clsfc"), 
                "대상": it.get("aply_trgt"),
                "대상상세": it.get("aply_trgt_ctnt"),
                "업력요건": it.get("biz_enyy"), 
                "접수시작": it.get("pbanc_rcpt_bgng_dt"),
                "접수마감": it.get("pbanc_rcpt_end_dt"),
                "지역": it.get("supt_regin"), 
                "신청URL": it.get("aply_mthd_onli_rcpt_istc"),
                "상세URL": it.get("detl_pg_url")
            })
    if len(items) < 100: break

out = {
    "수집시각_UTC": datetime.datetime.utcnow().isoformat() + "Z", 
    "건수": len(rows), 
    "공고": rows
}

with open("grants.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("저장 완료:", len(rows), "건")
