import gensim
from konlpy.tag import Kkma, Twitter, Mecab, Komoran, Okt
from konlpy.utils import pprint
import codes


# model = gensim.models.Word2Vec.load('control/ko.bin')
# okt = Okt()

def cmp_only_char(origin_sentence1, speech_sentence2):
    minimum_cnt = len(origin_sentence1) / 2
    cnt = 0
    for i in origin_sentence1:
        for j in speech_sentence2:
            if i == j:
                cnt += 1
                continue

                # 한바퀴 다돌고 판단
    if cnt > minimum_cnt:
        print("success")
        return 1
    else:
        return 0


def edit_distance(origin_sentence1, speech_sentence2):
    return 0
