#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['AUDIOSERVICE_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['AUDIOSERVICE_MONGOALCHEMY_SERVER'] = ''
    os.environ['AUDIOSERVICE_MONGOALCHEMY_PORT'] = ''
    os.environ['AUDIOSERVICE_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.audioservice import audioservice
    from qube.src.services.audioserviceservice import audioserviceService
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, audioserviceServiceError


class TestaudioserviceService(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.audioserviceService = audioserviceService(context)
        self.audioservice_api_model = self.createTestModelData()
        self.audioservice_data = self.setupDatabaseRecords(self.audioservice_api_model)
        self.audioservice_someoneelses = \
            self.setupDatabaseRecords(self.audioservice_api_model)
        self.audioservice_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.audioservice_someoneelses.save()
        self.audioservice_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.audioservice_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.audioservice_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, audioservice_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            audioservice_data = audioservice(name='test_record')
            for key in audioservice_api_model:
                audioservice_data.__setattr__(key, audioservice_api_model[key])

            audioservice_data.description = 'my short description'
            audioservice_data.tenantId = "23432523452345"
            audioservice_data.orgId = "987656789765670"
            audioservice_data.createdBy = "1009009009988"
            audioservice_data.modifiedBy = "1009009009988"
            audioservice_data.createDate = str(int(time.time()))
            audioservice_data.modifiedDate = str(int(time.time()))
            audioservice_data.save()
            return audioservice_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_audioservice(self, *args, **kwargs):
        result = self.audioserviceService.save(self.audioservice_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.audioservice_api_model['name'])
        audioservice.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_audioservice(self, *args, **kwargs):
        self.audioservice_api_model['name'] = 'modified for put'
        id_to_find = str(self.audioservice_data.mongo_id)
        result = self.audioserviceService.update(
            self.audioservice_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.audioservice_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_audioservice_description(self, *args, **kwargs):
        self.audioservice_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.audioservice_data.mongo_id)
        result = self.audioserviceService.update(
            self.audioservice_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.audioservice_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_audioservice_item(self, *args, **kwargs):
        id_to_find = str(self.audioservice_data.mongo_id)
        result = self.audioserviceService.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_audioservice_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(audioserviceServiceError):
            self.audioserviceService.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_audioservice_list(self, *args, **kwargs):
        result_collection = self.audioserviceService.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.audioservice_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.audioservice_data.mongo_id)
        with self.assertRaises(audioserviceServiceError) as ex:
            self.audioserviceService.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.audioservice_data.mongo_id)
        self.audioserviceService.auth_context.is_system_user = True
        self.audioserviceService.delete(id_to_delete)
        with self.assertRaises(audioserviceServiceError) as ex:
            self.audioserviceService.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.audioserviceService.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.audioservice_someoneelses.mongo_id)
        with self.assertRaises(audioserviceServiceError):
            self.audioserviceService.delete(id_to_delete)
