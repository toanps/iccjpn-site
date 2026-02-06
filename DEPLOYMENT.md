# ICC JAPAN Website - Cloudflare Pages デプロイガイド

## 📁 プロジェクト構成

```
iccjpn-site/
├── index.html          # メインページ（SEO最適化済み）
├── css/
│   └── style.css       # スタイルシート（レスポンシブ対応）
├── js/
│   └── main.js         # JavaScript（アニメーション・フォーム）
├── images/
│   └── favicon.svg     # ファビコン
├── robots.txt          # 検索エンジン用
├── sitemap.xml         # サイトマップ
├── DEPLOYMENT.md       # このファイル
└── SEO-CHECKLIST.md    # SEOチェックリスト
```

---

## 🚀 Cloudflare Pages へのデプロイ方法

### 方法1: GitHub連携（推奨）

#### Step 1: GitHubリポジトリを作成

```bash
cd ~/projects/iccjpn-site

# Gitを初期化
git init
git add .
git commit -m "Initial commit: ICC JAPAN website"

# GitHubにリポジトリを作成してプッシュ
# https://github.com/new でリポジトリ作成後:
git remote add origin https://github.com/YOUR_USERNAME/iccjpn-site.git
git branch -M main
git push -u origin main
```

#### Step 2: Cloudflare Pagesでプロジェクト作成

1. [Cloudflare Dashboard](https://dash.cloudflare.com/) にログイン
2. 左メニュー → **Pages** をクリック
3. **Create a project** をクリック
4. **Connect to Git** を選択
5. GitHubアカウントを連携（初回のみ）
6. `iccjpn-site` リポジトリを選択
7. 設定:
   - **Project name**: `iccjpn`
   - **Production branch**: `main`
   - **Build command**: (空欄のまま)
   - **Build output directory**: `/`
8. **Save and Deploy** をクリック

デプロイ完了後、`iccjpn.pages.dev` でアクセス可能になります。

---

### 方法2: 直接アップロード（簡単）

1. [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Pages**
2. **Create a project** → **Direct Upload**
3. プロジェクト名: `iccjpn`
4. **Upload assets** → `iccjpn-site` フォルダ内のすべてのファイルをドラッグ&ドロップ
5. **Deploy site** をクリック

---

## 🌐 カスタムドメイン設定 (iccjpn.com)

### 前提条件
- `iccjpn.com` がCloudflareのDNSで管理されていること
- または、他のレジストラでDNSレコードを設定できること

### Step 1: Cloudflare Pages でドメイン追加

1. Pages プロジェクト → **Custom domains** タブ
2. **Set up a custom domain** をクリック
3. `iccjpn.com` を入力
4. **Activate domain** をクリック

### Step 2: DNS設定（Cloudflare DNS使用の場合）

自動で設定されます。手動の場合:

```
Type: CNAME
Name: @
Content: iccjpn.pages.dev
Proxy: On (オレンジの雲)
```

www サブドメインも設定:

```
Type: CNAME
Name: www
Content: iccjpn.pages.dev
Proxy: On
```

### Step 3: www → apex リダイレクト設定

1. Cloudflare Dashboard → `iccjpn.com` → **Rules** → **Redirect Rules**
2. **Create rule**:
   - **Rule name**: `www to apex`
   - **When**: Hostname equals `www.iccjpn.com`
   - **Then**: Dynamic redirect to `https://iccjpn.com${http.request.uri.path}`
   - **Status code**: 301

---

## 📧 お問い合わせフォーム設定

### Formspree（推奨・無料枠あり）

1. [Formspree](https://formspree.io/) でアカウント作成
2. 新しいフォームを作成
3. フォームIDを取得（例: `xpzgdqwe`）
4. `index.html` のフォーム action を更新:

```html
<form action="https://formspree.io/f/xpzgdqwe" method="POST">
```

### その他の選択肢
- **Cloudflare Workers**: サーバーレスでメール送信
- **Netlify Forms**: Netlify使用時
- **Google Forms**: 埋め込み

---

## 🔍 Google Search Console 設定

### Step 1: プロパティ追加

1. [Google Search Console](https://search.google.com/search-console/) にアクセス
2. **プロパティを追加** → `https://iccjpn.com`
3. **所有権の確認** → DNS レコード（推奨）またはHTMLタグ

### Step 2: サイトマップ送信

1. Search Console → **サイトマップ**
2. `sitemap.xml` を入力して送信

---

## 📊 Google Analytics 設定

### Step 1: GA4 プロパティ作成

1. [Google Analytics](https://analytics.google.com/) にアクセス
2. **管理** → **プロパティを作成**
3. 測定ID（G-XXXXXXXXXX）を取得

### Step 2: コード追加

`index.html` の `</head>` 直前に追加:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## ⚡ パフォーマンス最適化（Cloudflare設定）

### 自動最適化を有効化

1. Cloudflare Dashboard → **Speed** → **Optimization**
2. 以下を有効化:
   - **Auto Minify**: JavaScript, CSS, HTML すべてチェック
   - **Brotli**: 圧縮を有効化
   - **Early Hints**: 有効化
   - **Rocket Loader**: 試験的に有効化（問題があれば無効に）

### キャッシュ設定

1. **Caching** → **Configuration**
2. **Browser Cache TTL**: 1 month
3. **Always Online**: 有効化

---

## ✅ デプロイ後チェックリスト

- [ ] `https://iccjpn.com` でサイトが表示される
- [ ] `https://www.iccjpn.com` が `iccjpn.com` にリダイレクトされる
- [ ] SSL証明書が有効（🔒マーク表示）
- [ ] モバイルで正常表示される
- [ ] お問い合わせフォームが動作する
- [ ] Google Search Console で所有権確認済み
- [ ] サイトマップが送信済み
- [ ] Google Analytics が動作している

---

## 🔧 更新方法

### GitHub連携の場合
```bash
# 変更をコミット
git add .
git commit -m "Update: 内容を更新"
git push
```
→ 自動でデプロイされます

### 直接アップロードの場合
1. Pages → プロジェクト → **Create new deployment**
2. 更新したファイルをアップロード

---

## 📞 サポート

何か問題があれば、Cloudflareのドキュメントを参照:
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Custom Domains](https://developers.cloudflare.com/pages/platform/custom-domains/)
