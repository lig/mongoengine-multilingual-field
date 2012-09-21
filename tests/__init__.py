# coding: u8
import unittest
from collections import OrderedDict

from i18n_string import MultilingualString
from mongoengine.connection import connect, get_connection

from documents import TestDocument


class TestMultilingualStringField(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('test')
        cls.connection = get_connection()

    def setUp(self):
        TestDocument.objects.delete()
        doc = TestDocument(name={'en': 'Hermitage', 'ru': u'Эрмитаж'})
        doc.save()
        del doc

    def test001_save(self):
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual(
            [
                {u'lang': u'en_US', u'value': u'Hermitage'},
                {u'lang': u'ru_RU', u'value': u'Эрмитаж'}
            ],
            db_doc['name'])

    def test002_load(self):
        doc = TestDocument.objects.first()
        self.assertIsInstance(doc.name, MultilingualString)
        self.assertDictEqual(
            doc.name.translations,
            {'en_US': 'Hermitage', 'ru_RU': u'Эрмитаж'})

    def test003_translate_doc(self):
        doc = TestDocument.objects.first()
        doc.translate('en')
        self.assertMultiLineEqual(doc.name, 'Hermitage')
        doc.translate('ru')
        self.assertMultiLineEqual(doc.name, u'Эрмитаж')
        doc.translate('en')
        self.assertMultiLineEqual(doc.name, 'Hermitage')

    def test004_set_value(self):
        doc = TestDocument.objects.first()
        doc.translate('en')
        doc.name = 'The Hermitage'
        doc.save()
        del doc
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual(
            [
                {u'lang': u'en_US', u'value': u'The Hermitage'},
                {u'lang': u'ru_RU', u'value': u'Эрмитаж'}
            ],
            db_doc['name'])

    def test005_value_empty_dict(self):
        doc = TestDocument(name={})
        doc.save()

    def test006_value_none(self):
        doc = TestDocument(name=None)
        doc.save()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
