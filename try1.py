import rdflib

# graph:
graph = rdflib.Graph()

# text:
text = "Florence May Harding studied at a school in Sydney, and with Douglas Robert Dundas , but in effect had no formal training in either botany or art."
splitted = text.split(' ')

# stop words:
stop_words = ['at', 'in', 'no', 'and', 'but', 'or']

# single words checking:
words_checked = []
for word in splitted:
    if word[-1] in ['.', ',', ';', '-']:
        word = word[:-1]
    if word not in stop_words and len(word) > 1:
        words_checked += [word]
        resource = rdflib.URIRef(f'http://dbpedia.org/resource/{word}')
        person_ns = rdflib.URIRef('http://dbpedia.org/ontology/Person')
        object_ns = rdflib.URIRef('http://dbpedia.org/ontology/Place')
        organisation_ns = rdflib.URIRef('http://dbpedia.org/ontology/Organisation')

        type_ = graph.value(resource, rdflib.RDFS.label)

        graph.load(resource)

        for subject, predicate, object_ in graph:
            if subject == resource and object_ in [person_ns, object_ns, organisation_ns]:
                beginning = text.find(word)
                end = beginning + len(word)
                print(
                    f"{word} at {beginning},{end}: s={subject} of type {type(subject)}; p={predicate} of type {type(predicate)}; o={object_} of type {type(object_)}")

print('Checked:')
print(words_checked)
