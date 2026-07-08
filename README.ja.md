# Coding Agent Project Template Source

[English](README.md) | **日本語**

このリポジトリは、公開テンプレート `popyson1648/coding-agent-project-template` のソースリポジトリです。
公開テンプレートとして配布する内容は `coding-agent-project-template/` 以下にあります。
それ以外のファイルは、テンプレートを保守し、検証し、公開先へ反映するための管理用ファイルです。

## このリポジトリの役割

このリポジトリでは、「テンプレート利用者に配る内容」と「テンプレートを配るための仕組み」を分けて扱います。
テンプレート利用者に配る内容を変える場合は、`coding-agent-project-template/` 以下を編集します。
公開ワークフロー、検証、計画、決定記録、保守向け文書を変える場合は、リポジトリルート側を編集します。
この境界が曖昧になると、公開テンプレートに管理用ファイルが混ざるか、公開に必要な検証が外れます。

## 作業場所

- **`coding-agent-project-template/`**：公開テンプレートへ同期される内容。
- **`.plans/`**：作業計画。
- **`.decisions/`**：構造、方針、設計判断の記録。
- **`.project/`**：このソースリポジトリの運用文書。
- **`.template/`**：`.project/` と設定ファイルの雛形。
- **`scripts/verify.py`**：ローカル検証と CI で使う入口。

## 変更前に読む文書

変更の種類に合わせて、先に読む文書を選びます。
公開フローを変える場合は、`.project/structure.md` と `.project/release.md` を読みます。
検証や CI を変える場合は、`.project/verification.toml`、`scripts/verify.py`、`.github/workflows/ci.yml` を読みます。
テンプレート利用者向けの説明を変える場合は、`coding-agent-project-template/README.md` と `coding-agent-project-template/README.ja.md` を読みます。

## 検証

変更後は次のコマンドを実行します。

```bash
python3 scripts/verify.py
```

`scripts/verify.py` は実行権限を前提にしません。
`./scripts/verify.py` ではなく、`python3 scripts/verify.py` として実行します。
pre-commit を使う環境では、同じ検証がローカルフックからも実行されます。

## 公開テンプレートへの反映

`coding-agent-project-template/` の変更は、ソースリポジトリの `main` ブランチに入ったあと、公開ワークフローによって公開リポジトリへ同期されます。
公開リポジトリを直接修正すると、次回の同期でソースリポジトリとの差分が分かりにくくなります。
公開後の復旧が必要な場合も、`.project/release.md` の手順を先に確認します。
