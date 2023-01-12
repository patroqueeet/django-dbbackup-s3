import os
import tarfile

from dbbackup import utils as dbbackup_utils
from django.conf import settings
from django.utils import timezone
from storages.backends.dropbox import DropBoxStorage
from storages.backends.s3boto3 import S3Boto3Storage


class SyncS3Dropbox:
    def __init__(
        self,
        s3_dir_path: str = settings.SYNC_S3_DIR,
        dropbox_dir: str = settings.SYNC_DROPBOX_DIR,
        s3_bucket: str = settings.SYNC_S3_BUCKET,
        target_file_name: str = settings.SYNC_TARGET_FILE_NAME,
    ):
        self.s3_bucket = s3_bucket
        self.s3_dir_path = s3_dir_path
        self.dropbox_dir = dropbox_dir
        self.target_file_name = target_file_name

        self.s3_storage = S3Boto3Storage(bucket_name=self.s3_bucket)
        self.dropbox_storage = DropBoxStorage()

    def _get_recursive_files(self):
        path = self.s3_dir_path
        dirs = [path]
        while dirs:
            path = dirs.pop()
            sub_dirs, files = self.s3_storage.listdir(path)
            for media_filename in files:
                yield os.path.join(path, media_filename)
            dirs.extend([os.path.join(path, subdir) for subdir in sub_dirs])

    def _get_target_file_name(self) -> str:
        dt_str = timezone.now().strftime("%Y-%m-%d-%H-%M-%S")
        return f"{self.dropbox_dir}{dt_str}-{self.target_file_name}"

    def _create_tar_file_object(self):
        file_obj = dbbackup_utils.create_spooled_temporary_file()
        mode = "w:gz"
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

    def write_to_storage(self, file, path):
        self.s3_storage.write_file(file, path)

    def sync(self):
        tar_file = self.generate_backup()
        self.dropbox_storage.save(name=self._get_target_file_name(), content=tar_file)
