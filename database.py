import pymssql
from config import Config

class DatabaseManager:
    """データベース接続管理クラス"""
    
    def __init__(self):
        self.config = Config()
    
    def get_connection(self):
        """データベース接続を取得"""
        try:
            conn = pymssql.connect(
                server=self.config.DB_SERVER,
                user=self.config.DB_USERNAME,
                password=self.config.DB_PASSWORD,
                database=self.config.DB_DATABASE
            )
            return conn
        except Exception as e:
            print(f"Database connection error: {e}")
            raise
    
    def execute_query(self, query, params=None):
        """クエリを実行してデータを取得"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(as_dict=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            return cursor.fetchall()
        except Exception as e:
            print(f"Query execution error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def execute_insert(self, query, params=None):
        """INSERT文を実行"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.lastrowid or cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Insert execution error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# グローバルインスタンス
db_manager = DatabaseManager()