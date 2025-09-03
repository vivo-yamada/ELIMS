from sqlalchemy import create_engine, text
import pandas as pd
import urllib

# SQL Server接続情報
server = '192.168.1.19\\SQLEXPRESS'
database = 'ELIMS'
username = 'ELIMS'
password = 'devin'
table_name = 'TC_変化点管理台帳'

# 接続文字列の作成
params = urllib.parse.quote_plus(
    f"DRIVER={{FreeTDS}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"TDS_Version=8.0;"
)

try:
    # SQLAlchemy エンジンの作成
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    
    # 接続テスト
    with engine.connect() as conn:
        print(f"Successfully connected to SQL Server: {server}")
        print(f"Database: {database}")
        print("-" * 80)
        
        # テーブルのカラム情報を取得
        query = text("""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = :table_name
        ORDER BY ORDINAL_POSITION
        """)
        
        result = conn.execute(query, {"table_name": table_name})
        df_columns = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        print(f"\n{table_name} テーブルの構造:")
        print("-" * 80)
        print(df_columns.to_string(index=False))
        
        # プライマリーキー情報を取得
        pk_query = text("""
        SELECT 
            KU.COLUMN_NAME
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
        INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU
            ON TC.CONSTRAINT_TYPE = 'PRIMARY KEY' AND
               TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME AND 
               KU.TABLE_NAME = :table_name
        ORDER BY KU.ORDINAL_POSITION
        """)
        
        result = conn.execute(pk_query, {"table_name": table_name})
        df_pk = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        if not df_pk.empty:
            print(f"\nプライマリーキー: {', '.join(df_pk['COLUMN_NAME'].tolist())}")
        
        # サンプルデータを取得（最初の5行）
        sample_query = text(f"SELECT TOP 5 * FROM {table_name}")
        result = conn.execute(sample_query)
        df_sample = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        print(f"\nサンプルデータ（最初の5行）:")
        print("-" * 80)
        print(df_sample.to_string(index=False))
        
        # テーブルの行数を取得
        count_query = text(f"SELECT COUNT(*) AS row_count FROM {table_name}")
        result = conn.execute(count_query)
        count = result.fetchone()[0]
        print(f"\n合計行数: {count}")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative connection method with pymssql...")