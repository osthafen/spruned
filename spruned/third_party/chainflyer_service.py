import bitcoin
import struct
from spruned import settings
from spruned.service.abstract import RPCAPIService
from datetime import datetime
from spruned.third_party.http_client import HTTPClient


class ChainFlyerService(RPCAPIService):
    def __init__(self, coin):
        assert coin == settings.Network.BITCOIN
        self._e_d = datetime(1970, 1, 1)
        self.client = HTTPClient(baseurl='https://chainflyer.bitflyer.jp/v1/')

    def getrawtransaction(self, txid, **_):
        data = self.client.get('tx/' + txid)
        return {
            'rawtx': None,
            'blockhash': None,
            'blockheight': data['block_height'],
            'confirmations': data['confirmed'],
            'time': None,
            'size': data['size'],
            'txid': data['tx_hash'],
            'source': 'chainflyer'
        }

    def getblock(self, blockhash):
        print('getblock from %s' % self.__class__)
        d = self.client.get('block/' + blockhash)
        _c = d['timestamp']
        utc_time = datetime.strptime(_c, "%Y-%m-%dT%H:%M:%SZ")
        epoch_time = int((utc_time - self._e_d).total_seconds())
        return {
            'hash': d['block_hash'],
            'confirmations': None,
            'strippedsize': None,
            'size': None,
            'weight': None,
            'height': d['height'],
            'version': str(d['version']),
            'versionHex': None,
            'merkleroot': d['merkle_root'],
            'tx': d['tx_hashes'],
            'time': epoch_time,
            'mediantime': None,
            'nonce': d['nonce'],
            'bits': bitcoin.safe_hexlify(struct.pack('l', d['bits'])[:4][::-1]),
            'difficulty': None,
            'chainwork': None,
            'previousblockhash': d['prev_block'],
            'nextblockhash': None,
            'source': 'chainflyer'
        }

    def getblockheader(self, blockhash):
        raise NotImplementedError
