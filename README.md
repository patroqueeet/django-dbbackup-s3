# django-dbbackup-s3

Extend django-dbbackup to backup s3 data to DropBox

# Dependencies

- Django >=3.2, <4.0

## Installation and configuration

1. Create a new virtualenv and activate it
2. Install the packages - `pip install -r requirements.txt -U` and add `storage_sync` to INSTALLED_APPS in Django settings.
3. Make sure you have set the settings variables for `django-storage` packages
    1. `AWS_ACCESS_KEY_ID`
    2. `AWS_SECRET_ACCESS_KEY`
    3. `AWS_STORAGE_BUCKET_NAME`
    4. `AWS_S3_REGION_NAME`
    5. `DROPBOX_OAUTH2_TOKEN`
    6. `DROPBOX_OAUTH2_REFRESH_TOKEN`
    7. `DROPBOX_APP_KEY`
    8. `DROPBOX_APP_SECRET`
4. Set the values for the following variables in `settings.py`
    1. `SYNC_S3_BUCKET` - The name of the bucket to sync (default: `settings.AWS_STORAGE_BUCKET_NAME`)
    2. `SYNC_S3_DIR` - The directory in the bucket to sync (default: `s3-source-dir/`)
    3. `SYNC_DROPBOX_DIR` - The directory in the dropbox the backup to be uploaded (default: `dropbox-dest-dir/`)
    4. `SYNC_TARGET_FILE_NAME` - The custom name of the file to be uploaded (default: `backup.tar.gz`)
5. Run the management command - `python manage.py s3backup` (by default the management command will use the values defined
   in the `settings.py`. But, it can be overridden by passing commandline args)
    1. Run `python manage.py s3backup --help` to see all available options (incl. Compression of backup)

## Run tests with docker

```
docker run -it --rm -v "$(pwd):/app" python:3.7 bash -c "cd /app; pip install -e .[tests]; pytest"
```
