# 표준 라이브러리
import sqlite3

# 서드파티 라이브러리
import pandas as pd

# 로컬 모듈
import missions.W1.M3.etl_project_gdp as etl_basic
from missions.W1.M3.log.log import Logger

logger = Logger.get_logger("GDP_ETL_LOGGER")

###########
#  Extract Process
###########
def extract_gdp_wiki_web2json(url: str, out_file: str) -> None:
    etl_basic.extract_gdp_wiki_web2json(url, out_file)

###########
#  Transform Process
###########

def json2dataframe(json_file: str)-> pd.DataFrame:
    """
    Reads a JSON file and converts it into a Pandas DataFrame.

    Args:
        json_file (str): The file path to the JSON file to be read.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the data from the JSON file.
    """

    try:
        logger.info(f"[START] Read data from {json_file} ...")
        df = pd.read_json(json_file)
        logger.info(f"[COMPLET] Data was read successfully: {json_file}")
    except Exception as e:
        logger.error(f"[FAIL] Failed to read data to {json_file}. Exception: {e.__class__.__name__}")
        raise
    return df

def merge_region_by_country(df_gdp: pd.DataFrame, df_region: pd.DataFrame)-> pd.DataFrame:
    try:
        logger.info(f"[START] Start Merging the region data with gdp data ...")
        df_merged = df_gdp.merge(df_region, on='country', how='left')
        logger.info(f"[COMPLET] Succesfuly merged the region data with gdp data.")
    except Exception as e:
        logger.info(f"[FAIL] Failed to merge the region data with gdp data.")
        raise
    return df_merged

def transform_gdp(df_gdp):
    df_gdp['gdp'] = pd.to_numeric(df_gdp['gdp'].str.replace(",", ""), errors='coerce')  # str2int
    df_gdp['gdp'] = (df_gdp['gdp'] / 1e3).round(2)  # GDP의 단위는 1B USD이어야 하고 소수점 2자리까지만 표시해 주세요.
    df_gdp = df_gdp.sort_values(by='gdp', ascending=False).reset_index(drop=True)  # 해당 테이블에는 GDP가 높은 국가들이 먼저 나와야 합니다.

    # 결측값에 "측정하지 못한 통게치"라는 의미가 있기 때문에 처리하지 않는다.
        

def transform_gdp_from_json(gdp_file, region_file):
    try:
        logger.info("[START] Starting GDP Transforming process...")

        df_gdp = json2dataframe(gdp_file)
        df_region = json2dataframe(region_file)

        # 데이터 정제 및 변환
        transform_gdp(df_gdp)

        # Region 병합
        df_gdp_with_region = merge_region_by_country(df_gdp, df_region)

        logger.info("[COMPLET] GDP Transforming process completed successfully.")
    except Exception as e:
          logger.warn("[FAIL] GDP Transforming process failed.")
    
    return df_gdp_with_region


###########
#  Load Process
###########
def load_to_sqlite(df, db_name="missions/W1/M3/data/Countries_by_GDP.db"):
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
    gdp_file = "missions/W1/M3/data/Countries_by_GDP.json"
    region_file = "missions/W1/M3/data/cultural-geo-mapper.json"

    extract_gdp_wiki_web2json(url, gdp_file)

    # Transform 단계 실행
    df_transformed = transform_gdp_from_json(gdp_file, region_file)

    # Load 단계 실행
    load_to_sqlite(df_transformed)

    print("[ETL] Process completed successfully.")


if __name__ == "__main__":
    main()
