#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
売上CSV → Googleスプレッドシート 書き込みスクリプト

【毎日の使い方】
  python upload_sales.py <CSVファイルパス>
  例: python upload_sales.py shop_daily_0508.csv

【初回一括投入】
  python upload_sales.py --bulk <フォルダパス>
  例: python upload_sales.py --bulk .
"""

import sys
import os
import csv
import io
import requests
import time

GAS_URL = "https://script.google.com/macros/s/AKfycbx2jwQJ86ghaWhvE7DBAYJh1ahW_0doceRXUr4sJqIbbHx8HGPkwbnMHwIObHkq0mPmMQ/exec"

COLUMNS = [
    "日付", "店舗計",
    "Se-マガザン楽天市場店", "セントラルマーケット楽天市場店",
    "Se-マガザンYahoo!ショッピング店", "Se-マガザンauPAYマーケット店",
    "ｾﾝﾄﾗﾙﾏｰｹｯﾄdｼｮｯﾋﾟﾝｸﾞ店", "ｾﾝﾄﾗﾙﾏｰｹｯﾄANA Mall店",
    "ｾﾝﾄﾗﾙﾏｰｹｯﾄJRE MALL店", "Se-magasinメルカリShops店",
    "ｾﾝﾄﾗﾙﾏｰｹｯﾄTemu店"
]

def parse_csv(path):
    with open(path, encoding="shift-jis") as f:
        content = f.read()
    reader = csv.reader(io.StringIO(content))
    rows = []
    for i, parts in enumerate(reader):
        if i == 0:
            continue
        while parts and parts[-1].strip() == "":
            parts.pop()
        if len(parts) < 2:
            continue
        r = []
        for j, col in enumerate(COLUMNS):
            if j >= len(parts):
                r.append(0)
            elif col == "日付":
                r.append(parts[j].strip())
            else:
                try:
                    r.append(int(parts[j].replace(",", "").strip()))
                except:
                    r.append(0)
        rows.append(r)
    return rows

def send_to_gas(rows, label=""):
    payload = {"rows": rows}
    resp = requests.post(GAS_URL, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()

def main():
    if len(sys.argv) < 2:
        print("使い方: python upload_sales.py <CSVファイルパス>")
        print("　　　　python upload_sales.py --bulk <フォルダパス>")
        sys.exit(1)

    if sys.argv[1] == "--bulk":
        if len(sys.argv) < 3:
            print("フォルダパスを指定してください")
            sys.exit(1)
        folder = sys.argv[2]
        files = sorted([f for f in os.listdir(folder) if f.endswith(".csv")])
        if not files:
            print(f"CSVファイルが見つかりません: {folder}")
            sys.exit(1)

        # 1ファイルずつ送信（タイムアウト対策）
        total = 0
        for f in files:
            path = os.path.join(folder, f)
            rows = parse_csv(path)
            print(f"送信中: {f} ({len(rows)}行)...", end=" ", flush=True)
            result = send_to_gas(rows, f)
            print(f"完了 → {result}")
            total += len(rows)
            time.sleep(1)  # GASへの負荷軽減

        print(f"\n全て完了！合計 {total} 行を書き込みました。")

    else:
        path = sys.argv[1]
        if not os.path.exists(path):
            print(f"ファイルが見つかりません: {path}")
            sys.exit(1)
        rows = parse_csv(path)
        print(f"読み込み: {os.path.basename(path)} ({len(rows)}行)")
        print("送信中...")
        result = send_to_gas(rows)
        print(f"完了: {result}")

if __name__ == "__main__":
    main()
