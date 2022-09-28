from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from datetime import datetime
import os
import pandas as pd
import json

class Event_Arsg:

    def __init__(self):
        self.timeout = 5.0
        self.project_id = os.environ.get("PROJECT_ID")
        self.subscription_id = os.environ.get("SUBSCRIPTION_ID")
        self.data1 = []
        self.data2 = []
        self.df = pd.DataFrame()
        self.pubsub_subscriber_event()


    def pubsub_subscriber_event(self):
        self._subscriber = pubsub_v1.SubscriberClient()
        self._subscription_path = self._subscriber.subscription_path(self.project_id, self.subscription_id)

        self._streaming_pull_future = self._subscriber.subscribe(self._subscription_path, callback = self.callback)

        with self._subscriber:

            try:
                self._streaming_pull_future.result(timeout=self.timeout)

            except TimeoutError:
                self._streaming_pull_future.cancel()
                self._streaming_pull_future.result()

        if len(self.data2) != 0:
            self.add_dataframe()

    def callback(self, message: pubsub_v1.subscriber.message.Message) -> None:
        self.data1.append(f"{message.data!r}")
        message.ack()

        for _row in self.data1:
            _row1 = _row[2:-1]

            try:
                json.loads(_row1)
                self.data2.append(_row1)
            except ValueError:
                return False
            return True


    def add_dataframe(self):
        self.df = pd.DataFrame(self.data2)
        self.df = self.df.drop_duplicates()
        self.data2 = []
        self.pubsub_subscriber_event()


#def main(event, context):
def main():
    event_arsg = Event_Arsg()
    event_arsg.df.to_csv('File.csv')

if __name__ == "__main__":
    main()