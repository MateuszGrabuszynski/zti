import unittest

from server import serializer, graph_checker


class TestWithSample1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('../server/test_samples/sample1.txt') as file:
            cls.sample1 = file.read()

    def test_extract_address(self):
        self.assertEqual(serializer.extract_address(self.sample1), 'http://example.com/example-task1#char=0,146')

    def test_extract_begin_end(self):
        begin, end = serializer.extract_begin_end(self.sample1)
        self.assertEqual(begin, 0)
        self.assertEqual(end, 146)

    def test_extract_string_full_text(self):
        extracted = serializer.extract_string(self.sample1, 0, 146)
        self.assertEqual(extracted,
                         'Florence May Harding studied at a school in Sydney, and with Douglas Robert Dundas , but in effect had no formal training in either botany or art.')

    def test_extract_string_indexed(self):
        extracted = serializer.extract_string(self.sample1, 5, 15)
        self.assertEqual(extracted, 'nce May Ha')

    def test_remove_signs_same(self):
        self.assertEqual(serializer.remove_signs('word1'), 'word1')
        self.assertEqual(serializer.remove_signs(''), '')

    def test_remove_signs_ends(self):
        self.assertEqual(serializer.remove_signs('word.'), 'word')
        self.assertEqual(serializer.remove_signs('word2,'), 'word2')
        self.assertEqual(serializer.remove_signs(','), '')

    def test_remove_signs_begins(self):
        self.assertEqual(serializer.remove_signs(',word'), 'word')
        self.assertEqual(serializer.remove_signs('.Word'), 'Word')

    def test_text_to_series(self):
        extracted = serializer.extract_string(self.sample1, 0, 146)
        serialized = serializer.text_to_series(extracted, 0, 146)
        self.assertEqual(serialized, [{'serie': 'Florence_May_Harding', 'found': False, 'begin': 0, 'end': 20},
                                      {'serie': 'Sydney', 'found': False, 'begin': 44, 'end': 50},
                                      {'serie': 'Douglas_Robert_Dundas', 'found': False, 'begin': 61, 'end': 82}])

    def test_check_series(self):
        graphed = graph_checker.check_series([{'serie': 'Florence_May_Harding', 'found': False, 'begin': 0, 'end': 20},
                                              {'serie': 'Sydney', 'found': False, 'begin': 44, 'end': 50},
                                              {'serie': 'Douglas_Robert_Dundas', 'found': False, 'begin': 61,
                                               'end': 82}])
        self.assertEqual(graphed, [{'serie': 'Florence_May_Harding', 'begin': 0, 'end': 20,
                                    'subject': 'http://dbpedia.org/resource/Florence_May_Harding',
                                    'predicate': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                                    'type': 'http://dbpedia.org/ontology/Person'},
                                   {'serie': 'Sydney', 'begin': 44, 'end': 50,
                                    'subject': 'http://dbpedia.org/resource/Sydney',
                                    'predicate': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                                    'type': 'http://dbpedia.org/ontology/Place'},
                                   {'serie': 'Douglas_Robert_Dundas', 'begin': 61, 'end': 82, 'subject': None,
                                    'predicate': None, 'type': None}]
                         )

    def test_prepare_response(self):
        address = serializer.extract_address(self.sample1)
        graphed = graph_checker.check_series([{'serie': 'Florence_May_Harding', 'found': False, 'begin': 0, 'end': 20},
                                              {'serie': 'Sydney', 'found': False, 'begin': 44, 'end': 50},
                                              {'serie': 'Douglas_Robert_Dundas', 'found': False, 'begin': 61,
                                               'end': 82}])
        response = serializer.prepare_response(graphed, self.sample1, address)
        self.assertEqual(response, '''@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
@prefix dbpedia: <http://dbpedia.org/resource/> .
@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .

<http://example.com/example-task1#char=0,146>
        a                     nif:RFC5147String , nif:String , nif:Context ;
        nif:beginIndex        "0"^^xsd:nonNegativeInteger ;
        nif:endIndex          "146"^^xsd:nonNegativeInteger ;
        nif:isString          "Florence May Harding studied at a school in Sydney, and with Douglas Robert Dundas , but in effect had no formal training in either botany or art."@en .
<http://example.com/example-task1#char=0,20>
        a                     nif:RFC5147String , nif:String ;
        nif:anchorOf          "Florence May Harding"@en ;
        nif:beginIndex        "0"^^xsd:nonNegativeInteger ;
        nif:endIndex          "20"^^xsd:nonNegativeInteger ;
        nif:referenceContext  <http://example.com/example-task1#char=0,146> ;
        itsrdf:taIdentRef     dbpedia:Florence_May_Harding .
<http://example.com/example-task1#char=44,50>
        a                     nif:RFC5147String , nif:String ;
        nif:anchorOf          "Sydney"@en ;
        nif:beginIndex        "44"^^xsd:nonNegativeInteger ;
        nif:endIndex          "50"^^xsd:nonNegativeInteger ;
        nif:referenceContext  <http://example.com/example-task1#char=0,146> ;
        itsrdf:taIdentRef     dbpedia:Sydney .
<http://example.com/example-task1#char=61,82>
        a                     nif:RFC5147String , nif:String ;
        nif:anchorOf          "Douglas Robert Dundas"@en ;
        nif:beginIndex        "61"^^xsd:nonNegativeInteger ;
        nif:endIndex          "82"^^xsd:nonNegativeInteger ;
        nif:referenceContext  <http://example.com/example-task1#char=0,146> ;
        itsrdf:taIdentRef     <http://aksw.org/notInWiki/Douglas_Robert_Dundas> .''')
