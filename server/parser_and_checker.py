"""Parses the text and checks terms' existence in dbpedia graph."""
import os

from nltk.tag import StanfordNERTagger
import rdflib

from server import serializer

graph = rdflib.Graph()


def check_series(series):
    """ Checks the series in Dbpedia graph.

    :param series: Series extracted from parse function.
    :return: Table of dicts:
    {
        "serie": term,
        "subject": dbpedia subject,
        "predicate": dbpedia predicate,
        "type": dbpedia type,
    }
    """
    response = []

    person_ns = rdflib.URIRef('http://dbpedia.org/ontology/Person')
    object_ns = rdflib.URIRef('http://dbpedia.org/ontology/Place')
    organisation_ns = rdflib.URIRef('http://dbpedia.org/ontology/Organisation')

    for serie in series:

        # Polish signs handler
        replaced = ''
        for i in range(len(serie)):
            curr_temp = serializer.replacements.get(serie[i])
            if curr_temp:
                replaced += curr_temp
            else:
                replaced += serie[i]
        serie = replaced

        # Check resources:
        resource = rdflib.URIRef(f"http://dbpedia.org/resource/{serie}")

        graph.value(resource, rdflib.RDFS.label)
        graph.load(resource)

        for subject, predicate, object_ in graph:
            if subject == resource and object_ in [person_ns, object_ns, organisation_ns]:
                response += [
                    {
                        'serie': serie,
                        'subject': u''.join(subject).encode('utf-8'),
                        'predicate': u''.join(predicate).encode('utf-8'),
                        'type': u''.join(object_).encode('utf-8')
                    }
                ]
                break

    return response


def parse(string):
    """Main parsing function using Stanford NER Parser and little tweaks from the authors.

    :param string: Sentence to be parsed.
    :return: Table of dicts:
    {
        "serie": term,
        "subject": dbpedia subject,
        "predicate": dbpedia predicate,
        "type": dbpedia type,
        "begin": begin index,
        "end": end index,
    }
    """
    # Base project path (eg. 'D:\zti')
    base_path = 'D:\zti'

    # Set environment variables for Java Stanford NER Parser program
    os.environ[
        'CLASSPATH'] = base_path + '\stanford-ner-2018-10-16\stanford-ner.jar'  # path to stanford-ner.jar file
    os.environ[
        'STANFORD_MODELS'] = base_path + '\stanford-ner-2018-10-16\classifiers'  # path to classifiers
    os.environ['JAVAHOME'] = 'C:\Program Files (x86)\Common Files\Oracle\Java\javapath'  # path to folder containing Java

    st3 = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')

    # Split through spaces
    words = string.split(' ')

    # Remove newline sign from the end
    if words[-1:][0] in ['\n', '\r', '\n\r', '\r\n']:
        words = words[:-1]

    # Remove dotto from words
    for i in range(len(words)):
        words[i] = serializer.remove_signs(words[i])

    # Tag words
    tags3 = st3.tag(words)

    # Go through every word and add them to the table of words to check
    curr_term = ''
    terms = []
    for i in range(len(tags3)):

        # If word is qualified
        if tags3[i][1] != 'O':

            # If word is not first
            if i != 0 and len(curr_term) > 0:
                # If previous word was NOT of the same (NER detected) type,
                # add previous to terms and set curr_term as new
                if tags3[i - 1][1] != tags3[i][1]:
                    terms += [curr_term]
                    curr_term = tags3[i][0]

            # If curr_term is NOT empty add '_' to make space
            if len(curr_term) > 0:
                curr_term += '_'
            curr_term += tags3[i][0]

        # If word is not qualified
        else:
            # ...and curr_term is NOT empty add curr_term to terms and
            if len(curr_term) > 0:
                terms += [curr_term]
                curr_term = ''

    # If the term was at the end, save it too
    if len(curr_term) > 0:
        terms += [curr_term]

    print(terms)
    # Add necessary commas when US states are in
    for i in range(len(terms)):
        for state in serializer.us_states:
            comma_needed = terms[i].find(state[0])
            if comma_needed > 0:
                # print(f'comma needed in {terms[i]} at {comma_needed}')
                terms += [terms[i][:comma_needed - 1]]
                terms += [terms[i][comma_needed:]]
                terms[i] = terms[i][:comma_needed - 1] + ',_' + terms[i][comma_needed:]

    # Split when United States is in term
    for i in range(len(terms)):
        split_needed = terms[i].find('United_States')
        if split_needed > 0:
            # print(f'split needed in {terms[i]} at {split_needed}')

            if 'United_States' not in terms:
                terms += ['United_States']

            terms[i] = terms[i][:split_needed - 1]

    # Check in graph
    results = check_series(terms)

    for term in terms:
        begin = string.find(term.replace('_', ' '))
        end = begin + len(term)
        print(f'{begin}:{end} -- {string[begin:end]}')

        if len(results):
            for i in range(len(results)):
                if results[i]['serie'] == term:
                    results[i]['begin'] = begin
                    results[i]['end'] = end
                    break
                elif i+1 == len(results):
                    results += [{'serie': term,
                                 'begin': begin,
                                 'end': end,
                                 'subject': None,
                                 'predicate': None,
                                 'type': None
                                 }]
        else:
            results += [{'serie': term,
                         'begin': begin,
                         'end': end,
                         'subject': None,
                         'predicate': None,
                         'type': None
                         }]

    return results


if __name__ == "__main__":
    """Runs the OKE_Tests_txt.txt file parsing test."""
    # Read the file with sentences
    with open('./server/test_samples/OKE_Tests_txt.txt', encoding='utf-8') as fl:
        # Extract every line
        for line in fl:
            print(f'Parsing "{line[:-1]}"')
            parse(line)
