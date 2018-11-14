import rdflib

# text:
text = "Florence May Harding studied at a school in Sydney, and with Douglas Robert Dundas , but in effect had no formal training in either botany or art."
# text="Bill Gates founded Microsoft in USA."


def split_every(sentence, number_of_words, delimeter):
    # if number_of_words == 1:
    #     splitted = sentence.split(delimeter)
    #     cleaned = []
    #     for word in splitted:
    #         if word[-1] in ['.', ',', '-', ';']:
    #             cleaned += word[:-1]
    #     return cleaned
    # else:
    sentence_pos = temp_pos = 0
    phrases = []
    while sentence_pos != -1:
        for _ in range(number_of_words):
            temp_pos += sentence[temp_pos:].find(delimeter)
        phrases += [sentence[sentence_pos:sentence_pos+temp_pos-1]]
        temp_pos = 0
        sentence_pos += sentence[sentence_pos:].find(delimeter)+1  # move sentence_pos to first delimeter
    return phrases


if __name__ == "__main__":
    split_every('Ala ma kotka w kropki bordo', 1, ' ')
#
#
# # graph:
# graph = rdflib.Graph()
#
# # stop words:
# stop_words = ['at', 'in', 'no', 'and', 'but', 'or']
#
# # single words checking:
# words_checked = []
# for word in splitted:
#     if word[-1] in ['.', ',', ';', '-']:
#         word = word[:-1]
#     if word not in stop_words and len(word) > 1:
#         words_checked += [word]
#         resource = rdflib.URIRef(f'http://dbpedia.org/resource/{word}')
#         person_ns = rdflib.URIRef('http://dbpedia.org/ontology/Person')
#         object_ns = rdflib.URIRef('http://dbpedia.org/ontology/Place')
#         organisation_ns = rdflib.URIRef('http://dbpedia.org/ontology/Organisation')
#
#         type_ = graph.value(resource, rdflib.RDFS.label)
#
#         graph.load(resource)
#
#         for subject, predicate, object_ in graph:
#             if subject == resource and object_ in [person_ns, object_ns, organisation_ns]:
#                 beginning = text.find(word)
#                 end = beginning + len(word)
#                 print(
#                     f"{word} at {beginning},{end}: s={subject} of type {type(subject)}; p={predicate} of type {type(predicate)}; o={object_} of type {type(object_)}")
#
# print('Checked:')
# print(words_checked)
#
# print('Double words:')
#
# doublewords = list(map(' '.join, zip(words_checked[:-1], words_checked[1:])))
#
# # double words checking:
# doublewords_checked = []
# for word in doublewords:
#     # if word in mystring:
#     if word not in stop_words:
#         dbword = word.replace(" ", "_")
#         doublewords_checked += [dbword]
#         resource = rdflib.URIRef(f'http://dbpedia.org/resource/{dbword}')
#         person_ns = rdflib.URIRef('http://dbpedia.org/ontology/Person')
#         object_ns = rdflib.URIRef('http://dbpedia.org/ontology/Place')
#         organisation_ns = rdflib.URIRef('http://dbpedia.org/ontology/Organisation')
#
#     type_ = graph.value(resource, rdflib.RDFS.label)
#
#     graph.load(resource)
#
#     for subject, predicate, object_ in graph:
#         if subject == resource and object_ in [person_ns, object_ns, organisation_ns]:
#             beginning = text.find(dbword)
#             end = beginning + len(dbword)
#             print(
#                 f"{dbword} at {beginning},{end}: s={subject} of type {type(subject)}; p={predicate} of type {type(predicate)}; o={object_} of type {type(object_)}")
#
# print('Checked:')
# print(doublewords_checked)
#
# doublewords = list(map(' '.join, zip(words_checked[:-1], words_checked[1:])))
#
# # double words checking:
# doublewords_checked = []
# for word in doublewords:
#     # if word in mystring:
#     if word not in stop_words:
#         dbword = word.replace(" ", "_")
#         doublewords_checked += [dbword]
#         resource = rdflib.URIRef(f'http://dbpedia.org/resource/{dbword}')
#         person_ns = rdflib.URIRef('http://dbpedia.org/ontology/Person')
#         object_ns = rdflib.URIRef('http://dbpedia.org/ontology/Place')
#         organisation_ns = rdflib.URIRef('http://dbpedia.org/ontology/Organisation')
#
#     type_ = graph.value(resource, rdflib.RDFS.label)
#
#     graph.load(resource)
#
#     for subject, predicate, object_ in graph:
#         if subject == resource and object_ in [person_ns, object_ns, organisation_ns]:
#             beginning = text.find(dbword)
#             end = beginning + len(dbword)
#             print(
#                 f"{dbword} at {beginning},{end}: s={subject} of type {type(subject)}; p={predicate} of type {type(predicate)}; o={object_} of type {type(object_)}")
#
# print('Checked:')
# print(doublewords_checked)
#
# print('Revers Words:')
# reverseWords_checked = []
# reverseWords = " "
#
# for word in doublewords:
#     zawurodo = reverseWords.join(word.split()[::-1])
#
#     if word not in stop_words:
#         zawurodo = zawurodo.replace(" ", "_")
#         reverseWords_checked += [zawurodo]
#         resource = rdflib.URIRef(f'http://dbpedia.org/resource/{zawurodo}')
#         person_ns = rdflib.URIRef('http://dbpedia.org/ontology/Person')
#         object_ns = rdflib.URIRef('http://dbpedia.org/ontology/Place')
#         organisation_ns = rdflib.URIRef('http://dbpedia.org/ontology/Organisation')
#
#     type_ = graph.value(resource, rdflib.RDFS.label)
#
#     graph.load(resource)
#
#     for subject, predicate, object_ in graph:
#         if subject == resource and object_ in [person_ns, object_ns, organisation_ns]:
#             beginning = text.find(zawurodo)
#             end = beginning + len(zawurodo)
#             print(
#                 f"{zawurodo} at {beginning},{end}: s={subject} of type {type(subject)}; p={predicate} of type {type(predicate)}; o={object_} of type {type(object_)}")
#
# print('Checked:')
# print(reverseWords_checked)
