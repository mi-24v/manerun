## maneRun

[テレバイス:テレビと体験するシステム　テレビ×デバイスで テレビと体験](https://protopedia.net/prototype/89885ff2c83a10305ee08bd507c1049c)の真似ラン機能のWeb実装

## Usage

* Google App Engine Standard(Python 3.7+ runtime)で動作します
    * 機械学習機能は、ロード時間が長すぎるため使用されていません(ローカル実行なら問題なし)。

Google Cloud SDKがログインまでできているものとします

1. プロジェクトを作成

```sh
gcloud projects create "[YOUR_PROJECT_ID]"
gcloud config set project "[YOUR_PROJECT_ID]"
gcloud app create --project="[YOUR_PROJECT_ID]"
```

2. バケット等作成

* FireStoreに `user` KINDを作成するか `util.py` 13行目のKIND名を適宜変更
* `manerun-motions` バケットを作成するか `util.py` 14行目のバケット名を適宜変更

3. デプロイ

secret.yaml.exampleを適宜変更した後secret.yamlにリネーム

```sh
gcloud app deploy
```
