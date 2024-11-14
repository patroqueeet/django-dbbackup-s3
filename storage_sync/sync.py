import logging
import os
import tarfile

from dbbackup import utils as dbbackup_utils
from dbbackup.storage import get_storage
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage

from storage_sync import settings as sync_settings

logger = logging.getLogger(__name__)


class SyncS3Backup:
    def __init__(
        self,
        s3_dir: str = sync_settings.S3_DIR,
        target_dir: str = sync_settings.TARGET_DIR,
        s3_bucket: str = sync_settings.S3_BUCKET,
        target_file_name: str = sync_settings.TARGET_FILE_NAME,
        compress: bool = True,
        filename=None,
        servername=None,
        content_type=None,
    ):
        self.s3_bucket = s3_bucket
        self.s3_dir = s3_dir
        self.target_dir = target_dir
        self.target_file_name = target_file_name
        self.compress = compress
        self.filename = filename
        self.servername = servername
        self.content_type = content_type

        self.s3_storage = S3Boto3Storage(bucket_name=self.s3_bucket)
        self.target_storage = get_storage().storage  # use nested storage

    def _get_recursive_files(self):
        path = self.s3_dir
        dirs = [path]
        while dirs:
            path = dirs.pop()
            sub_dirs, files = self.s3_storage.listdir(path)
            for media_filename in files:
                yield os.path.join(path, media_filename)
            dirs.extend([os.path.join(path, subdir) for subdir in sub_dirs])

    def _get_target_file_name(self) -> str:
        if self.filename:
            filename = self.filename
        else:
            extension = f"tar{'.gz' if self.compress else ''}"
            filename = dbbackup_utils.filename_generate(
                extension, servername=self.servername, content_type=self.content_type
            )
        return os.path.join(self.target_dir, filename)

    def _create_tar_file_object(self):
        file_obj = dbbackup_utils.create_spooled_temporary_file()
        mode = "w:gz" if self.compress else "w"
        tar_file = tarfile.open(name=self.target_file_name, fileobj=file_obj, mode=mode)
        for media_filename in self._get_recursive_files():
            tarinfo = tarfile.TarInfo(media_filename)
            media_file = self.s3_storage.open(media_filename)
            tarinfo.size = len(media_file)
            tar_file.addfile(tarinfo, media_file)
        # Close the TAR for writing
        tar_file.close()
        return file_obj

    def generate_backup(self):
        return self._create_tar_file_object()

    def write_to_storage(self, file_obj):
        self.target_storage.save(name=self._get_target_file_name(), content=file_obj)

    def sync(self):
        start = timezone.now()
        logger.info("Generating backup file")
        tar_file = self.generate_backup()
        logger.info("Writing backup file to storage")
        self.write_to_storage(tar_file)
        duration = timezone.now() - start
        logger.info("Backup file written to storage %s", duration)
