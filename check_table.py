import pymssql
import pandas as pd

# SQL Server接続情報
server = '192.168.1.19'
port = 1433  # SQL Express default port
database = 'ELIMS'
username = 'devin'
password = 'elhin'
table_name = 'TC_変化点管理台帳'

try:
    # SQL Serverに接続
    conn = pymssql.connect(server=server, port=port, user=username, password=password, database=database)
    cursor = conn.cursor()
    
    print(f"Successfully connected to SQL Server: {server}")
    print(f"Database: {database}")
    print("-" * 80)
    
    # テーブルのカラム情報を取得
    query = """
    SELECT 
        COLUMN_NAME,
        DATA_TYPE,
        CHARACTER_MAXIMUM_LENGTH,
        IS_NULLABLE,
        COLUMN_DEFAULT
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = ?
    ORDER BY ORDINAL_POSITION
    """
    
    df_columns = pd.read_sql_query(query, conn, params=[table_name])
    
    print(f"\n{table_name} テーブルの構造:")
    print("-" * 80)
    print(df_columns.to_string(index=False))
    
    # プライマリーキー情報を取得
    pk_query = """
    SELECT 
        KU.COLUMN_NAME
    FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
    INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU
        ON TC.CONSTRAINT_TYPE = 'PRIMARY KEY' AND
           TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME AND 
           KU.TABLE_NAME = ?
    ORDER BY KU.ORDINAL_POSITION
    """
    
    df_pk = pd.read_sql_query(pk_query, conn, params=[table_name])
    
    if not df_pk.empty:
        print(f"\nプライマリーキー: {', '.join(df_pk['COLUMN_NAME'].tolist())}")
    
    # サンプルデータを取得（最初の5行）
    sample_query = f"SELECT TOP 5 * FROM {table_name}"
    df_sample = pd.read_sql_query(sample_query, conn)
    
    print(f"\nサンプルデータ（最初の5行）:")
    print("-" * 80)
    print(df_sample.to_string(index=False))
    
    # テーブルの行数を取得
    count_query = f"SELECT COUNT(*) AS row_count FROM {table_name}"
    df_count = pd.read_sql_query(count_query, conn)
    print(f"\n合計行数: {df_count['row_count'][0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")