from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import traceback
from database import db_manager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    """メインページ - 一覧画面を表示"""
    return render_template('list.html')

@app.route('/list')
def list_page():
    """一覧画面"""
    return render_template('list.html')

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

@app.route('/api/changes/list', methods=['POST'])
def api_changes_list():
    """一覧データ取得API（DataTables ServerSide用）"""
    try:
        # DataTablesからのリクエストパラメータを取得
        draw = request.form.get('draw', type=int, default=1)
        start = request.form.get('start', type=int, default=0)
        length = request.form.get('length', type=int, default=50)

        # ソートパラメータ
        order_column = request.form.get('order[0][column]', type=int, default=20)
        order_dir = request.form.get('order[0][dir]', default='desc')

        # 検索・フィルタパラメータ
        filter_henkaiten_no = request.form.get('filterHenkaitenNo', '')
        filter_kihyo_busho = request.form.get('filterKihyoBusho', '')
        filter_hinban = request.form.get('filterHinban', '')
        filter_hinmei = request.form.get('filterHinmei', '')
        filter_tanto = request.form.get('filterTanto', '')
        filter_date_from = request.form.get('filterDateFrom', '')
        filter_date_to = request.form.get('filterDateTo', '')
        filter_ryudo_kahi = request.form.get('filterRyudoKahi', '')
        filter_kotei_henko = request.form.get('filterKoteiHenkoJisshi', '')

        # カラムマッピング
        columns = [
            None,  # チェックボックス
            '[変化点NO]',
            '[KH担当]',
            '[KH初品納入変更日]',
            '[KH初品納入実績初]',
            '[流動可否]',
            '[工程変更実施可否]',
            '[起票部署]',
            '[KH品番]',
            '[KH品名]',
            '[納入予定日]',
            '[KH設変出図予定日]',
            '[KH設変出図実績日]',
            '[変更内容]',
            '[特採後の処置]',
            '[流動判定日]',
            '[切替基準日]',
            '[KH管轄]',
            '[受付NO]',
            '[連絡書NO]',
            '[受付日]',
            None  # 操作ボタン
        ]

        # ベースクエリ
        base_query = """
            SELECT
                [ID],
                [変化点NO],
                [KH担当],
                [KH初品納入変更日],
                [KH初品納入実績初],
                [流動可否],
                [工程変更実施可否],
                [起票部署],
                [KH品番],
                [KH品名],
                [納入予定日],
                [KH設変出図予定日],
                [KH設変出図実績日],
                [変更内容],
                [特採後の処置],
                [流動判定日],
                [切替基準日],
                [KH管轄],
                [受付NO],
                [連絡書NO],
                [受付日]
            FROM [TC_変化点管理台帳]
        """

        # WHERE句の構築
        where_conditions = []
        params = []

        if filter_henkaiten_no:
            where_conditions.append("[変化点NO] LIKE %s")
            params.append(f'%{filter_henkaiten_no}%')

        if filter_kihyo_busho:
            where_conditions.append("[起票部署] LIKE %s")
            params.append(f'%{filter_kihyo_busho}%')

        if filter_hinban:
            where_conditions.append("[KH品番] LIKE %s")
            params.append(f'%{filter_hinban}%')

        if filter_hinmei:
            where_conditions.append("[KH品名] LIKE %s")
            params.append(f'%{filter_hinmei}%')

        if filter_tanto:
            where_conditions.append("[KH担当] LIKE %s")
            params.append(f'%{filter_tanto}%')

        if filter_date_from:
            where_conditions.append("[受付日] >= %s")
            params.append(filter_date_from)

        if filter_date_to:
            where_conditions.append("[受付日] <= %s")
            params.append(filter_date_to)

        if filter_ryudo_kahi:
            where_conditions.append("[流動可否] = %s")
            params.append(filter_ryudo_kahi)

        if filter_kotei_henko:
            where_conditions.append("[工程変更実施可否] = %s")
            params.append(filter_kotei_henko)

        # WHERE句を追加
        where_clause = ""
        if where_conditions:
            where_clause = " WHERE " + " AND ".join(where_conditions)

        # 総件数を取得
        count_query = f"SELECT COUNT(*) as count FROM [TC_変化点管理台帳]{where_clause}"
        count_result = db_manager.execute_query(count_query, tuple(params) if params else None)
        total_records = count_result[0]['count'] if count_result else 0

        # ORDER BY句を追加
        order_column_name = columns[order_column] if order_column < len(columns) and columns[order_column] else '[受付日]'
        order_clause = f" ORDER BY {order_column_name} {order_dir.upper()}"

        # OFFSET-FETCH句を追加（SQL Server用）
        pagination_clause = f" OFFSET {start} ROWS FETCH NEXT {length} ROWS ONLY"

        # データ取得クエリ
        data_query = base_query + where_clause + order_clause + pagination_clause
        results = db_manager.execute_query(data_query, tuple(params) if params else None)

        # レスポンスデータの整形
        data = []
        for row in results:
            data.append({
                'ID': row['ID'],
                '変化点NO': row['変化点NO'],
                'KH担当': row['KH担当'] or '',
                'KH初品納入変更日': row['KH初品納入変更日'].isoformat() if row['KH初品納入変更日'] else None,
                'KH初品納入実績初': row['KH初品納入実績初'].isoformat() if row['KH初品納入実績初'] else None,
                '流動可否': row['流動可否'] or '',
                '工程変更実施可否': row['工程変更実施可否'] or '',
                '起票部署': row['起票部署'] or '',
                'KH品番': row['KH品番'] or '',
                'KH品名': row['KH品名'] or '',
                '納入予定日': row['納入予定日'].isoformat() if row['納入予定日'] else None,
                'KH設変出図予定日': row['KH設変出図予定日'].isoformat() if row['KH設変出図予定日'] else None,
                'KH設変出図実績日': row['KH設変出図実績日'].isoformat() if row['KH設変出図実績日'] else None,
                '変更内容': row['変更内容'] or '',
                '特採後の処置': row['特採後の処置'] or 0,
                '流動判定日': row['流動判定日'].isoformat() if row['流動判定日'] else None,
                '切替基準日': row['切替基準日'].isoformat() if row['切替基準日'] else None,
                'KH管轄': row['KH管轄'] or '',
                '受付NO': row['受付NO'] or '',
                '連絡書NO': row['連絡書NO'] or '',
                '受付日': row['受付日'].isoformat() if row['受付日'] else None
            })

        # DataTables用のレスポンス
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error in api_changes_list: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/detail/<int:id>')
def detail(id):
    """詳細画面の表示"""
    return render_template('detail.html')

@app.route('/edit/<int:id>')
def edit(id):
    """編集画面の表示"""
    return render_template('detail.html')

@app.route('/api/changes/<int:id>', methods=['GET'])
def api_get_change(id):
    """変化点データの取得API"""
    try:
        # データ取得
        query = """
            SELECT * FROM [TC_変化点管理台帳] WHERE [ID] = %s
        """
        result = db_manager.execute_query(query, (id,))

        if not result or len(result) == 0:
            return jsonify({'error': '指定されたデータが見つかりません。'}), 404

        # レスポンスデータの整形
        data = result[0]
        response_data = {}
        for key, value in data.items():
            if value is not None and hasattr(value, 'isoformat'):
                response_data[key] = value.isoformat()
            else:
                response_data[key] = value

        return jsonify(response_data)

    except Exception as e:
        print(f"Error in api_get_change: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/changes/<int:id>', methods=['PUT'])
def api_update_change(id):
    """変化点データの更新API"""
    try:
        data = request.get_json()

        # 更新可能なフィールドを定義
        update_fields = [
            '素性', '受付No', '受付日', '受付NO', '連絡書NO',
            '起票部署', 'KH起票部署CODE', 'KH担当', 'KH管轄', 'KH工務区分',
            'KH品番', 'KH品名', '変更内容', '流動可否', '工程変更実施可否',
            '特採後の処置', 'KH初品納入変更日', 'KH初品納入実績初',
            '納入予定日', '流動判定日', 'KH設変出図予定日',
            'KH設変出図実績日', '切替基準日'
        ]

        # UPDATE文を構築
        update_parts = []
        params = []
        for field in update_fields:
            if field in data:
                update_parts.append(f"[{field}] = %s")
                # 空文字列をNULLに変換
                value = data[field] if data[field] != '' else None
                params.append(value)

        if not update_parts:
            return jsonify({'error': '更新するフィールドがありません。'}), 400

        # 更新時刻を追加
        update_parts.append("[入力時刻] = %s")
        params.append(datetime.now())

        # IDをパラメータに追加
        params.append(id)

        # UPDATE文を実行
        update_query = f"""
            UPDATE [TC_変化点管理台帳]
            SET {', '.join(update_parts)}
            WHERE [ID] = %s
        """

        db_manager.execute_query(update_query, tuple(params))

        return jsonify({'success': True, 'message': 'データを更新しました。'})

    except Exception as e:
        print(f"Error in api_update_change: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/changes/<int:id>', methods=['DELETE'])
def api_delete_change(id):
    """変化点データの削除API"""
    try:
        # データの存在確認
        check_query = "SELECT COUNT(*) as count FROM [TC_変化点管理台帳] WHERE [ID] = %s"
        result = db_manager.execute_query(check_query, (id,))

        if result[0]['count'] == 0:
            return jsonify({'error': '指定されたデータが見つかりません。'}), 404

        # 削除実行（物理削除）
        delete_query = "DELETE FROM [TC_変化点管理台帳] WHERE [ID] = %s"
        db_manager.execute_query(delete_query, (id,))

        return jsonify({'success': True, 'message': 'データを削除しました。'})

    except Exception as e:
        print(f"Error in api_delete_change: {str(e)}")
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
            kh_hinban = form_data.get('hinban')  # KH品番を取得
            hinmei = form_data.get('hinmei')  # 品名を取得

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
                [KH品番], [KH品名], [入力時刻]
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                kh_hinban,
                hinmei,
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