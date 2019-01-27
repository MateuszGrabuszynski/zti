""" Extracting and serializing data from client. """

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
dotto = ['.', ',', ':', ';', '-', '/', ')', '(', '\'', '\"', '+', '^', '\n', '\r']
replacements = {'\u0104': '%C4%84', '\u0105': '%C4%85',  # a
                '\u0106': '%C4%86', '\u0107': '%C4%87',  # c
                '\u0118': '%C4%98', '\u0119': '%C4%99',  # ę
                '\u0143': '%C5%83', '\u0144': '%C5%84',  # ń
                '\u015a': '%C5%9A', '\u015b': '%C5%9B',  # si
                '\u0179': '%C5%B9', '\u017a': '%C5%BA',  # zi kreska
                '\u017b': '%C5%BB', '\u017c': '%C5%BC',  # rz kropka
                '\u00d3': '%C3%93', '\u00f3': '%C3%B3',  # o
                '\u0141': '%C5%81', '\u0142': '%C5%82'}  # l
us_states = [
    ('Alabama', 'AL'), ('Alaska', 'AK'), ('Arizona', 'AZ'), ('Arkansas', 'AR'), ('California', "CA"),
    ('Colorado', 'CO'), ('Connecticut', 'CT'), ('Delaware', 'DE'), ('Florida', 'FL'), ('Georgia', 'GA'),
    ('Hawaii', 'HI'), ('Idaho', 'ID'), ('Illinois', 'IL'), ('Indiana', 'IN'), ('Iowa', 'IA'),
    ('Kansas', 'KS'), ('Kentucky', 'KY'), ('Louisiana', 'LA'), ('Maine', 'ME'), ('Maryland', 'MD'),
    ('Massachusetts', 'MA'), ('Michigan', 'MI'), ('Minnesota', 'MN'), ('Mississippi', 'MS'), ('Missouri', 'MO'),
    ('Montana', 'MT'), ('Nebraska', 'NE'), ('Nevada', 'NV'), ('New_Hampshire', 'NH'), ('New_Jersey', 'NJ'),
    ('New_Mexico', 'NM'), ('New_York', 'NY'), ('North_Carolina', 'NC'), ('North_Dakota', 'ND'), ('Ohio', 'OH'),
    ('Oklahoma', 'OK'), ('Oregon', 'OR'), ('Pennsylvania', 'PA'), ('Rhode_Island', 'RI'), ('South_Carolina', 'SC'),
    ('South_Dakota', 'SD'), ('Tennessee', 'TN'), ('Texas', 'TX'), ('Utah', 'UT'), ('Vermont', 'VT'),
    ('Virginia', 'VA'), ('Washington', 'WA'), ('West_Virginia', 'WV'), ('Wisconsin', 'WI'), ('Wyoming', 'WY'),
]


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
        string = data.split("nif:isString")[1].split("\"")[1][begin:end]
        return string
    except IndexError:
        return -1


def remove_signs(word):
    """ Removes dots, commas etc. from beginnings and endings. 'Inc' gets dot at the end and is returned as 'Inc.'

    :param word: Just a word from the sentence.
    :return: Word without dots and other signs if they are on the beginning or the end of it.
    """
    # In the beginning:
    while True:
        try:
            if word[0] in dotto:
                word = word[1:]
            else:
                break
        except IndexError:
            pass

    # In the end:
    while True:
        try:
            if word[-1:] in dotto:
                word = word[:-1]
            else:
                break
        except IndexError:
            pass

    if word == 'Inc':
        word = 'Inc.'

    return word


def prepare_response(series, data, address):
    """ Prepares response for the client.

    :param series: Graphed series.
    :param data: Original data from the client.
    :param address: Address given in <> brackets by the client.
    :return: Response to be sent back to the client.
    """
    data = data[data.find('@prefix'):]
    response = data + '\n'  # data is all data sent by user (except headers)
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
