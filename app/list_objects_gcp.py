from google.cloud import storage


class ListObjects:


    def __init__(self, bucket):
        self._bucket = bucket
        self._storage_client = storage.Client()
        self.list_objects()


    def list_objects(self):
        self._bucket = storage.Bucket(self._storage_client, self._bucket)
        self.all_blobs = list(self._storage_client.list_blobs(self._bucket))
        return self.all_blobs