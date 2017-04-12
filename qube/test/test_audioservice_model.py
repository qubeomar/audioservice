#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class TestaudioserviceModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_audioservice_model(self):
        from qube.src.models.audioservice import audioservice
        audioservice_data = audioservice(name='testname')
        audioservice_data.tenantId = "23432523452345"
        audioservice_data.orgId = "987656789765670"
        audioservice_data.createdBy = "1009009009988"
        audioservice_data.modifiedBy = "1009009009988"
        audioservice_data.createDate = str(int(time.time()))
        audioservice_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            audioservice_data.save()
            self.assertIsNotNone(audioservice_data.mongo_id)
            audioservice_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
