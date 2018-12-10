import rdflib
import re

graph = rdflib.Graph()


def check_words(text, words):
    text = re.sub(' ', '_', text)

    response = []

    person_ns = rdflib.URIRef('http://dbpedia.org/ontology/Person')
    object_ns = rdflib.URIRef('http://dbpedia.org/ontology/Place')
    organisation_ns = rdflib.URIRef('http://dbpedia.org/ontology/Organisation')

    for word in words:
        resource = rdflib.URIRef(f'http://dbpedia.org/resource/{word}')

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
                        'subject': str(subject),
                        'predicate': str(predicate),
                        'type': str(object_)
                    }
                ]

    return response
