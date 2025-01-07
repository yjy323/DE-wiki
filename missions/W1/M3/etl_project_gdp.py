import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json

# -------------------------
# 1. Extract: 크롤링, 테이블 파싱, JSON 변환
# -------------------------

def parse_webpage(html):
    # BeautifulSoup으로 HTML 파싱
    
    gdp_table = parse_gdp_table(html)
    gdp_data = parse_gdp_table_data(gdp_table)
    return gdp_data

def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch webpage. Status Code: {response.status_code}")
        return None
    return response.text

def parse_gdp_table(html):
    # 특정 테이블 검색: class="wikitable" AND caption="GDP (million US$) by country"
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
    # 테이블 데이터 파싱
    rows = gdp_table.find_all("tr")
    data = []
    
    for row in rows[3:]:  # 1-2 번째 행은 헤더이므로 제외, 3번째 행은 총계이므로 제외
        cells = row.find_all(["td"])

        for cell in cells[1:]:
                for sup in cell.find_all("sup"):
                    sup.decompose()  # <sup> 태그와 내용을 제거
        
        country = cells[0].get_text(strip=True)  # 첫 번째 열: 국가
        gdp_cell = cells[1]  # 두 번째 열: GDP 값
        if "table-na" in gdp_cell.get("class", []):
            gdp = None
            year = None
        else:
            gdp = gdp_cell.get_text(strip=True)
            year = cells[2].get_text(strip=True)  # 세 번째 열: 연도
            
        # 데이터를 리스트에 추가
        data.append({
            "country": country,
            "type": "IMF",
            "gdp": gdp,
            "year": year
        })
    
    print(f"[Extract] Extracted {len(data)} rows.")
    return data

def save_to_json(data, output_file):
    # JSON 파일로 저장
    print(f"[Extract] Saving data to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"[Extract] Data successfully saved to {output_file}.")

def extract_gdp_data_to_json(url, output_file):
    html = fetch_webpage(url)
    if not html:
        return
    
    data = parse_webpage(html)
    save_to_json(data, output_file)


# ----------------------
# 2. Transform: 데이터 변환
# ----------------------
def transform(json_file):
    print("[Transform] Parsing HTML data...")
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    df['gdp'] = df['gdp'].str.replace(",", "").astype(float)
    df['gdp'] = (df['gdp'] / 1e3).round(2)
    df = df.sort_values(by='gdp', ascending=False).reset_index(drop=True)
    return df

def main():
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    output_file = "data/Countries_by_GDP.json"
    
    # Extract 단계 실행
    extract_gdp_data_to_json(url, output_file)
    print("[ETL] Process completed successfully.")

    # Transform 단계 실행
    df = transform(output_file)
    return df


if __name__ == "__main__":
    main()