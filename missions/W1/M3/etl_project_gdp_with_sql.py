import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import json
import os

# -------------------------
# 1. Extract: 크롤링, 테이블 파싱, JSON 변환
# -------------------------
def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch webpage. Status Code: {response.status_code}")
        return None
    return response.text

def parse_gdp_table(html):
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})

    gdp_table = None
    for table in tables:
        caption = table.find("caption")
        if caption and "GDP (million US$) by country" in caption.get_text():
            gdp_table = table
            break

    if not gdp_table:
        print("[Extract] No matching table found.")
        return None
    
    print("[Extract] Found the target table. Parsing data...")
    return gdp_table

def parse_gdp_table_data(gdp_table):
    rows = gdp_table.find_all("tr")
    data = []
    
    for row in rows[3:]:  # 헤더와 총계를 제외
        cells = row.find_all(["td"])
        for cell in cells[1:]:
            for sup in cell.find_all("sup"):
                sup.decompose()  # <sup> 태그 제거

        country = cells[0].get_text(strip=True)
        gdp_cell = cells[1]
        if "table-na" in gdp_cell.get("class", []):
            gdp = None
            year = None
        else:
            gdp = gdp_cell.get_text(strip=True)
            year = cells[2].get_text(strip=True)
        
        data.append({
            "country": country,
            "type": "IMF",
            "gdp": gdp,
            "year": year
        })
    
    print(f"[Extract] Extracted {len(data)} rows.")
    return data

def save_to_json(data, output_file):
    print(f"[Extract] Saving data to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"[Extract] Data successfully saved to {output_file}.")

def extract_gdp_data_to_json(url, output_file):
    html = fetch_webpage(url)
    if not html:
        return
    gdp_table = parse_gdp_table(html)
    if not gdp_table:
        return
    data = parse_gdp_table_data(gdp_table)
    save_to_json(data, output_file)


# ----------------------
# 2. Transform: 데이터 변환
# ----------------------
def transform(json_file, region_file):
    print("[Transform] Transforming data...")

    # Load JSON 데이터
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    df_gdp = pd.DataFrame(data)

    # Load region 데이터
    regions = pd.read_json(region_file)

    # 데이터 정제 및 변환
    df_gdp['gdp'] = pd.to_numeric(df_gdp['gdp'].str.replace(",", ""), errors='coerce')
    df_gdp['gdp'] = (df_gdp['gdp'] / 1e3).round(2)  # 단위 변환 (1B USD)
    df_gdp = df_gdp.sort_values(by='gdp', ascending=False).reset_index(drop=True)

    # Region 병합
    df_merged = df_gdp.merge(regions, on='country', how='left')
    df_merged = df_merged.rename(columns={"gdp": "GDP_USD_billion", "year": "Year", "region": "Region"})

    print("[Transform] Transformation complete.")
    return df_merged


# ----------------------
# 3. Load: 데이터 로드
# ----------------------
def load_to_sqlite(df, db_name="data/Countries_by_GDP.db"):
    print("[Load] Loading data into SQLite database...")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Countries_by_GDP (
        Country TEXT,
        GDP_USD_billion REAL,
        Year TEXT,
        Region TEXT
    )
    """)

    # 데이터 삽입
    df.to_sql("Countries_by_GDP", conn, if_exists="replace", index=False)

    print("[Load] Data successfully loaded into SQLite database.")
    conn.close()


# ----------------------
# Main ETL Process
# ----------------------

def main():
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    output_file = "data/Countries_by_GDP.json"
    region_file = "data/cultural-geo-mapper.json"

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Extract 단계 실행
    extract_gdp_data_to_json(url, output_file)

    # Transform 단계 실행
    df_transformed = transform(output_file, region_file)

    # Load 단계 실행
    load_to_sqlite(df_transformed)

    print("[ETL] Process completed successfully.")


if __name__ == "__main__":
    main()
