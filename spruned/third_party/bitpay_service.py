from spruned import settings
from spruned.service.abstract import RPCAPIService
from datetime import datetime
from spruned.third_party.http_client import HTTPClient


class BitpayService(RPCAPIService):
    def __init__(self, coin, httpclient=HTTPClient):
        assert coin == settings.Network.BITCOIN
        self._e_d = datetime(1970, 1, 1)
        self.client = httpclient(baseurl='https://insight.bitpay.com/api/')

    def getrawtransaction(self, txid, **_):
        data = self.client.get('tx/' + txid)
        return {
            'rawtx': None,
            'blockhash': data['blockhash'],
            'blockheight': data['blockheight'],
            'confirmations': data['confirmations'],
            'time': data['time'],
            'size': None,
            'txid': txid,
            'source': 'insight.bitpay.com'
        }

    def getblock(self, blockhash):
        print('getblock from %s' % self.__class__)
        d = self.client.get('block/' + blockhash)
        return {
            'hash': d['hash'],
            'confirmations': d['confirmations'],
            'strippedsize': None,
            'size': d['size'],
            'weight': None,
            'height': d['height'],
            'version': str(d['version']),
            'versionHex': None,
            'merkleroot': d['merkleroot'],
            'tx': None,
            'time': d['time'],
            'mediantime': None,
            'nonce': d['nonce'],
            'bits': d['bits'],
            'difficulty': int(float(d['difficulty'])),
            'chainwork': None,
            'previousblockhash': d['previousblockhash'],
            'nextblockhash': d.get('nextblockhash'),
            'source': 'blockexplorer.com'
        }

    def getblockheader(self, blockhash):
        raise NotImplementedError
