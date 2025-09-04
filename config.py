import os

class Config:
    """アプリケーション設定"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # SQL Server設定
    DB_SERVER = '192.168.1.19\\SQLEXPRESS'
    DB_DATABASE = 'ELIMS'
    DB_USERNAME = 'devin'
    DB_PASSWORD = 'elhin'
    
    # データベース接続文字列
    @property
    def DATABASE_URL(self):
        return {
            'server': self.DB_SERVER,
            'database': self.DB_DATABASE,
            'username': self.DB_USERNAME,
            'password': self.DB_PASSWORD
        }