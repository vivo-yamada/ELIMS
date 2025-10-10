# ELIMS 配色仕様書

## 概要
ELIMSシステムで使用している配色は、ブルー系統を基調としたモダンで清潔感のあるデザインです。

## カラーパレット

### メインカラー

| 用途 | カラーコード | 説明 |
|------|-------------|------|
| **プライマリーブルー（濃）** | `#1976d2` | メインのアクセントカラー、タイトル、重要なテキスト |
| **プライマリーブルー（明）** | `#2196f3` | ボタン、境界線、リンク、アクティブ状態 |
| **ライトブルー** | `#42a5f5` | サブボタン、補助的な要素 |

### 背景カラー

| 用途 | カラーコード | 説明 |
|------|-------------|------|
| **ページ背景（開始）** | `#f8faff` | グラデーション開始色 |
| **ページ背景（終了）** | `#e8f2ff` | グラデーション終了色 |
| **カード背景** | `#ffffff` (white) | メインコンテンツエリアの背景 |
| **セクション背景** | `#f8f9fa` | フォームセクション、フィルターエリアの背景 |
| **入力カード背景** | `#f8faff` | 入力フィールドをグループ化したカードの背景 |

### アクセントカラー（カード・ボーダー）

| 用途 | カラーコード | 説明 |
|------|-------------|------|
| **カードボーダー** | `#e3f2fd` | 入力カード、カテゴリカードの境界線 |
| **フォーカスカラー** | `rgba(33, 150, 243, 0.2)` | 入力フィールドのフォーカス時のシャドウ |
| **ホバー背景** | `#e3f2fd` | ラジオボタン、トグルアイテムの選択時背景 |
| **テーブルホバー** | `rgba(33, 150, 243, 0.1)` | テーブル行のホバー時背景 |

### ステータスカラー

| 用途 | カラーコード | 説明 |
|------|-------------|------|
| **成功** | `#4caf50` | 完了状態、成功ボタン |
| **警告** | `#ff9800` | 警告ボタン |
| **危険** | `#f44336` | 削除ボタン、エラー状態 |
| **セカンダリ** | `#6c757d` | キャンセルボタン、無効状態 |

### テキストカラー

| 用途 | カラーコード | 説明 |
|------|-------------|------|
| **見出しテキスト** | `#1976d2` | ページタイトル、セクションタイトル |
| **本文テキスト** | `#333` | 通常のテキスト |
| **ラベルテキスト** | `#495057` | フォームラベル |
| **サブテキスト** | `#666` | 補足説明、グレーアウトテキスト |

## グラデーション定義

### 背景グラデーション
```css
background: linear-gradient(135deg, #f8faff 0%, #e8f2ff 100%);
```

### プライマリボタングラデーション
```css
background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
```

### ヘッダーグラデーション（新規登録画面用）
```css
background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
```

### サブボタングラデーション
```css
background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
```

## 影（シャドウ）定義

### カードシャドウ
```css
box-shadow: 0 4px 12px rgba(33, 150, 243, 0.1);
```

### ヘッダーシャドウ
```css
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
```

### ボタンホバーシャドウ
```css
box-shadow: 0 5px 15px rgba(33, 150, 243, 0.4);
```

### 浮き上がり効果シャドウ
```css
box-shadow: 0 8px 24px rgba(33, 150, 243, 0.15);
```

## 適用例

### 1. ページ全体の基本スタイル
```css
body {
    background: linear-gradient(135deg, #f8faff 0%, #e8f2ff 100%);
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
```

### 2. メインカードコンテナ
```css
.main-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.1);
    padding: 30px;
    margin-top: 20px;
}
```

### 3. ページタイトル
```css
.page-title {
    color: #1976d2;
    font-weight: bold;
    margin-bottom: 30px;
    padding-bottom: 10px;
    border-bottom: 3px solid #2196f3;
}
```

### 4. セクションタイトル
```css
.section-title {
    color: #1976d2;
    font-size: 1.2rem;
    font-weight: bold;
    margin-top: 25px;
    margin-bottom: 15px;
    padding-left: 10px;
    border-left: 4px solid #2196f3;
}
```

### 5. プライマリボタン
```css
.btn-primary {
    background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
    border: none;
    transition: transform 0.2s;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(33, 150, 243, 0.4);
}
```

### 6. 入力フィールド
```css
.form-input, .form-select {
    width: 100%;
    padding: 12px 15px;
    border: 2px solid #ced4da;
    border-radius: 6px;
    font-size: 16px;
    transition: all 0.2s;
    background: white;
}

.form-input:focus, .form-select:focus {
    outline: none;
    border-color: #2196f3;
    box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2);
    transform: translateY(-1px);
}
```

### 7. ローディングスピナー
```css
.loading-spinner {
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #2196f3;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
```

### 8. テーブルホバー効果
```css
.table-hover tbody tr:hover {
    background-color: rgba(33, 150, 243, 0.1);
    cursor: pointer;
}
```

## デザイン原則

1. **清潔感**: 白背景に淡いブルーのグラデーションで清潔感を表現
2. **視認性**: 濃いブルー(#1976d2)で重要な情報を強調
3. **階層性**: グラデーションとシャドウで要素の階層を表現
4. **一貫性**: 全画面で同じカラーパレットを使用
5. **アクセシビリティ**: 十分なコントラスト比を確保

## ブランドカラーの使い分け

| シーン | カラー | 理由 |
|--------|--------|------|
| タイトル・見出し | `#1976d2` | 権威性と信頼感 |
| ボタン・アクション | `#2196f3` | アクティブ感と誘導性 |
| 背景 | `#f8faff → #e8f2ff` | 柔らかさと清潔感 |
| 選択・フォーカス | `#e3f2fd` | 優しい強調 |

## 注意事項

- 紫系の配色（`#667eea`, `#764ba2`）は**使用しない**
- 常にブルー系統（`#2196f3`, `#1976d2`）を使用する
- RGBAを使用する場合は、`rgba(33, 150, 243, ...)` を基準にする
- グラデーションの角度は常に `135deg` で統一

## バージョン情報

- **作成日**: 2025-10-06
- **バージョン**: 1.0
- **適用範囲**: ELIMS全画面（一覧、詳細、編集、新規登録）
