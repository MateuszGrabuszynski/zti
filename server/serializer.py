import re

# stopwords from nltk.corpus as on Jul 6 2018
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
             'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
             'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
             'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
             'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but',
             'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
             'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
             'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
             'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
             'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
             "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
             'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',
             "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
             "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
             "wouldn't"]
connectors = ['a', 'an', 'in', 'the', 'of', 'at', 'for', 'to']
dotto = ['.', ',', ':', ';', '-', '/', ')', '(', '\'', '\"', '+', '^']


def extract_address(data):
    """ Finds all <...>, chooses the last one and removes the unnecessary brackets

    :param data: Data sent by the client.
    :return: Just the extracted address from triangle brackets.
    """
    address = re.findall("\<.*\>", data)[-1][1:-1]
    return address


def extract_begin_end(data):
    """ Finds nif:beginIndex and nif:endIndex values.

    :param data: Data sent by the client.
    :return: Begin index and end index, -1 if error.
    """
    try:
        begin = data.split("nif:beginIndex")[1].split("\"")[1]
        end = data.split("nif:endIndex")[1].split("\"")[1]
        return int(begin), int(end)
    except IndexError:
        return -1, -1


def extract_string(data, begin, end):
    """ Extracts the main string from the message sent by the client and cuts it specifically.

    :param end: The end of the string.
    :param begin: The beginning of the string.
    :param data: Data sent by the client.
    :return: String part of the message.
    """
    try:
        return data.split("nif:isString")[1].split("\"")[1][begin:end]
    except IndexError:
        return -1


def remove_signs(word):
    """ Removes dots, commas etc. if first or last character in word

    :param word: Just a word from the sentence.
    :return: Word without dots and other signs if they are on the beginning or the end of it.
    """
    try:
        if word[0] in dotto:
            word = word[1:]
        if word[-1:] in dotto:
            word = word[:-1]
    # If empty string, does not break into pieces (just pass)
    except IndexError:
        pass
    return word


def text_to_series(text, search_begin, search_end):
    """ Splits text to series from search_begin to search_end index.

    :param text: Input text extracted from data sent by the client.
    :param search_begin: Index of the first sign, letter from which the search should begin.
    :param search_end: Index of the last sign, letter on which the search should end.
    :return: Array of sets as follows:
        {
            'serie': serie,
            'found': False,
            'begin': first_sign_of_the_serie,
            'end': last_sign_of_the_serie,
        }
    """
    splitted = text[search_begin:search_end].split(" ")

    serie = ''
    longer_serie = ''
    series = []

    for wi in range(0, len(splitted)):
        # Removes one letter words
        if len(splitted[wi]) == 1:
            continue
        # If the current word starts from uppercase letter
        elif splitted[wi][0].isupper():
            splitted[wi] = remove_signs(splitted[wi])
            # If the serie is empty, add current word to it
            if serie == '':
                serie = splitted[wi]
            # If the serie is not empty, add underscore and current word to it (basically next word)
            else:
                serie += '_' + splitted[wi]
                # If previous word was an connector, add it to longer_serie
                if splitted[wi - 1] in connectors:
                    longer_serie = splitted[wi]
                # If longer_serie is not empty, add the current word to longer_serie
                elif longer_serie != '':
                    longer_serie += '_' + splitted[wi]
            continue
        # If the current word is a connector and serie is not empty, add current serie to series
        # and underscore with current word to serie
        elif splitted[wi] in connectors and serie != '':
            serie_to_find = re.sub('_', ' ', serie)
            begin = search_begin + text.find(serie_to_find)
            series += [{
                'serie': serie,
                'found': False,
                'begin': begin,
                'end': begin + len(serie)
            }]
            serie += '_' + splitted[wi]

            # If longer_serie is not empty add longer_serie to series and make longer_serie empty
            if longer_serie != '':
                serie_to_find = re.sub('_', ' ', longer_serie)
                begin = search_begin + text.find(serie_to_find)
                series += [{'serie': longer_serie, 'found': False, 'begin': begin,
                            'end': begin + len(longer_serie)}]
                longer_serie = ''

        # Otherwise
        else:
            splitted[wi] = remove_signs(splitted[wi])
            # If serie is not empty, add serie to series and make it empty
            if serie != '':
                serie_to_find = re.sub('_', ' ', serie)
                begin = search_begin + text.find(serie_to_find)
                series += [
                    {'serie': serie, 'found': False, 'begin': begin, 'end': begin + len(serie)}]
                serie = ''
            # If current word not in stopwords add it to series
            # if splitted[wi] not in stopwords:
            #     series += [splitted[wi]]

            # If longer_serie is not empty, add longer_serie to series and make it empty
            if longer_serie != '':
                serie_to_find = re.sub('_', ' ', longer_serie)

                begin = search_begin + text.find(serie_to_find)
                series += [{'serie': longer_serie, 'found': False, 'begin': begin,
                            'end': begin + len(longer_serie)}]
                longer_serie = ''

    # Saves when the keyword is on the last position (last word in sentence)
    if serie != '':
        serie_to_find = re.sub('_', ' ', serie)
        begin = search_begin + text.find(serie_to_find)
        series += [{'serie': serie, 'found': False, 'begin': begin, 'end': begin + len(serie)}]
    if longer_serie != '':
        serie_to_find = re.sub('_', ' ', longer_serie)
        begin = search_begin + text.find(serie_to_find)
        series += [{'serie': longer_serie, 'found': False, 'begin': begin,
                    'end': begin + len(longer_serie)}]

    return series


def prepare_response(series, data, address):
    """ Prepares response for the client.

    :param series: Graphed series.
    :param data: Original data from the client.
    :param address: Address given in <> brackets by the client.
    :return: Response to be sent back to the client.
    """
    response = data + '\n'  # data is all data sent by user
    nochar_address = address.split('#char=')[0]  # from address take the part without #char=...
    # add every serie to response
    for serie in series:
        anchor_of = re.sub('_', ' ', serie['serie'])
        response += f"<{nochar_address}#char={serie['begin']},{serie['end']}>\n" \
                    f"        a                     nif:RFC5147String , nif:String ;\n" \
                    f"        nif:anchorOf          \"{anchor_of}\"@en ;\n" \
                    f"        nif:beginIndex        \"{serie['begin']}\"^^xsd:nonNegativeInteger ;\n" \
                    f"        nif:endIndex          \"{serie['end']}\"^^xsd:nonNegativeInteger ;\n" \
                    f"        nif:referenceContext  <{address}> ;\n"
        if serie['predicate']:
            response += f"        itsrdf:taIdentRef     dbpedia:{serie['serie']} .\n"
        else:
            response += f"        itsrdf:taIdentRef     <http://aksw.org/notInWiki/{serie['serie']}> .\n"
    return response[:-1]
