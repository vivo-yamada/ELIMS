import pymssql
import pandas as pd

# SQL Server接続情報
server = '192.168.1.19\\SQLEXPRESS'  # インスタンス名を含める
database = 'ELIMS'
username = 'devin'
password = 'elhin'
table_name = 'TC_変化点管理台帳'

try:
    # SQL Serverに接続
    print(f"Connecting to {server}...")
    conn = pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database
    )
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
    WHERE TABLE_NAME = %s
    ORDER BY ORDINAL_POSITION
    """
    
    cursor.execute(query, (table_name,))
    columns = cursor.fetchall()
    
    # カラム情報を表示
    print(f"\n{table_name} テーブルの構造:")
    print("-" * 80)
    print(f"{'カラム名':<30} {'データ型':<15} {'最大長':<10} {'NULL可':<10} {'デフォルト値'}")
    print("-" * 80)
    
    for col in columns:
        col_name = col[0]
        data_type = col[1]
        max_length = col[2] if col[2] else ''
        is_nullable = col[3]
        default_val = col[4] if col[4] else ''
        print(f"{col_name:<30} {data_type:<15} {str(max_length):<10} {is_nullable:<10} {str(default_val)}")
    
    # プライマリーキー情報を取得
    pk_query = """
    SELECT 
        KU.COLUMN_NAME
    FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
    INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU
        ON TC.CONSTRAINT_TYPE = 'PRIMARY KEY' AND
           TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME AND 
           KU.TABLE_NAME = %s
    ORDER BY KU.ORDINAL_POSITION
    """
    
    cursor.execute(pk_query, (table_name,))
    pk_columns = cursor.fetchall()
    
    if pk_columns:
        print(f"\nプライマリーキー: {', '.join([col[0] for col in pk_columns])}")
    
    # テーブルの行数を取得
    count_query = f"SELECT COUNT(*) AS row_count FROM [{table_name}]"
    cursor.execute(count_query)
    row_count = cursor.fetchone()[0]
    print(f"\n合計行数: {row_count}")
    
    # サンプルデータを取得（最初の3行）
    sample_query = f"SELECT TOP 3 * FROM [{table_name}]"
    cursor.execute(sample_query)
    sample_rows = cursor.fetchall()
    
    if sample_rows:
        print(f"\nサンプルデータ（最初の3行）:")
        print("-" * 80)
        # カラム名を取得
        col_names = [column[0] for column in cursor.description]
        for i, col_name in enumerate(col_names[:5]):  # 最初の5カラムのみ表示
            print(f"Column {i+1}: {col_name}")
        print("(その他のカラムは省略...)")
    
    cursor.close()
    conn.close()
    print("\n接続を閉じました。")
    
except pymssql.DatabaseError as e:
    print(f"Database Error: {e}")
except pymssql.InterfaceError as e:
    print(f"Interface Error: {e}")
except Exception as e:
    print(f"Error: {e}")