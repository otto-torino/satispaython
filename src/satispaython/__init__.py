from .api import create_payment, get_payment_details, obtain_key_id, test_authentication
from .auth import SatispayAuth
from .client import SatispayClient, AsyncSatispayClient

try:
    import importlib.metadata as _metadata
except ModuleNotFoundError:
    import importlib_metadata as _metadata

__version__ = _metadata.version(__name__)

__all__ = [
    'obtain_key_id',
    'test_authentication',
    'create_payment',
    'get_payment_details',
    'SatispayClient',
    'AsyncSatispayClient',
    'SatispayAuth',
]
