from django.core.management.base import BaseCommand

from storage_sync import settings as sync_settings
from storage_sync.sync import SyncS3Backup


class Command(BaseCommand):
    help = "Create backup of a directory in S3 and backup to target storage"

    def add_arguments(self, parser):
        parser.add_argument(
            "--s3_dir",
            help="Path to directory in S3. Must ends with a '/'",
            type=str,
            default=sync_settings.S3_DIR,
        )
        parser.add_argument(
            "--target_dir",
            help="Path to directory in target storage. Must ends with a '/'",
            type=str,
            default=sync_settings.TARGET_DIR,
        )
        parser.add_argument(
            "--s3_bucket",
            help="S3 bucket name",
            type=str,
            default=sync_settings.S3_BUCKET,
        )
        parser.add_argument(
            "--target_file_name",
            help="Name of the file to be created in backup storage",
            type=str,
            default=sync_settings.TARGET_FILE_NAME,
        )
        parser.add_argument(
            "-z",
            "--compress",
            help="Compress the archive",
            action="store_true",
            default=False,
        ),

    def handle(self, *args, **options):
        sync_obj = SyncS3Backup(
            s3_dir=options["s3_dir"],
            target_dir=options["target_dir"],
            s3_bucket=options["s3_bucket"],
            target_file_name=options["target_file_name"],
            compress=options["compress"],
        )
        sync_obj.sync()
        self.stdout.write(
            self.style.SUCCESS("Successfully uploaded backup to backup storage")
        )
