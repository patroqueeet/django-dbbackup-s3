from unittest import TestCase, mock

from storage_sync.sync import SyncS3Backup


class SyncS3BackupTestCase(TestCase):
    @mock.patch("storage_sync.sync.tarfile")
    @mock.patch("storage_sync.sync.import_string", mock.Mock())
    @mock.patch("storage_sync.sync.S3Boto3Storage")
    def test_compress(
        self,
        import_string_mock,
        tarfile_mock,
    ):
        """compress resulting tar file"""
        import_string_mock().listdir.side_effect = [(["subdir"], ["file"]), ([], [])]
        SyncS3Backup().sync()
        tarfile_mock.open.assert_called_with(
            fileobj=mock.ANY, mode="w:gz", name="backup.tar.gz"
        )
