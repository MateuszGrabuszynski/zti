import rdflib
from re import sub

graph = rdflib.Graph()


def check_words(text, words):
    text = sub(' ', '_', text)

    response = []

    for word in words:
        resource = rdflib.URIRef(f'http://dbpedia.org/resource/{word}')
        person_ns = rdflib.URIRef('http://dbpedia.org/ontology/Person')
        object_ns = rdflib.URIRef('http://dbpedia.org/ontology/Place')
        organisation_ns = rdflib.URIRef('http://dbpedia.org/ontology/Organisation')

        graph.value(resource, rdflib.RDFS.label)
        graph.load(resource)

        for subject, predicate, object_ in graph:
            if subject == resource and object_ in [person_ns, object_ns, organisation_ns]:
                begin = text.find(word)
                end = begin + len(word)
                response += [
                    {
                        'word': word,
                        'begin': begin,
                        'end': end,
                        'subject': subject,
                        'predicate': predicate,
                        'type': object_
                    }
                ]

    return response
