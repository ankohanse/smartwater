"""Constants for the DAB Pumps integration."""
import logging
import types

_LOGGER: logging.Logger = logging.getLogger(__package__)

GOOGLE_PUBLIC_API_KEY = 'AIzaSyBIZVEyu1r1lK_wRj8d2AIkr1ljk-Ruk2k'
GOOGLE_PROJECT_NAME = 'smartwater-app'
GOOGLE_PROJECT_ID = '1054539760629'

GOOGLE_APIS_LOGIN_URL = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword'
GOOGLE_APIS_REFRESH_URL = 'https://securetoken.googleapis.com/v1/token'
GOOGLE_FIRESTORE_URL = 'https://firestore.googleapis.com/v1'

ACCESS_TOKEN_EXPIRE_MARGIN = 60 # seconds

CALL_CONTEXT_SYNC = "SYNC"
CALL_CONTEXT_ASYNC = "ASYNC"

