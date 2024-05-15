# HSSAPI-Python  
[![PyPI](https://img.shields.io/badge/-Pypi-000.svg?logo=pypi&style=plastic)](https://pypi.org/project/HSS.py/) <img src="https://img.shields.io/badge/-Python-ffd700.svg?logo=python&style=plastic">
  
## 目的
HSSAPIをPythonで簡単にしようできるようにしたAPIラッパー

# 使用方法
***[HSS API ドキュメント](https://hss-dev-docs.aknet.tech/)***  
***APIラッパーは一部の機能をサポートしています。  API機能を全て活用したい場合、Request_HHSAPI.pyやHSS.pyのget_data関数を使用することにより処理ができると思われます。***  
## インストール
```
pip install HSS.py
```
### githubから直接インストールする
```
pip install git+https://github.com/HSS-Project/HSS.py.git
```
or 
```
pip install git+git@github.com:HSS-Project/HSS.py.git
```

## 初期設定
***HSS APIのアプリケーション画面でtokenを発行してください。***   
```py
import hss
import asyncio

client = hss.Client()

async def main():
    token = "HSS API token"
    await client.setup(token=token)

asyncio.run(main())
```
