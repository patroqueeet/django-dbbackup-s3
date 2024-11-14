from django.conf import settings
from environ import Env

env = Env()

#####################
# Django Storages 👇 #
#####################

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="ap-south-1")

DROPBOX_OAUTH2_TOKEN = env("DROPBOX_OAUTH2_TOKEN", default="")
DROPBOX_OAUTH2_REFRESH_TOKEN = env("DROPBOX_OAUTH2_REFRESH_TOKEN", default="")
DROPBOX_APP_KEY = env("DROPBOX_APP_KEY", default="")
DROPBOX_APP_SECRET = env("DROPBOX_APP_SECRET", default="")
#####################
# Sync App Settings #
#####################

SYNC_S3_BUCKET = env("SYNC_S3_BUCKET", default=AWS_STORAGE_BUCKET_NAME)
SYNC_S3_DIR = env("SYNC_S3_DIR", default="/")
SYNC_DROPBOX_DIR = env("SYNC_DROPBOX_DIR", default="upload-dir/")
SYNC_TARGET_FILE_NAME = env("SYNC_TARGET_FILE_NAME", default="backup.tar.gz")

AWS_S3_ENDPOINT_URL = "https://objects.rma.cloudscale.ch"
AWS_QUERYSTRING_EXPIRE = "600"
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None  # storage 1.10 requirement to use bucket default
AWS_PROXY_PATH_NAME = "s3media"

AWS_S3_CUSTOM_DOMAIN = "objects.rma.cloudscale.ch/%s/" % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

# FIXME enabled for prod only and test it
AWS_STATIC_LOCATION = "static"
# STATICFILES_STORAGE = "project.storage.StaticStorage"
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_PUBLIC_MEDIA_LOCATION = ""

AWS_PRIVATE_MEDIA_LOCATION = ""
AWS_PRIVATE_MEDIA_BUCKET_NAME = "darg-private"
AWS_TEST_BUCKET_NAME = "darg-test"  # for dev and debug

S3_BUCKET = getattr(settings, "SYNC_S3_BUCKET", settings.AWS_STORAGE_BUCKET_NAME)
S3_DIR = getattr(settings, "SYNC_S3_DIR", "s3-source-dir/")
TARGET_DIR = getattr(settings, "SYNC_DROPBOX_DIR", "dropbox-dest-dir/")
TARGET_FILE_NAME = getattr(settings, "SYNC_TARGET_FILE_NAME", "backup.tar.gz")
