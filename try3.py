import rdflib

# stopwords from nltk.corpus as on Jul 6 2018
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
connectors = ['a', 'an', 'in', 'the', 'of', 'at', 'for', 'to']


def remove_signs(word):
    if word[-1:] in ['.', ',', ':', ';', '-', '/', ')', '(', '\'', '\"', '+', '^']:
        return word[:-1]
    else:
        return word


if __name__ == "__main__":
    # text = "Florence May Harding studied at a school in Sydney, and with Douglas Robert Dundas, but in effect had no formal training in either botany or art."
    text = "Barack Obama is not the current president of the United States of the Greatest America and that's weird"
    splitted = text.split(" ")

    serie = ''
    series = []

    others = []
    for wi in range(0, len(splitted)):
        if splitted[wi][0].isupper():
            splitted[wi] = remove_signs(splitted[wi])
            if serie == '':
                serie = splitted[wi]
            else:
                serie += '_' + splitted[wi]
            continue
        elif splitted[wi] in connectors and serie != '':
            series += [serie]
            serie += '_' + splitted[wi]
        else:
            splitted[wi] = remove_signs(splitted[wi])
            if serie != '':
                series += [serie]
                serie = ''
            if splitted[wi] not in stopwords:
                others += [splitted[wi]]

    print(f'series={series}\nothers={others}')
