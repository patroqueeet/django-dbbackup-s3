from unittest import TestCase, mock

from storage_sync.sync import SyncS3Backup


class SyncS3BackupTestCase(TestCase):
    @mock.patch("storage_sync.sync.tarfile")
    @mock.patch("storage_sync.sync.get_storage", mock.Mock())
    @mock.patch("storage_sync.sync.S3Boto3Storage")
    def test_compress(
        self,
        get_storage_mock,
        tarfile_mock,
    ):
        """compress resulting tar file"""
        get_storage_mock().listdir.side_effect = [(["subdir"], ["file"]), ([], [])]
        SyncS3Backup().sync()
        tarfile_mock.open.assert_called_with(
            fileobj=mock.ANY, mode="w:gz", name="backup.tar.gz"
        )
