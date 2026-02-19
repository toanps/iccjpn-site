# ICC JAPAN Website - SEO チェックリスト

## ✅ 実装済み SEO 要素

### 📄 基本メタタグ

| 項目 | 状態 | 内容 |
|------|------|------|
| Title タグ | ✅ | `ベトナム人材紹介・採用支援 \| 株式会社ICC JAPAN【大阪】` |
| Meta Description | ✅ | 200文字以内、キーワード含む |
| Meta Keywords | ✅ | 主要キーワード10個 |
| Canonical URL | ✅ | 全ページに設定済み |
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

### 🏢 構造化データ (Schema.org)

| スキーマタイプ | 状態 |
|---------------|------|
| Organization | ✅ |
| EmploymentAgency | ✅ |
| PostalAddress | ✅ |
| ContactPoint | ✅ |
| OpeningHours | ✅ |

### 📱 ソーシャルメディア最適化

| 項目 | 状態 |
|------|------|
| Open Graph (Facebook) | ✅ |
| Twitter Cards | ✅ |
| OG Image (1200×630) | ✅ 生成済み |

### 🔗 技術的SEO

| 項目 | 状態 |
|------|------|
| robots.txt | ✅ |
| sitemap.xml | ✅ |
| HTTPS | ✅ (Cloudflare Pages) |
| モバイル対応 | ✅ |
| ページ速度 | ✅ |

### 📊 アナリティクス・フォーム

| 項目 | 状態 |
|------|------|
| Google Analytics 4 | ⚠️ プレースホルダー設置済み（測定ID要設定） |
| お問い合わせフォーム | ⚠️ Formspree 設定待ち（YOUR_FORM_ID を要置換） |
| スパム対策 (honeypot) | ✅ |
| 送信成功メッセージ | ✅ |

---

## 🚀 オーナー向け残作業 (Remaining Actions for Owner)

### 必須タスク

- [ ] **Google Analytics 4 設定**
  1. https://analytics.google.com → Admin → Data Streams で測定ID取得
  2. 全HTMLファイル（index.html, faq.html, news.html）の `G-XXXXXXXXXX` を実際のIDに置換

- [ ] **Google Search Console 登録**
  1. https://search.google.com/search-console でプロパティ追加: `https://iccjpn.com`
  2. 所有権確認（DNS または HTMLタグ）
  3. サイトマップ送信: `https://iccjpn.com/sitemap.xml`

- [ ] **Google ビジネスプロフィール登録**
  1. https://www.google.com/business/ で登録
  2. 地域検索（「人材紹介 大阪」等）で上位表示に効果大

- [ ] **Cloudflare Pages デプロイ**
  1. Cloudflare Pages に GitHub 連携でデプロイ（DEPLOYMENT_EN.md 参照）
  2. Formspree（https://formspree.io）でフォーム作成 → YOUR_FORM_ID を置換


### 推奨タスク

- [ ] 会社ロゴ画像の追加（`/images/logo.png`）
- [ ] オフィス写真の追加（`/images/office.jpg`）
- [ ] PageSpeed Insights でパフォーマンス確認

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
