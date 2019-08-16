import gensim
from konlpy.tag import Kkma, Twitter, Mecab, Komoran, Okt
from konlpy.utils import pprint
import codes

model = gensim.models.Word2Vec.load('control/ko.bin')
okt = Okt()

def ckeck_sentence_similarity(sentence1, sentence2):
    sentence1_list = okt.nouns(sentence1)
    sentence2_list = okt.nouns(sentence2)

    if len(sentence1_list) == len(sentence2_list):
        return True
    else:
        return False

