from pywallet import wallet
import qrcode
from io import StringIO

def CreateBTCWallet():
    seed = wallet.generate_mnemonic()
    w = wallet.create_wallet(network="BTC", seed=seed, children=0)
    img = qrcode.make("bitcoin:" + w['address'])
    return img

def CreateETHWallet():
    seed = wallet.generate_mnemonic()
    w = wallet.create_wallet(network="ETH", seed=seed, children=0)
    img = qrcode.make("ethereum:" + w['address'])
    return img

def CreateLTCWallet():
    seed = wallet.generate_mnemonic()
    w = wallet.create_wallet(network="LTC", seed=seed, children=0)
    img = qrcode.make("litecoin:" + w['address'])
    return img

def GenerateImage(address, coin):
    img = qrcode.make(coin + ":" + address)
    #img = StringIO(img.tobytes("raw", 'RGBA'))
    data_uri = 'data:image/jpg;base64,'
    data_uri += str(base64.b64encode(img.tobytes()),'utf8')
    return data_uri
