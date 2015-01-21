# -*- coding: utf-8 -*-

import unittest
from geopdf import LGIDict, GeoCanvas
from StringIO import StringIO
from reportlab.pdfbase.pdfdoc import PDFString, PDFArray


class TestGeoPDF(unittest.TestCase):

    def test_lgidict_defaults(self):
        lgi_dict = LGIDict()

        self.assertTrue(isinstance(lgi_dict['Type'], PDFString))
        self.assertEqual(lgi_dict['Type'].s, 'LGIDict')
        self.assertTrue(isinstance(lgi_dict['Version'], PDFString))
        self.assertEqual(lgi_dict['Version'].s, '2.1')
        self.assertEqual(lgi_dict['Projection']['Type'], '/Projection')
        self.assertTrue(isinstance(lgi_dict['Projection']['Datum'], PDFString))
        self.assertEqual(lgi_dict['Projection']['Datum'].s, 'WE')

    def test_lgi_dict_validity(self):
        lgi_dict = LGIDict()
        self.assertFalse(lgi_dict.is_valid())

        lgi_dict['Registration'] = 'test'
        self.assertTrue(lgi_dict.is_valid())

        lgi_dict.dict.pop('Registration', None)
        self.assertFalse(lgi_dict.is_valid())

        lgi_dict['CTM'] = 'test'
        self.assertTrue(lgi_dict.is_valid())

    def test_pdf(self):
        canvas = GeoCanvas(StringIO())

        registration = PDFArray([
            PDFArray(map(PDFString, ['200', '400', '-180', '-90'])),
            PDFArray(map(PDFString, ['200', '600', '-180', '90'])),
            PDFArray(map(PDFString, ['400', '600', '180', '90'])),
            PDFArray(map(PDFString, ['400', '400', '180', '-90']))
        ])
        canvas.rect(200, 400, 200, 200, stroke=1)
        canvas.addGeo(Registration=registration)

        self.assertTrue('LGIDict' in canvas.getpdfdata())

        canvas.save()

if __name__ == '__main__':
    unittest.main()
