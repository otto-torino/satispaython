from ._api import create_payment, get_payment_details, obtain_key_id, test_authentication
from ._auth import SatispayAuth
from ._client import SatispayClient, AsyncSatispayClient

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)

__all__ = [
    'obtain_key_id',
    'test_authentication',
    'create_payment',
    'get_payment_details',
    'SatispayClient',
    'AsyncSatispayClient',
    'SatispayAuth',
]
