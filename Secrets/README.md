Create a config.py file inside the Secrets folder.
It is just a file with key value pairs to hide the secrets/keys/passwords etc.
The content of config.py would be something like this:
STORAGE_ACCOUNT_NAME = '<STORAGE_ACCOUNT_NAME>'

STORAGE_ACCOUNT_KEY = '<STORAGE_ACCOUNT_KEY>'

CONTAINER_NAME='<CONTAINER_NAME>'
BLOB_OBJECT='<BLOB_OBJECT>'


SAS_TOKEN='<SAS_TOKEN>'
SAS_DATE_START='<SAS_DATE_START>'
SAS_DATE_EXPIRY='<SAS_DATE_EXPIRY>'

MAP_ENTERPRISE_MASTER_KEY='<MAP_ENTERPRISE_MASTER_KEY>'
MAP_ENTERPRISE_QUERY_KEY='<MAP_ENTERPRISE_QUERY_KEY>'
MAP_DEV_KEY='<MAP_DEV_KEY>'

You can call the module like this way:
import secrets_keys.config as config

And then refer the variable like:
config.STORAGE_ACCOUNT_NAME
config.STORAGE_ACCOUNT_KEY ... you get the point