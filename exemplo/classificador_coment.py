import random
import nltk
import re
from nltk.corpus import floresta
from textblob import TextBlob
from unidecode import unidecode
from nltk.tokenize import RegexpTokenizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import SVC, LinearSVC, NuSVC

dic = []
word_features = []

def features(word, ofensas):

    cont = 0
    stemmed = aplicaStem(word)
    for ofensa in ofensas:
        if ofensa in stemmed:
            cont += 1

    tam = 0
    for palavra in word:
        tam += len(palavra)

    corretas = 0
    for w in word:
        if w in dic:
            corretas += 1

    features = {}


    features['quant_ofensivas'] = (cont)
    features['quant_palavras'] = (len(word))
    features['tam_medio_palavras'] = (tam / len(word))
    features['quant_carac'] = (tam)
    features['palavras_corretas'] = (corretas)

    return features

def dicionario():

    global dic

    for word in floresta.words():
        dic.append(unidecode(word.lower()))

def palavrasFreq(texto):

    global word_features
    word = []

    for t in texto:
        for x in t:
            if type(x) is list:
                word += x
    word = nltk.FreqDist(word)
    for t in word.most_common(500):
        for x in t:
            if type(x) is str:
                word_features.append(x)

def geraOfensas():

    ofensas = []
    for of in open('palavras_ofensivas.txt'):
        ofensas.append((aplicaStem(preProcessamento(of)))[0])

    return ofensas

def aplicaStem(texto):

    frasesStemming = []
    stemmer = nltk.stem.RSLPStemmer()

    for palavras in texto:
        frasesStemming.append(stemmer.stem(palavras))

    return frasesStemming

def deletaDoisOuMais(s):

    r = re.compile(r"(\w)\1{1,}")
    return "".join(r.split(s))

def preProcessamento(texto):

    aux = texto.lower()

    r = re.compile('[ha]{3,}')
    texto_l = "".join(r.split(aux))

    texto_lower = deletaDoisOuMais(texto_l)

    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(texto_lower)

    stopwordsnltk = nltk.corpus.stopwords.words('portuguese')

    final = []

    for palavra in text:
        if palavra not in stopwordsnltk:
            final.append(palavra)
    return final

def load_coment():
    ofen = open('ofensivo.txt', 'r', encoding='utf8')
    nao_ofen = open('nao_ofensivo.txt', 'r', encoding='utf8')
    of = ofen.read().split('\n')
    nof = nao_ofen.read().split('\n')
    return of, nof

if __name__ == '__main__':
    of, nof = load_coment()

    comentarios = (
        [(preProcessamento(coment), 'ofensivo') for coment in of] +
        [(preProcessamento(coment), 'nao_ofensivo') for coment in nof]
    )
    random.shuffle(comentarios)
    #print(comentarios)

    ofensas = geraOfensas()
    dicionario()
    palavrasFreq(comentarios)

    featuresets = [(features(n, ofensas), comentario) for (n, comentario) in comentarios]
    training_set, testing_set = featuresets[600:], featuresets[:100]

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Original Naive Bayes accuracy percent:", nltk.classify.accuracy(classifier, testing_set))
    print(classifier.show_most_informative_features(5))
