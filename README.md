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
### Python仮想環境の作成

```bash
python -m venv venv
source venv/bin/activate
```

### 依存ライブラリのインストール

```bash
pip install git+https://github.com/heinemml/CO2Meter
pip install pyserial fastapi uvicorn
```

### Raspberry Piが環境センサにアクセスするために必要な設定
#### ユーザーグループの設定

```bash
sudo groupadd sensors
sudo usermod -a -G sensors <username>
```

#### udevルールの作成

/etc/udev/rules.d/60-omron-sensor.rules
```
ACTION=="add", ATTRS{idVendor}=="0590", ATTRS{idProduct}=="00d4", RUN+="/sbin/modprobe ftdi_sio" RUN+="/bin/sh -c 'echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id'", SYMLINK+="2JCIE-BU"
SUBSYSTEM=="tty", ATTRS{idVendor}=="0590", ATTRS{idProduct}=="00d4", GROUP="sensors", MODE="0660"
```

/etc/udev/rules.d/61-custom-co2-monitor.rules
```
ACTION=="remove", GOTO="co2mini_end"
SUBSYSTEMS=="usb", KERNEL=="hidraw*", ATTRS{idVendor}=="04d9", ATTRS{idProduct}=="a052", GROUP="sensors", MODE="0660", SYMLINK+="co2mini%n", GOTO="co2mini_end"
LABEL="co2mini_end"
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="04d9", ATTRS{idProduct}=="a052", GROUP="sensors", MODE="0660"
```

5. FastAPIサーバーの起動

```bash
uvicorn main:app --host 0.0.0.0 --reload
```

## API docs
- http://localhost:8000/docs

## ライセンス
このソフトウェアはMITライセンスの下で公開されています。詳細なライセンスについてはLICENCE.txtを参照してください。

また、このソフトウェアは以下のリポジトリで公開されているコードを使用しています。

- https://github.com/omron-devhub/2jciebu-usb-raspberrypi
- https://github.com/heinemml/CO2Meter

これらのコードは、MITライセンスの下で公開されています。詳細なライセンスについては、各リポジトリのライセンス条項を参照してください。
