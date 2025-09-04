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
    return render_template('register_modern.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """変化点管理台帳の登録処理"""
    
    if request.method == 'GET':
        return render_template('register_modern.html')
    
    if request.method == 'POST':
        try:
            # フォームデータを取得
            form_data = request.form.to_dict()
            
            # チェックボックスの複数値を取得
            henkou_naiyou_list = request.form.getlist('henkou_naiyou')
            henkou_naiyou = ','.join(henkou_naiyou_list) if henkou_naiyou_list else None
            
            # 現在時刻を取得
            now = datetime.now()
            
            # INSERTクエリを構築
            insert_query = """
            INSERT INTO [TC_変化点管理台帳] (
                [素性], [変化点NO], [発行月日], [目的内容], [変更内容], 
                [実施期間], [切替時期], [切替基準日], [納入日], [客先設変],
                [客先データ], [製品ランク], [重大項目], [検査項目], [備考],
                [案], [決定], [入力時刻], [部品数], [ERRFL],
                [工変ランク], [起票部署], [連絡書NO], [受付NO], [工程変更実施可否],
                [流動可否], [初期管理解除可否], [受付日], [承認], [初品カード添付],
                [承認日付], [先行FL], [流動可否提出期限], [流動可否提出完了日], 
                [流動可否PDFパス], [添付ファイル有無], [納入予定日], [品管受付NO],
                [数量], [発行部署メーカ名], [流動判定日], [完了日], [特採後の処置],
                [MAILFLG_60D], [MAILFLG_76D], [KH品番], [KH品名], 
                [KH変更内容設備], [KH変更内容検査機器], [KH変更内容金型], 
                [KH変更内容冶工具], [KH変更内容製造条件], [KH変更内容工程],
                [KH変更内容製造場所], [KH変更内容材料], [KH変更内容副資材], 
                [KH変更内容その他], [KH回答書NO], [KH客先提出要否], 
                [KH客先連絡回答書], [KH客先連絡事前承認], [KH工程確認旧予定日],
                [KH工程確認旧実施日], [KH工程確認新予定日], [KH工程確認新実施日],
                [KH部品サンプル], [KH部品データ], [KH部品工程能力], [KH製品サンプル],
                [KH製品データ], [KH製品工程能力], [KH製品試組], [KH製品試験],
                [KH初品納入変更日], [KH初品納入実績初], [KH初品納入実績終],
                [KH特別実施項目], [KH保管場所], [KH返却日], [KH返却内容],
                [KH工務受付日], [KH工務区分], [KH工務備考], [KH管轄],
                [KH部品試験], [KH部品試組], [KH部品評価有無], [KH製品評価有無],
                [KH期限切れ], [KH設変NO], [KH変更内容まとめ], [KH担当],
                [KHフォロー日], [KH取消日], [KH配布日], [KH設変区分],
                [KH設変ランク], [KH起票部署CODE], [KH担当CODE], [KH部品サンプル状態],
                [KH部品データ状態], [KH部品工程能力状態], [KH部品試組状態], [KH部品試験状態],
                [KH製品サンプル状態], [KH製品データ状態], [KH製品工程能力状態],
                [KH製品試組状態], [KH製品試験状態], [KH客先連絡回答書状態],
                [KH客先連絡事前承認状態], [KH流動可否提出承認日], [KH工程確認要否],
                [KH部品サンプル変更日], [KH部品データ変更日], [KH部品工程能力変更日],
                [KH部品試組変更日], [KH部品試験変更日], [KH製品サンプル変更日],
                [KH製品データ変更日], [KH製品工程能力変更日], [KH製品試組変更日],
                [KH製品試験変更日], [KH特殊工程有無], [KH部品金型FP], [KH部品金型FP変更日],
                [KH部品金型FP状態], [KH最終フォロー日], [KH流動可否提出期限フォローCH],
                [KHフォローメール送信回数], [KH流動可否提出期限フォロー回数], 
                [KH流動可否提出期限状態], [KH変更内容物流], [リンクフォルダパス],
                [KH設変出図予定日], [KH設変出図実績日], [KH起票日], [KHフリー入力1],
                [KHフリー入力2], [KHフリー入力3], [KHフリー入力4], [KHTEL], [KHメールアドレス]
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
            """
            
            # パラメータを準備（フォームの値とデフォルト値）
            params = (
                form_data.get('komu_kubun'),  # 素性
                form_data.get('henkaiten_no'),  # 変化点NO
                datetime.strptime(form_data.get('kippu_bi'), '%Y-%m-%d') if form_data.get('kippu_bi') else None,  # 発行月日
                form_data.get('mokuteki_naiyou'),  # 目的内容
                henkou_naiyou,  # 変更内容
                form_data.get('jisshi_kikan'),  # 実施期間
                form_data.get('kirikae_jiki'),  # 切替時期
                datetime.strptime(form_data.get('kirikae_kijun_bi'), '%Y-%m-%d') if form_data.get('kirikae_kijun_bi') else None,  # 切替基準日
                form_data.get('nounyuu_bi'),  # 納入日
                form_data.get('kyakusaki_setsuhen'),  # 客先設変
                form_data.get('kyakusaki_data'),  # 客先データ
                form_data.get('seihin_rank'),  # 製品ランク
                form_data.get('juudai_koumoku'),  # 重大項目
                form_data.get('kensa_koumoku'),  # 検査項目
                form_data.get('bikou'),  # 備考
                0,  # 案
                0,  # 決定
                now,  # 入力時刻
                0,  # 部品数
                0,  # ERRFL
                form_data.get('kouhen_rank'),  # 工変ランク
                form_data.get('kippu_busho'),  # 起票部署
                form_data.get('renraku_sho_no'),  # 連絡書NO
                form_data.get('uketsuke_no'),  # 受付NO
                form_data.get('koutei_henkou_jisshi_kahi'),  # 工程変更実施可否
                form_data.get('ryuudou_kahi'),  # 流動可否
                form_data.get('shoki_kanri_kaijo_kahi'),  # 初期管理解除可否
                datetime.strptime(form_data.get('uketsuke_bi'), '%Y-%m-%d') if form_data.get('uketsuke_bi') else None,  # 受付日
                form_data.get('shounin'),  # 承認
                form_data.get('shohin_card_tenpu'),  # 初品カード添付
                datetime.strptime(form_data.get('shounin_hiduke'), '%Y-%m-%d') if form_data.get('shounin_hiduke') else None,  # 承認日付
                0,  # 先行FL
                datetime.strptime(form_data.get('ryuudou_kahi_teishutsu_kigen'), '%Y-%m-%d') if form_data.get('ryuudou_kahi_teishutsu_kigen') else None,  # 流動可否提出期限
                datetime.strptime(form_data.get('ryuudou_kahi_teishutsu_kanryou_bi'), '%Y-%m-%d') if form_data.get('ryuudou_kahi_teishutsu_kanryou_bi') else None,  # 流動可否提出完了日
                form_data.get('ryuudou_kahi_pdf_path'),  # 流動可否PDFパス
                form_data.get('tenpu_file_umu'),  # 添付ファイル有無
                datetime.strptime(form_data.get('nounyuu_yotei_bi'), '%Y-%m-%d') if form_data.get('nounyuu_yotei_bi') else None,  # 納入予定日
                form_data.get('hinkan_uketsuke_no'),  # 品管受付NO
                0,  # 数量
                form_data.get('hakkou_busho_maker_mei'),  # 発行部署メーカ名
                datetime.strptime(form_data.get('ryuudou_hantei_bi'), '%Y-%m-%d') if form_data.get('ryuudou_hantei_bi') else None,  # 流動判定日
                datetime.strptime(form_data.get('kanryou_bi'), '%Y-%m-%d') if form_data.get('kanryou_bi') else None,  # 完了日
                0,  # 特採後の処置
                0,  # MAILFLG_60D
                0,  # MAILFLG_76D
                form_data.get('hinban'),  # KH品番
                form_data.get('hinmei'),  # KH品名
                1 if 'henkou_setsubi' in henkou_naiyou_list else 0,  # KH変更内容設備
                1 if 'henkou_kensa_kiki' in henkou_naiyou_list else 0,  # KH変更内容検査機器
                1 if 'henkou_kanagata' in henkou_naiyou_list else 0,  # KH変更内容金型
                1 if 'henkou_jikougu' in henkou_naiyou_list else 0,  # KH変更内容冶工具
                1 if 'henkou_seizo_jooken' in henkou_naiyou_list else 0,  # KH変更内容製造条件
                1 if 'henkou_koutei' in henkou_naiyou_list else 0,  # KH変更内容工程
                1 if 'henkou_seizo_basho' in henkou_naiyou_list else 0,  # KH変更内容製造場所
                1 if 'henkou_zairyou' in henkou_naiyou_list else 0,  # KH変更内容材料
                1 if 'henkou_fuku_shizai' in henkou_naiyou_list else 0,  # KH変更内容副資材
                1 if 'henkou_sonota' in henkou_naiyou_list else 0,  # KH変更内容その他
                form_data.get('kh_kaitou_sho_no'),  # KH回答書NO
                form_data.get('kyakusaki_teishutsu_youhi'),  # KH客先提出要否
                form_data.get('kh_kyakusaki_renraku_kaitou_sho'),  # KH客先連絡回答書
                form_data.get('kh_kyakusaki_renraku_jizen_shounin'),  # KH客先連絡事前承認
                datetime.strptime(form_data.get('kh_koutei_kakunin_kyuu_yotei_bi'), '%Y-%m-%d') if form_data.get('kh_koutei_kakunin_kyuu_yotei_bi') else None,  # KH工程確認旧予定日
                datetime.strptime(form_data.get('kh_koutei_kakunin_kyuu_jisshi_bi'), '%Y-%m-%d') if form_data.get('kh_koutei_kakunin_kyuu_jisshi_bi') else None,  # KH工程確認旧実施日
                datetime.strptime(form_data.get('kh_koutei_kakunin_shin_yotei_bi'), '%Y-%m-%d') if form_data.get('kh_koutei_kakunin_shin_yotei_bi') else None,  # KH工程確認新予定日
                datetime.strptime(form_data.get('kh_koutei_kakunin_shin_jisshi_bi'), '%Y-%m-%d') if form_data.get('kh_koutei_kakunin_shin_jisshi_bi') else None,  # KH工程確認新実施日
                datetime.strptime(form_data.get('kh_buhin_sample'), '%Y-%m-%d') if form_data.get('kh_buhin_sample') else None,  # KH部品サンプル
                datetime.strptime(form_data.get('kh_buhin_data'), '%Y-%m-%d') if form_data.get('kh_buhin_data') else None,  # KH部品データ
                datetime.strptime(form_data.get('kh_buhin_koutei_nouryoku'), '%Y-%m-%d') if form_data.get('kh_buhin_koutei_nouryoku') else None,  # KH部品工程能力
                datetime.strptime(form_data.get('kh_seihin_sample'), '%Y-%m-%d') if form_data.get('kh_seihin_sample') else None,  # KH製品サンプル
                datetime.strptime(form_data.get('kh_seihin_data'), '%Y-%m-%d') if form_data.get('kh_seihin_data') else None,  # KH製品データ
                datetime.strptime(form_data.get('kh_seihin_koutei_nouryoku'), '%Y-%m-%d') if form_data.get('kh_seihin_koutei_nouryoku') else None,  # KH製品工程能力
                datetime.strptime(form_data.get('kh_seihin_shigumi'), '%Y-%m-%d') if form_data.get('kh_seihin_shigumi') else None,  # KH製品試組
                datetime.strptime(form_data.get('kh_seihin_shiken'), '%Y-%m-%d') if form_data.get('kh_seihin_shiken') else None,  # KH製品試験
                datetime.strptime(form_data.get('kh_shohin_nounyuu_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_shohin_nounyuu_henkou_bi') else None,  # KH初品納入変更日
                datetime.strptime(form_data.get('kh_shohin_nounyuu_jisseki_hatsu'), '%Y-%m-%d') if form_data.get('kh_shohin_nounyuu_jisseki_hatsu') else None,  # KH初品納入実績初
                datetime.strptime(form_data.get('kh_shohin_nounyuu_jisseki_owari'), '%Y-%m-%d') if form_data.get('kh_shohin_nounyuu_jisseki_owari') else None,  # KH初品納入実績終
                form_data.get('kh_tokubetsu_jisshi_koumoku'),  # KH特別実施項目
                form_data.get('kh_hokan_basho'),  # KH保管場所
                datetime.strptime(form_data.get('henkyaku_bi'), '%Y-%m-%d') if form_data.get('henkyaku_bi') else None,  # KH返却日
                form_data.get('kh_henkyaku_naiyou'),  # KH返却内容
                datetime.strptime(form_data.get('komu_uketsuke_bi'), '%Y-%m-%d') if form_data.get('komu_uketsuke_bi') else None,  # KH工務受付日
                form_data.get('komu_kubun'),  # KH工務区分
                form_data.get('komu_bikou'),  # KH工務備考
                form_data.get('kankatsu'),  # KH管轄
                datetime.strptime(form_data.get('kh_buhin_shiken'), '%Y-%m-%d') if form_data.get('kh_buhin_shiken') else None,  # KH部品試験
                datetime.strptime(form_data.get('kh_buhin_shigumi'), '%Y-%m-%d') if form_data.get('kh_buhin_shigumi') else None,  # KH部品試組
                form_data.get('kh_buhin_hyouka_umu'),  # KH部品評価有無
                form_data.get('kh_seihin_hyouka_umu'),  # KH製品評価有無
                0,  # KH期限切れ
                form_data.get('kh_setsuhen_no'),  # KH設変NO
                form_data.get('kh_henkou_naiyou_matome'),  # KH変更内容まとめ
                form_data.get('tantousha'),  # KH担当
                form_data.get('kh_follow_bi'),  # KHフォロー日
                datetime.strptime(form_data.get('torikeshi_bi'), '%Y-%m-%d') if form_data.get('torikeshi_bi') else None,  # KH取消日
                datetime.strptime(form_data.get('haifu_bi'), '%Y-%m-%d') if form_data.get('haifu_bi') else None,  # KH配布日
                form_data.get('kh_setsuhen_kubun'),  # KH設変区分
                form_data.get('kh_setsuhen_rank'),  # KH設変ランク
                form_data.get('kh_kippu_busho_code'),  # KH起票部署CODE
                form_data.get('kh_tantou_code'),  # KH担当CODE
                form_data.get('kh_buhin_sample_joutai'),  # KH部品サンプル状態
                form_data.get('kh_buhin_data_joutai'),  # KH部品データ状態
                form_data.get('kh_buhin_koutei_nouryoku_joutai'),  # KH部品工程能力状態
                form_data.get('kh_buhin_shigumi_joutai'),  # KH部品試組状態
                form_data.get('kh_buhin_shiken_joutai'),  # KH部品試験状態
                form_data.get('kh_seihin_sample_joutai'),  # KH製品サンプル状態
                form_data.get('kh_seihin_data_joutai'),  # KH製品データ状態
                form_data.get('kh_seihin_koutei_nouryoku_joutai'),  # KH製品工程能力状態
                form_data.get('kh_seihin_shigumi_joutai'),  # KH製品試組状態
                form_data.get('kh_seihin_shiken_joutai'),  # KH製品試験状態
                form_data.get('kh_kyakusaki_renraku_kaitou_sho_joutai'),  # KH客先連絡回答書状態
                form_data.get('kh_kyakusaki_renraku_jizen_shounin_joutai'),  # KH客先連絡事前承認状態
                datetime.strptime(form_data.get('kh_ryuudou_kahi_teishutsu_shounin_bi'), '%Y-%m-%d') if form_data.get('kh_ryuudou_kahi_teishutsu_shounin_bi') else None,  # KH流動可否提出承認日
                form_data.get('kh_koutei_kakunin_youhi'),  # KH工程確認要否
                datetime.strptime(form_data.get('kh_buhin_sample_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_buhin_sample_henkou_bi') else None,  # KH部品サンプル変更日
                datetime.strptime(form_data.get('kh_buhin_data_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_buhin_data_henkou_bi') else None,  # KH部品データ変更日
                datetime.strptime(form_data.get('kh_buhin_koutei_nouryoku_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_buhin_koutei_nouryoku_henkou_bi') else None,  # KH部品工程能力変更日
                datetime.strptime(form_data.get('kh_buhin_shigumi_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_buhin_shigumi_henkou_bi') else None,  # KH部品試組変更日
                datetime.strptime(form_data.get('kh_buhin_shiken_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_buhin_shiken_henkou_bi') else None,  # KH部品試験変更日
                datetime.strptime(form_data.get('kh_seihin_sample_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_seihin_sample_henkou_bi') else None,  # KH製品サンプル変更日
                datetime.strptime(form_data.get('kh_seihin_data_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_seihin_data_henkou_bi') else None,  # KH製品データ変更日
                datetime.strptime(form_data.get('kh_seihin_koutei_nouryoku_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_seihin_koutei_nouryoku_henkou_bi') else None,  # KH製品工程能力変更日
                datetime.strptime(form_data.get('kh_seihin_shigumi_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_seihin_shigumi_henkou_bi') else None,  # KH製品試組変更日
                datetime.strptime(form_data.get('kh_seihin_shiken_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_seihin_shiken_henkou_bi') else None,  # KH製品試験変更日
                1 if form_data.get('tokushu_koutei_umu') == '有' else 2,  # KH特殊工程有無
                datetime.strptime(form_data.get('kh_buhin_kanagata_fp'), '%Y-%m-%d') if form_data.get('kh_buhin_kanagata_fp') else None,  # KH部品金型FP
                datetime.strptime(form_data.get('kh_buhin_kanagata_fp_henkou_bi'), '%Y-%m-%d') if form_data.get('kh_buhin_kanagata_fp_henkou_bi') else None,  # KH部品金型FP変更日
                form_data.get('kh_buhin_kanagata_fp_joutai'),  # KH部品金型FP状態
                datetime.strptime(form_data.get('kh_saishuu_follow_bi'), '%Y-%m-%d') if form_data.get('kh_saishuu_follow_bi') else None,  # KH最終フォロー日
                0,  # KH流動可否提出期限フォローCH
                0,  # KHフォローメール送信回数
                0,  # KH流動可否提出期限フォロー回数
                form_data.get('kh_ryuudou_kahi_teishutsu_kigen_joutai'),  # KH流動可否提出期限状態
                1 if 'henkou_butsuryu' in henkou_naiyou_list else 0,  # KH変更内容物流
                form_data.get('link_folder_path'),  # リンクフォルダパス
                datetime.strptime(form_data.get('shutsuzu_yotei_bi'), '%Y-%m-%d') if form_data.get('shutsuzu_yotei_bi') else None,  # KH設変出図予定日
                datetime.strptime(form_data.get('shutsuzu_jisseki_bi'), '%Y-%m-%d') if form_data.get('shutsuzu_jisseki_bi') else None,  # KH設変出図実績日
                datetime.strptime(form_data.get('kippu_bi'), '%Y-%m-%d') if form_data.get('kippu_bi') else None,  # KH起票日
                form_data.get('free_nyuryoku_1'),  # KHフリー入力1
                form_data.get('free_nyuryoku_2'),  # KHフリー入力2
                form_data.get('free_nyuryoku_3'),  # KHフリー入力3
                form_data.get('free_nyuryoku_4'),  # KHフリー入力4
                form_data.get('tel'),  # KHTEL
                form_data.get('email')  # KHメールアドレス
            )
            
            # データベースに挿入
            result = db_manager.execute_insert(insert_query, params)
            
            flash('変化点管理台帳が正常に登録されました。', 'success')
            return redirect(url_for('register'))
            
        except Exception as e:
            error_message = f"登録処理中にエラーが発生しました: {str(e)}"
            print(f"Error: {error_message}")
            print(f"Traceback: {traceback.format_exc()}")
            flash(error_message, 'error')
            return render_template('register_modern.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error='ページが見つかりません。'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='サーバー内部エラーが発生しました。'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)