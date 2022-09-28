from list_objects_gcp import ListObjects
from bigquery_functions import BigqueryFunctions
from pubsub_publisher_message import PubsubMessage
from datetime import datetime
import pandas as pd
import os


class Arsg:

    def __init__(self):
        self.project_id = os.environ.get("PROJECT_ID")
        self.topic_id = os.environ.get("TOPIC_ID")
        self.dataset_id = os.environ.get("DATASET_ID")
        self.table_id = os.environ.get("TABLE_ID")
        self.bigquery_dataset = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        self.data1 = []
        self.bucket_in = os.environ.get("BUCKET_IN")
        self.query_text = ''
        self.starting_process()

    def starting_process(self):
        self._list_object = ListObjects(bucket = self.bucket_in)
        for self._blob in self._list_object.all_blobs:

            self._ciphertext = self._blob.download_as_bytes()
            self._ciphertext = self._ciphertext.decode('utf-8')
            if self._ciphertext:
                self._new_ciphertext = self._ciphertext.replace('{"insertId"','*{"insertId"' )
                self._new_ciphertext = self._new_ciphertext.split('*')

                for self._i in self._new_ciphertext:
                    if self._i != '':
                        self.data1.append(self._i)

        self.add_dataframe()

        self.insert_table = BigqueryFunctions(query_text = self.query_text, bigquery_dataset = self.bigquery_dataset, df = self.df)
        self.insert_table.insert_table()

        self.query_text = f"""
            UPDATE `{self.bigquery_dataset}` AS a
            SET  a.messages = remplazo_a.messagesa
                ,a.date_colombia = remplazo_a.date_colombiaa
                ,a.flag = 1
            FROM (
                SELECT
                    REPLACE(
                        REPLACE(
                            messages
                            ,SUBSTR(JSON_QUERY(messages, "$.receiveTimestamp"), 2 , 10)
                            ,SUBSTR(STRING(TIMESTAMP(DATETIME(TIMESTAMP(RIGHT(LEFT(JSON_QUERY(messages, "$.receiveTimestamp"),27), 26)),"America/Bogota"))),1,10)
                        )
                        ,SUBSTR(JSON_QUERY(messages, "$.receiveTimestamp"), 13 , 5)
                        ,SUBSTR(STRING(TIMESTAMP(DATETIME(TIMESTAMP(RIGHT(LEFT(JSON_QUERY(messages, "$.receiveTimestamp"),27), 26)),"America/Bogota"))),12,5)
                    ) AS messagesa
                    ,messages
                    ,TIMESTAMP(DATETIME(date_colombia,"America/Bogota")) as date_colombiaa
                FROM `{self.bigquery_dataset}`
                WHERE JSON_QUERY(messages, "$.receiveTimestamp") IS NOT NULL and flag = 0
                UNION ALL
                SELECT
                    messages AS messagesa
                    ,messages
                    ,TIMESTAMP(DATETIME(date_colombia,"America/Bogota")) as date_colombiaa
                FROM `{self.bigquery_dataset}`
                WHERE JSON_QUERY(messages, "$.receiveTimestamp") IS NULL and flag = 0
            )AS remplazo_a
            WHERE a.messages = remplazo_a.messages and a.flag = 0
        """
        self.update_table = BigqueryFunctions(query_text = self.query_text, bigquery_dataset = self.bigquery_dataset, df = self.df)
        self.update_table.update_table()

        self.query_text = f"""
                SELECT DISTINCT messages
                FROM `{self.bigquery_dataset}`
                WHERE flag = 1
            """
        self.select_table = BigqueryFunctions(query_text = self.query_text, bigquery_dataset = self.bigquery_dataset, df = self.df)
        self.select_table.select_table()

        if len(self.select_table.df2) != 0:
            self.pubsub_publisher = PubsubMessage(project_id = self.project_id, topic_id = self.topic_id, message = self.select_table.df2)
            self.pubsub_publisher.pubsub_publisher_event()

            if self.pubsub_publisher.status == True:
                self.query_text = f"""
                    UPDATE `{self.bigquery_dataset}` AS a
                    SET  a.flag = 2
                    WHERE a.flag = 1
                """
                self.update_table = BigqueryFunctions(query_text = self.query_text, bigquery_dataset = self.bigquery_dataset, df = self.df)
                self.update_table.update_table()

                self.delete_blob()


    def delete_blob(self):
        for self._blob in self._list_object.all_blobs:
            self._blob.delete()
            print(f"Blob {self._blob.name} deleted.")


    def add_dataframe(self):
        self.df = pd.DataFrame(self.data1, columns=['messages'])
        self._update_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.df['date_colombia'] = self._update_date
        self.df['flag'] = 0
        self.df = self.df.astype(dtype={"date_colombia": "datetime64[ns]"})
        self.df = self.df.drop_duplicates()
        return self.df

def main(event, context):
    args = Arsg()
    return args