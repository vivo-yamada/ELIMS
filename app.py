from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import traceback
from database import db_manager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    """メインページ"""
    return render_template('register_modern_new.html')

@app.route('/test')
def test():
    """テストページ"""
    return render_template('test_multistep.html')

@app.route('/working')
def working():
    """動作確認版"""
    return render_template('test_working.html')

@app.route('/api/generate_henkaiten_no', methods=['GET'])
def generate_henkaiten_no():
    """変化点No.の自動生成API"""
    try:
        # 現在の年を取得（2桁）
        current_year = datetime.now().strftime('%y')
        
        # データベースから同年の最大値を取得
        query = f"""
            SELECT MAX(CAST(SUBSTRING([変化点NO], 7, 4) AS INT)) as max_num
            FROM [TC_変化点管理台帳]
            WHERE [変化点NO] LIKE 'HPC{current_year}-%'
        """
        result = db_manager.execute_query(query)
        
        # 次の番号を決定
        if result and len(result) > 0 and result[0].get('max_num') is not None:
            next_num = result[0]['max_num'] + 1
        else:
            next_num = 1
            
        # 変化点No.を生成（HPC + 年2桁 + - + 4桁連番）
        henkaiten_no = f"HPC{current_year}-{next_num:04d}"
        
        return jsonify({'henkaiten_no': henkaiten_no})
        
    except Exception as e:
        print(f"Error generating henkaiten_no: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/check_duplicate_no', methods=['POST'])
def check_duplicate_no():
    """変化点No.の重複チェックと再採番"""
    try:
        data = request.get_json()
        henkaiten_no = data.get('henkaiten_no')
        
        # 重複チェック
        check_query = """
            SELECT COUNT(*) as count FROM [TC_変化点管理台帳] 
            WHERE [変化点NO] = %s
        """
        result = db_manager.execute_query(check_query, (henkaiten_no,))
        
        if result[0]['count'] > 0:
            # 重複している場合、新しい番号を生成
            current_year = datetime.now().strftime('%y')
            query = f"""
                SELECT MAX(CAST(SUBSTRING([変化点NO], 7, 4) AS INT)) as max_num
                FROM [TC_変化点管理台帳]
                WHERE [変化点NO] LIKE 'HPC{current_year}-%'
            """
            max_result = db_manager.execute_query(query)
            
            if max_result and len(max_result) > 0 and max_result[0].get('max_num') is not None:
                next_num = max_result[0]['max_num'] + 1
            else:
                next_num = 1
                
            new_henkaiten_no = f"HPC{current_year}-{next_num:04d}"
            return jsonify({
                'is_duplicate': True,
                'new_henkaiten_no': new_henkaiten_no,
                'message': f'変化点No.が重複していたため、{new_henkaiten_no}に更新しました。'
            })
        else:
            return jsonify({'is_duplicate': False})
            
    except Exception as e:
        print(f"Error checking duplicate: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    """変化点管理台帳の登録処理"""
    
    if request.method == 'GET':
        return render_template('register_modern_new.html')
    
    if request.method == 'POST':
        try:
            # フォームデータを取得
            form_data = request.form.to_dict()
            henkaiten_no = form_data.get('henkaiten_no')
            sosei = form_data.get('sosei', '工程変更')  # 素性フィールドを取得（デフォルト値：工程変更）

            # 新しいフィールドを取得
            uketsuke_no = form_data.get('受付No')
            kh_komu_kubun = form_data.get('KH工務区分')
            kh_kankatsu = form_data.get('KH管轄')
            kh_kihyo_busho_code = form_data.get('KH起票部署CODE')
            kihyo_busho = form_data.get('起票部署')

            if not henkaiten_no:
                return jsonify({'error': '変化点Noは必須です。'}), 400

            # IDの最大値を取得
            id_query = "SELECT MAX([ID]) as max_id FROM [TC_変化点管理台帳]"
            id_result = db_manager.execute_query(id_query)

            if id_result and len(id_result) > 0 and id_result[0].get('max_id') is not None:
                next_id = id_result[0]['max_id'] + 1
            else:
                next_id = 1

            # 現在時刻を取得
            now = datetime.now()

            # 更新されたINSERTクエリ
            insert_query = """
            INSERT INTO [TC_変化点管理台帳] (
                [ID], [変化点NO], [素性], [受付No],
                [KH工務区分], [KH管轄], [KH起票部署CODE], [起票部署],
                [入力時刻]
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            # パラメータを準備
            params = (
                next_id,
                henkaiten_no,
                sosei,
                uketsuke_no,
                kh_komu_kubun,
                kh_kankatsu,
                kh_kihyo_busho_code,
                kihyo_busho,
                now
            )
            
            # データベースに挿入
            result = db_manager.execute_insert(insert_query, params)
            
            return jsonify({'success': True, 'message': '変化点管理台帳が正常に登録されました。', 'id': next_id})
            
        except Exception as e:
            error_message = f"登録処理中にエラーが発生しました: {str(e)}"
            print(f"Error: {error_message}")
            print(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': error_message}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error='ページが見つかりません。'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='サーバー内部エラーが発生しました。'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)