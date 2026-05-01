import hmac
import hashlib
import time
import requests
import logging
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    """Wrapper for the Binance Futures REST API."""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
        
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })

    def _generate_signature(self, query_string: str) -> str:
        """Generates HMAC SHA256 signature required by Binance."""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def send_signed_request(self, method: str, endpoint: str, payload: dict = None) -> dict:
        """Sends an authenticated request to the Binance API."""
        if payload is None:
            payload = {}
            
        # Add timestamp required for all signed endpoints
        payload['timestamp'] = int(time.time() * 1000)
        
        query_string = urlencode(payload)
        signature = self._generate_signature(query_string)
        
        # Binance requires the query string and signature in the URL for signed requests
        url = f"{self.base_url}{endpoint}?{query_string}&signature={signature}"

        logger.info(f"API Request: {method} {self.base_url}{endpoint} | Params: {payload}")
        
        try:
            response = self.session.request(method, url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"API Response: {data}")
            return data
            
        except requests.exceptions.HTTPError as e:
            # Binance returns specific error details in the JSON body
            try:
                err_data = response.json()
                err_msg = err_data.get('msg', response.text)
            except ValueError:
                err_msg = response.text
                
            logger.error(f"HTTP Error: {e} | Binance Response: {err_msg}")
            raise Exception(f"Binance API Error: {err_msg}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error: {e}")
            raise Exception(f"Network communication failed: {e}")
