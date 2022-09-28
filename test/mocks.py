import pandas as pd
from concurrent.futures import TimeoutError
class JobMock():
    num_dml_affected_rows = 1
    def result(self, timeout=5):
        if timeout == 0:
            raise TimeoutError()
        return {
            'Nombre': 'Soy un mock'
        }

    def cancel(self):
        return True

    def close(self):
        return {
            'Nombre': 'Soy un mock'
        }
    def to_dataframe(self):
        data={'messages':['Este es un mensaje de prueba','Este es otro mensaje de prueba','Tercer Mensaje de prueba']}
        df = pd.DataFrame(data)
        return df

class MockEvent():
    data = ""
    def ack(self):
        return JobMock()
    
class BigQueryClientMock():
    def load_table_from_dataframe(self, argumento1, argumento2, job_config):
        return JobMock()

    def query(self, argumento1):
        return JobMock()


class Pubsubv1SubscriberClientMock():
    def __init__(self):
        self.stream = JobMock()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.stream.close()

    def subscription_path(self, argumento1, argumento2):
        return True

    def subscribe(self, argumento1, callback):
        return JobMock()


class Pubsubv1PublisherClientMock():
    def topic_path(self, project_id, topic_id):
        return JobMock()

    def publish(self, topic_path, data):
        return JobMock()

class Pubsubv2PublisherClientMock():
    def topic_path(self, project_id, topic_id):
        return JobMock()

    def publish(self, topic_path, data):
        if (data == b'Tercer Mensaje de prueba'):
            raise Exception('Falló')
        return JobMock()
class StorageClientMock():

    def __init__(self):
        self.stream = JobMock()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.stream.close()

    def bucket(self, argumento1):
        return JobMock()

    def get_bucket(self, argumento):
        return JobMock()

    def upload_from_filename(self, argumento1):
        return JobMock()
        
    def list_blobs(self, _bucket):
        return list([BucketObj(1),BucketObj(0)])

class BucketObj():

    def __init__(self, value) -> None:
        self.value = value

    value = 0 
    name = "Test.py"

    def download_as_bytes(self):
        return FileObj(value=self.value)

    def delete(self):
        return True

class FileObj():

    value = 0
    def __init__(self, value = 0) -> None:
        self.value = value

    def decode(self, decode):
        if (self.value == 1):
            return '{"insertId",{"insertId",{"insertId",{"insertId",{"insertId"'
        else:
            return ''