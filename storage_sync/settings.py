from django.conf import settings

S3_BUCKET = getattr(settings, "SYNC_S3_BUCKET", settings.AWS_STORAGE_BUCKET_NAME)
S3_DIR = getattr(settings, "SYNC_S3_DIR", "s3-source-dir/")
DROPBOX_DIR = getattr(settings, "SYNC_DROPBOX_DIR", "dropbox-dest-dir/")
TARGET_FILE_NAME = getattr(settings, "SYNC_TARGET_FILE_NAME", "backup.tar.gz")
