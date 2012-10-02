# coding: u8
import unittest
from collections import OrderedDict

from i18n_string import MultilingualString, normalize_lang
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
                {u'lang': u'en_US', u'value': u'Hermitage'},
                {u'lang': u'ru_RU', u'value': u'Эрмитаж'}
            ],
            db_doc['name1'])

    def test002_load(self):
        doc = TestDocument(name1={'en': 'Hermitage', 'ru': u'Эрмитаж'})
        doc.save()
        del doc
        doc = TestDocument.objects.first()
        self.assertIsInstance(doc.name1, MultilingualString)
        self.assertDictEqual(
            doc.name1.translations,
            {'en_US': 'Hermitage', 'ru_RU': u'Эрмитаж'})

    def test003_translate_doc(self):
        doc = TestDocument(name1={'en': 'Hermitage', 'ru': u'Эрмитаж'})
        doc.save()
        del doc
        doc = TestDocument.objects.first()
        doc.translate('en')
        self.assertMultiLineEqual(doc.name1, 'Hermitage')
        doc.translate('ru')
        self.assertMultiLineEqual(doc.name1, u'Эрмитаж')
        doc.translate('en')
        self.assertMultiLineEqual(doc.name1, 'Hermitage')

    def test004_set_value(self):
        doc = TestDocument(name1={'en': 'Hermitage', 'ru': u'Эрмитаж'})
        doc.save()
        del doc
        doc = TestDocument.objects.first()
        doc.translate('en')
        doc.name1 = 'The Hermitage'
        doc.save()
        del doc
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual(
            [
                {u'lang': u'en_US', u'value': u'The Hermitage'},
                {u'lang': u'ru_RU', u'value': u'Эрмитаж'}
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

    def test007_initial_values_are_strings(self):
        doc = TestDocument()
        doc.translate('en')
        doc.name1 = 'Hermitage'
        doc.save()
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual(
            [
                {u'lang': u'en_US', u'value': u'Hermitage'},
            ],
            db_doc['name1'])

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
            name1__lang=normalize_lang('en'), name1__value='Hermitage').update(
            set__name1__S__value='The Hermitage')
        db_doc = TestDocument._get_collection().find_one()
        self.assertItemsEqual(
            [
                {u'lang': u'en_US', u'value': u'The Hermitage'},
                {u'lang': u'ru_RU', u'value': u'Эрмитаж'}
            ],
            db_doc['name1'])

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
