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


def extract_string(message):
    response = message.split("nif:isString")
    if len(response) >1:
        response = response[1].split("\"")
        if len(response) >1:
            response = response[1]
    return response


def remove_signs(word):
    if word[0] in dotto:
        word = word[1:]
    if word[-1:] in dotto:
        word = word[:-1]
    return word


def text_to_series(text):
    splitted = text.split(" ")

    serie = ''
    series = []

    second_serie = ''

    for wi in range(0, len(splitted)):
        if len(splitted[wi]) == 1:
            continue
        elif splitted[wi][0].isupper():
            splitted[wi] = remove_signs(splitted[wi])
            if serie == '':
                serie = splitted[wi]
            else:
                serie += '_' + splitted[wi]

                if splitted[wi - 1] in connectors:
                    second_serie = splitted[wi]
                elif second_serie != '':
                    second_serie += '_' + splitted[wi]
            continue
        elif splitted[wi] in connectors and serie != '':
            series += [serie]
            serie += '_' + splitted[wi]

            if second_serie != '':
                series += [second_serie]
                second_serie = ''
        else:
            splitted[wi] = remove_signs(splitted[wi])
            if serie != '':
                series += [serie]
                serie = ''
            if splitted[wi] not in stopwords:
                series += [splitted[wi]]

            if second_serie != '':
                series += [second_serie]
                second_serie = ''

    if serie != '':
        series += [serie]
    if second_serie != '':
        series += [second_serie]

    return series
