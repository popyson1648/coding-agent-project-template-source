# Coding Agent Project Template Source

[English](README.md) | **日本語**

このリポジトリは、公開テンプレート `popyson1648/coding-agent-project-template` のソースリポジトリである。
`coding-agent-project-template/` にはテンプレート利用者へ配布する内容を置き、リポジトリルート側には公開ワークフロー、検証、計画、決定記録、保守向け文書を置く。

## 変更の扱い

テンプレート利用者向けの変更は `coding-agent-project-template/` 以下、公開ワークフロー、検証、計画、決定記録、保守向け文書の変更はリポジトリルート側で扱う。

## 作業場所の構成

```text
.
├── coding-agent-project-template/  公開テンプレートへ同期する内容
├── .plans/                         作業ごとの計画
├── .decisions/                     構造、方針、設計判断の記録
├── .project/                       このソースリポジトリの運用文書
├── .template/                      `.project/` と設定ファイルの雛形
├── scripts/verify.py               ローカル検証と CI で使う入口
├── README.md                       英語版 README
└── README.ja.md                    日本語版 README
```

## 変更前に読む文書

変更の種類ごとに、先に読む文書が決まる。
公開フローの変更は `.project/structure.md` と `.project/release.md`、検証や CI の変更は `.project/verification.toml`、`scripts/verify.py`、`.github/workflows/ci.yml`、テンプレート利用者向け説明の変更は `coding-agent-project-template/README.md` と `coding-agent-project-template/README.ja.md` が対象。

## 検証

変更後に実行するコマンド。

```bash
python3 scripts/verify.py
```

`scripts/verify.py` は実行権限を前提にしない。
`./scripts/verify.py` ではなく、`python3 scripts/verify.py` として実行する。

## 公開テンプレートへの反映

`coding-agent-project-template/` の変更は、ソースリポジトリの `main` ブランチに入ったあと、公開ワークフローによって公開リポジトリへ同期される。
公開後の復旧手順は `.project/release.md`。
