import pymssql
import socket

# SQL Server接続情報のパターンを試す
servers = [
    ('192.168.1.19', 1433),    # デフォルトポート
    ('192.168.1.19', 1434),    # SQL Browser port
    ('192.168.1.19', 49172),   # Common dynamic port
    ('192.168.1.19', 50000),   # Another common port
]

database = 'ELIMS'
username = 'ELIMS'
password = 'devin'

print("Testing SQL Server connections...")
print("-" * 60)

for server, port in servers:
    try:
        print(f"\nTrying {server}:{port}...")
        
        # ポートが開いているか確認
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((server, port))
        sock.close()
        
        if result == 0:
            print(f"Port {port} is open")
            
            # SQL Server接続を試す
            conn = pymssql.connect(
                server=server, 
                port=port,
                user=username, 
                password=password, 
                database=database
            )
            print(f"✓ Successfully connected to {server}:{port}")
            
            # 簡単なクエリを実行
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            row = cursor.fetchone()
            print(f"SQL Server Version: {row[0][:50]}...")
            
            cursor.close()
            conn.close()
            break
        else:
            print(f"Port {port} is not open")
            
    except Exception as e:
        print(f"Connection failed: {str(e)[:100]}...")

print("\n" + "-" * 60)

# インスタンス名での接続も試す
print("\nTrying with instance name...")
try:
    conn = pymssql.connect(
        server='192.168.1.19\\SQLEXPRESS',
        user=username, 
        password=password, 
        database=database
    )
    print("✓ Successfully connected with instance name")
    conn.close()
except Exception as e:
    print(f"Failed: {str(e)[:100]}...")