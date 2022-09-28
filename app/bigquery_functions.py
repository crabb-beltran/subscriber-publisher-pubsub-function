from google.cloud import bigquery
import pandas as pd


class BigqueryFunctions:

    def __init__(self, query_text, bigquery_dataset, df):
        self.query_text = query_text
        self.bigquery_dataset = bigquery_dataset
        self.df = df
        self.df2 = pd.DataFrame()
        self._bigquery_client = bigquery.Client()


    def insert_table(self):
        self._job_config = bigquery.LoadJobConfig(schema=[
            bigquery.SchemaField("messages", "STRING"),
            bigquery.SchemaField("date_colombia", "TIMESTAMP"),
            bigquery.SchemaField("flag", "INTEGER"),
        ],
            write_disposition="WRITE_APPEND",
        )

        self._job = self._bigquery_client.load_table_from_dataframe(self.df, self.bigquery_dataset, job_config=self._job_config)
        self._job.result()


    def update_table(self):
        self._query_job = self._bigquery_client.query(self.query_text)
        self._query_job.result()
        print(f"DML query modified {self._query_job.num_dml_affected_rows} rows.")


    def select_table(self):
        self.df2 = self._bigquery_client.query(self.query_text).to_dataframe()
        return self.df2