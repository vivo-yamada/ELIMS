import pymssql
import pandas as pd
from datetime import datetime

# SQL Server接続情報
server = '192.168.1.19\\SQLEXPRESS'
database = 'ELIMS'
username = 'devin'
password = 'elhin'
table_name = 'TC_変化点管理台帳'

try:
    # SQL Serverに接続
    conn = pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database
    )
    cursor = conn.cursor()
    
    print("最新レコードを取得中...")
    print("=" * 80)
    
    # 最新のレコードを取得（IDで降順ソート）
    query = f"""
    SELECT TOP 1 * 
    FROM [{table_name}]
    ORDER BY ID DESC
    """
    
    cursor.execute(query)
    row = cursor.fetchone()
    
    # カラム名を取得
    col_names = [column[0] for column in cursor.description]
    
    # レコードを表示
    print("\n【最新レコードの内容】")
    print("-" * 80)
    
    for i, (col_name, value) in enumerate(zip(col_names, row)):
        # NULLや空文字列でない値のみ表示
        if value is not None and str(value).strip():
            # datetime型の場合はフォーマット
            if isinstance(value, datetime):
                value_str = value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                value_str = str(value)
            
            print(f"{i+1:3}. {col_name:<30}: {value_str}")
    
    # 主要な情報をまとめて表示
    print("\n" + "=" * 80)
    print("【主要情報のサマリー】")
    print("-" * 80)
    
    # IDを取得
    id_idx = col_names.index('ID')
    print(f"ID: {row[id_idx]}")
    
    # 変化点NO
    if '変化点NO' in col_names:
        idx = col_names.index('変化点NO')
        print(f"変化点NO: {row[idx]}")
    
    # 発行月日
    if '発行月日' in col_names:
        idx = col_names.index('発行月日')
        if row[idx]:
            print(f"発行月日: {row[idx].strftime('%Y-%m-%d') if isinstance(row[idx], datetime) else row[idx]}")
    
    # 目的内容
    if '目的内容' in col_names:
        idx = col_names.index('目的内容')
        print(f"目的内容: {row[idx]}")
    
    # 変更内容
    if '変更内容' in col_names:
        idx = col_names.index('変更内容')
        print(f"変更内容: {row[idx]}")
    
    # 入力時刻
    if '入力時刻' in col_names:
        idx = col_names.index('入力時刻')
        if row[idx]:
            print(f"入力時刻: {row[idx].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[idx], datetime) else row[idx]}")
    
    cursor.close()
    conn.close()
    print("\n接続を閉じました。")
    
except Exception as e:
    print(f"Error: {e}")