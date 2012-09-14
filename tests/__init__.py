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
        self.assertIn(
            {u'lang': u'en_US.ISO8859-1', u'value': u'Hermitage'},
            db_doc['name'])
        self.assertIn(
            {u'lang': u'ru_RU.UTF-8', u'value': u'Эрмитаж'},
            db_doc['name'])

    def test002_load(self):
        doc = TestDocument.objects.first()
        self.assertIsInstance(doc.name, MultilingualString)
        self.assertDictEqual(
            doc.name.translations,
            {'en_US.ISO8859-1': 'Hermitage', 'ru_RU.UTF-8': u'Эрмитаж'})

    def test003_translate_doc(self):
        doc = TestDocument.objects.first()
        doc.translate('en')
        self.assertMultiLineEqual(doc.name, 'Hermitage')
        doc.translate('ru')
        self.assertMultiLineEqual(doc.name, u'Эрмитаж')
        doc.translate('en')
        self.assertMultiLineEqual(doc.name, 'Hermitage')

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
