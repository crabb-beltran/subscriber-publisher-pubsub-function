
import base64
import os
import unittest

import pytest
from unittest.mock import MagicMock, Mock, patch
from google.cloud import pubsub_v1, bigquery, storage
import pandas as pd
from concurrent.futures import TimeoutError
import app.main as m
from test import mocks

# import mocks

class TestCase(unittest.TestCase):
    @unittest.mock.patch.object(pubsub_v1, 'PublisherClient')
    @unittest.mock.patch.object(pubsub_v1, 'SubscriberClient')
    @unittest.mock.patch.object(bigquery, 'Client')    
    @unittest.mock.patch.object(storage, 'Client')
    def test_gcs_event(self, storage_client, bigquery_client, pubsub_v1_subscriber_client, pubsub_v1_publisher_client):
        bigquery_client.return_value = mocks.BigQueryClientMock()
        pubsub_v1_subscriber_client.return_value = mocks.Pubsubv1SubscriberClientMock()
        pubsub_v1_publisher_client.return_value = mocks.Pubsubv1PublisherClientMock()
        storage_client.return_value = mocks.StorageClientMock()
        mock_context = Mock()
        mock_context.event_id = '617187464135194'
        mock_context.timestamp = '2019-07-15T22:09:03.761Z'
        mock_context.resource = {
            'name': 'projects/my-project/topics/my-topic',
            'service': 'pubsub.googleapis.com',
            'type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage',
        }
        name = 'test'
        data = {'data': base64.b64encode(name.encode())}
        status = m.main(data, mock_context)
        self.assertIsNotNone(status)

    @unittest.mock.patch.object(pubsub_v1, 'PublisherClient')
    @unittest.mock.patch.object(pubsub_v1, 'SubscriberClient')
    @unittest.mock.patch.object(bigquery, 'Client')    
    @unittest.mock.patch.object(storage, 'Client')
    def test_gcs_event_failed(self, storage_client, bigquery_client, pubsub_v1_subscriber_client, pubsub_v1_publisher_client):
        bigquery_client.return_value = mocks.BigQueryClientMock()
        pubsub_v1_subscriber_client.return_value = mocks.Pubsubv1SubscriberClientMock()
        pubsub_v1_publisher_client.return_value = mocks.Pubsubv2PublisherClientMock()
        storage_client.return_value = mocks.StorageClientMock()
        mock_context = Mock()
        mock_context.event_id = '617187464135194'
        mock_context.timestamp = '2019-07-15T22:09:03.761Z'
        mock_context.resource = {
            'name': 'projects/my-project/topics/my-topic',
            'service': 'pubsub.googleapis.com',
            'type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage',
        }
        name = 'test'
        data = {'data': base64.b64encode(name.encode())}
        status = m.main(data, mock_context)
        self.assertIsNotNone(status)
