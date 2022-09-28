from google.cloud import pubsub_v1
import os


class PubsubMessage:

    def __init__(self, project_id, topic_id, message):
        self.project_id = project_id
        self.topic_id = topic_id
        self.df2 = message
        self.status = ''


    def pubsub_publisher_event(self):
        self._publisher = pubsub_v1.PublisherClient()
        self._topic_path = self._publisher.topic_path(self.project_id, self.topic_id)

        try:
            for i in range(len(self.df2)):
                self._data = self.df2.loc[i, "messages"]
                self._data = self._data.encode('utf-8')
                self._future = self._publisher.publish(self._topic_path, self._data)
                print(f'Publised message id {self._future.result()}')

            self.status = True
        except Exception:
            print("The publication of the message in the topic failed")
            self.status = False

        return self.status