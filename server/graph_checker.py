import rdflib

graph = rdflib.Graph()


def check_series(series):
    response = []

    person_ns = rdflib.URIRef('http://dbpedia.org/ontology/Person')
    object_ns = rdflib.URIRef('http://dbpedia.org/ontology/Place')
    organisation_ns = rdflib.URIRef('http://dbpedia.org/ontology/Organisation')

    for serie in series:
        resource = rdflib.URIRef(f"http://dbpedia.org/resource/{serie['serie']}")

        graph.value(resource, rdflib.RDFS.label)
        graph.load(resource)

        for subject, predicate, object_ in graph:
            if subject == resource and object_ in [person_ns, object_ns, organisation_ns]:
                serie['found'] = True
                response += [
                    {
                        'serie': serie['serie'],
                        'begin': serie['begin'],
                        'end': serie['end'],
                        'subject': str(subject),
                        'predicate': str(predicate),
                        'type': str(object_)
                    }
                ]
                break

        # Current serie was not found in graph
        if not serie['found']:
            response += [
                {
                    'serie': serie['serie'],
                    'begin': serie['begin'],
                    'end': serie['end'],
                    'subject': None,
                    'predicate': None,
                    'type': None
                }
            ]

    return response
