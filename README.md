# nauka-sensor-api
Raspberry Piに接続した以下のセンサからの情報を返すAPIサーバ

- [オムロン 環境センサ(USB型) 2JCIE-BU](https://www.fa.omron.co.jp/products/family/3724/)
- [CUSTOM CO2モニター CO2-mini](https://www.kk-custom.co.jp/emp/CO2-mini.html)

## 依存ライブラリ
- [CO2Meter](https://github.com/heinemml/CO2Meter)
- FastAPI
- pyserial
- uvicorn

## セットアップ手順
1. Python仮想環境の作成

```bash
python -m venv venv
source venv/bin/activate
```

2. 依存ライブラリのインストール

```bash
pip install git+https://github.com/heinemml/CO2Meter
pip install pyserial fastapi uvicorn
```

3. Raspberry Piが環境センサにアクセスするために必要な設定

```bash
sudo modprobe ftdi_sio
sudo chmod 777 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sudo echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
```

5. FastAPIサーバーの起動

```bash
sudo venv/bin/uvicorn main:app --host 0.0.0.0 --reload
```

## API docs
- http://localhost:8000/docs

## ライセンス
このプログラムは、以下のリポジトリで公開されているコードを使用しています。

- https://github.com/omron-devhub/2jciebu-usb-raspberrypi
- https://github.com/heinemml/CO2Meter

これらのコードは、MITライセンスの下で公開されています。詳細なライセンスについては、各リポジトリのライセンス条項を参照してください。
