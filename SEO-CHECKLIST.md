# ICC JAPAN Website - SEO チェックリスト

## ✅ 実装済み SEO 要素

### 📄 基本メタタグ

| 項目 | 状態 | 内容 |
|------|------|------|
| Title タグ | ✅ | `ベトナム人材紹介・採用支援 \| 株式会社ICC JAPAN【大阪】` |
| Meta Description | ✅ | 200文字以内、キーワード含む |
| Meta Keywords | ✅ | 主要キーワード10個 |
| Canonical URL | ✅ | `https://iccjpn.com/` |
| Robots | ✅ | `index, follow` |
| Viewport | ✅ | レスポンシブ対応 |
| Charset | ✅ | UTF-8 |

### 🔍 日本語キーワード最適化

#### ターゲットキーワード（本文に含まれる）
- ✅ ベトナム人材紹介
- ✅ 技能実習生
- ✅ 特定技能
- ✅ エンジニア採用
- ✅ 外国人採用
- ✅ ベトナム人エンジニア
- ✅ 人材紹介会社
- ✅ 大阪
- ✅ N3日本語
- ✅ 外国人労働者

#### LSIキーワード（関連語）
- ✅ 採用支援
- ✅ 在留資格
- ✅ 成功報酬
- ✅ 紹介実績
- ✅ 定着率

### 🏢 構造化データ (Schema.org)

| スキーマタイプ | 状態 | 用途 |
|---------------|------|------|
| Organization | ✅ | 会社情報 |
| EmploymentAgency | ✅ | 人材紹介業 |
| PostalAddress | ✅ | 住所情報 |
| ContactPoint | ✅ | 連絡先 |
| OpeningHours | ✅ | 営業時間 |

### 📱 ソーシャルメディア最適化

| 項目 | 状態 |
|------|------|
| Open Graph (Facebook) | ✅ |
| Twitter Cards | ✅ |
| OG Image | ⚠️ 画像ファイルを追加必要 |

### 🔗 技術的SEO

| 項目 | 状態 |
|------|------|
| robots.txt | ✅ |
| sitemap.xml | ✅ |
| HTTPs | ✅ (Cloudflare) |
| モバイル対応 | ✅ |
| ページ速度 | ✅ (軽量CSS/JS) |

---

## 📋 デプロイ後のTODO

### 必須タスク

- [ ] **Google Search Console 設定**
  1. プロパティ追加: `https://iccjpn.com`
  2. 所有権確認（DNS または HTMLタグ）
  3. サイトマップ送信: `sitemap.xml`

- [ ] **Google Analytics 設定**
  1. GA4 プロパティ作成
  2. 測定IDを `index.html` に追加

- [ ] **お問い合わせフォーム設定**
  1. Formspree アカウント作成
  2. フォームID取得
  3. `index.html` の action 属性を更新

### 推奨タスク

- [ ] **OG画像作成**
  - サイズ: 1200x630px
  - ファイル: `/images/og-image.jpg`
  - 内容: 会社ロゴ + キャッチコピー

- [ ] **会社ロゴ作成**
  - SVG形式推奨
  - ファイル: `/images/logo.svg`

- [ ] **写真追加**
  - オフィス写真: `/images/office.jpg`
  - スタッフ写真（許可あれば）
  - 紹介実績イメージ

---

## 🎯 追加SEO施策（推奨）

### 短期（1-2週間）

1. **Google ビジネスプロフィール登録**
   - https://www.google.com/business/
   - 地域検索で上位表示

2. **業界ディレクトリ登録**
   - 人材紹介会社一覧サイト
   - 大阪の企業ディレクトリ

3. **サイト速度チェック**
   - [PageSpeed Insights](https://pagespeed.web.dev/)
   - [GTmetrix](https://gtmetrix.com/)

### 中期（1-3ヶ月）

1. **コンテンツマーケティング**
   - ブログページ追加（/blog/）
   - 記事例:
     - 「ベトナム人エンジニアを採用するメリット」
     - 「特定技能と技能実習の違い」
     - 「外国人採用の手続きガイド」

2. **事例・お客様の声ページ**
   - 採用成功事例
   - 企業の声（許可取得後）

3. **FAQ ページ**
   - よくある質問
   - FAQ Schema 追加

### 長期（3-6ヶ月）

1. **バックリンク獲得**
   - 業界メディア掲載
   - プレスリリース配信
   - 関連企業との相互リンク

2. **多言語対応**
   - ベトナム語ページ追加
   - 英語ページ追加

---

## 📊 KPI・目標設定

### 検索順位目標（6ヶ月後）

| キーワード | 目標順位 |
|-----------|---------|
| ベトナム人材紹介 大阪 | 10位以内 |
| ベトナム人エンジニア 採用 | 20位以内 |
| 技能実習生 紹介 大阪 | 10位以内 |
| 特定技能 人材紹介 | 30位以内 |

### トラフィック目標

- 1ヶ月目: 100 セッション/月
- 3ヶ月目: 500 セッション/月
- 6ヶ月目: 1,000 セッション/月

### コンバージョン目標

- お問い合わせ: 5件/月
- 電話問い合わせ: 3件/月

---

## 🔧 SEOツール（無料）

| ツール | 用途 | URL |
|-------|------|-----|
| Google Search Console | 検索パフォーマンス | search.google.com/search-console |
| Google Analytics | トラフィック分析 | analytics.google.com |
| PageSpeed Insights | ページ速度 | pagespeed.web.dev |
| Rich Results Test | 構造化データ確認 | search.google.com/test/rich-results |
| Mobile-Friendly Test | モバイル対応確認 | search.google.com/test/mobile-friendly |

---

## 📝 定期メンテナンス

### 月次
- [ ] Search Console でエラー確認
- [ ] ランキング変動チェック
- [ ] お問い合わせ数確認

### 四半期
- [ ] コンテンツ更新（実績数など）
- [ ] 競合サイト分析
- [ ] キーワード見直し

### 年次
- [ ] サイト全体リニューアル検討
- [ ] 年間実績更新
- [ ] 構造化データ更新
