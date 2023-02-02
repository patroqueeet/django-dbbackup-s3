from unittest import TestCase, mock

from storage_sync.sync import SyncS3Dropbox


class SyncS3DropboxTestCase(TestCase):
    @mock.patch("storage_sync.sync.tarfile")
    @mock.patch("storage_sync.sync.DropBoxStorage")
    @mock.patch("storage_sync.sync.S3Boto3Storage")
    def test_compress(
        self, s3boto_mock, dropbox_mock, tarfile_mock,
    ):
        """ compress resulting tar file """
        s3boto_mock().listdir.side_effect = [(["subdir"], ["file"]), ([], [])]
        SyncS3Dropbox().sync()
        tarfile_mock.open.assert_called_with(
            fileobj=mock.ANY, mode="w:gz", name="backup.tar.gz"
        )
