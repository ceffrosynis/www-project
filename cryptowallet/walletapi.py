from pywallet import wallet
import qrcode
from io import StringIO
import io
import base64

def CreateBTCWallet():
    seed = wallet.generate_mnemonic()
    w = wallet.create_wallet(network="BTC", seed=seed, children=0)
    return w['address']

def CreateETHWallet():
    seed = wallet.generate_mnemonic()
    w = wallet.create_wallet(network="ETH", seed=seed, children=0)
    img = qrcode.make("ethereum:" + w['address'])
    return w['address']

def CreateLTCWallet():
    seed = wallet.generate_mnemonic()
    w = wallet.create_wallet(network="LTC", seed=seed, children=0)
    img = qrcode.make("litecoin:" + w['address'])
    return w['address']

def GenerateImage(address, coin):
    img = qrcode.make(coin + ":" + address)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    b64_src = base64.b64encode(imgByteArr)
    data_uri = 'data:image/png;base64, ' + str(b64_src, 'utf8')
    return data_uri
