# coding: u8
import unittest
from collections import OrderedDict, MutableMapping

from mongoengine.connection import connect, get_connection

from documents import TestDocument


class TestMultilingualStringField(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('test')
        cls.connection = get_connection()

    def setUp(self):
        TestDocument.objects.delete()

    def test001_save(self):
        doc = TestDocument(name1={'en': 'Hermitage', 'ru': u'Эрмитаж'})
        doc.save()
        del doc
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual(
            [
                {u'lang': u'en', u'value': u'Hermitage'},
                {u'lang': u'ru', u'value': u'Эрмитаж'}
            ],
            db_doc['name1'])

    def test002_load(self):
        doc = TestDocument(name1={'en': 'Hermitage', 'ru': u'Эрмитаж'})
        doc.save()
        del doc
        doc = TestDocument.objects.first()
        self.assertIsInstance(doc.name1, MutableMapping)
        self.assertDictEqual(
            doc.name1,
            {'en': 'Hermitage', 'ru': u'Эрмитаж'})

    def test004_set_value(self):
        doc = TestDocument(name1={'en': 'Hermitage', 'ru': u'Эрмитаж'})
        doc.save()
        del doc
        doc = TestDocument.objects.first()
        doc.name1['en'] = 'The Hermitage'
        doc.save()
        del doc
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual(
            [
                {u'lang': u'en', u'value': u'The Hermitage'},
                {u'lang': u'ru', u'value': u'Эрмитаж'}
            ],
            db_doc['name1'])

    def test005_value_empty_dict(self):
        doc = TestDocument(name1={})
        doc.save()
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual([], db_doc['name1'])

    def test006_value_none(self):
        doc = TestDocument(name1=None)
        doc.save()
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual([], db_doc['name1'])

    def test008_find_doc_by_value(self):
        doc = TestDocument(name1={'en': 'Hermitage', 'ru': u'Эрмитаж'})
        doc.save()
        doc_id = doc.pk
        del doc
        doc = TestDocument.objects(name1__value='Hermitage').first()
        self.assertEqual(doc.pk, doc_id)

    def test009_perform_atomic_value_update(self):
        doc = TestDocument(name1={'en': 'Hermitage', 'ru': u'Эрмитаж'})
        doc.save()
        del doc
        TestDocument.objects(
            name1__lang='en', name1__value='Hermitage').update(
            set__name1__S__value='The Hermitage')
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual(
            [
                {u'lang': u'en', u'value': u'The Hermitage'},
                {u'lang': u'ru', u'value': u'Эрмитаж'}
            ],
            db_doc['name1'])

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
