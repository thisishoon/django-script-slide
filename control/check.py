import gensim
from konlpy.tag import Kkma, Twitter, Mecab, Komoran, Okt
from konlpy.utils import pprint
import codes
import math


# model = gensim.models.Word2Vec.load('control/ko.bin')
# okt = Okt()
def cmp_only_char(origin_sentence, speech_sentence):
    minimum_cnt = (len(origin_sentence) / 2.2) ** 1.95

    cnt = 0
    for i, i2 in enumerate(origin_sentence):
        for j, j2 in enumerate(speech_sentence):
            if i2 == j2:
                # print(str(i)+" "+str(j))
                cnt += i * 0.7 + 2
                break

                # 한바퀴 다돌고 판단
    print(minimum_cnt)
    print(cnt)
    print(str(cnt / minimum_cnt) + "%")
    if cnt > minimum_cnt:
        print("success")
        return 1
    else:
        print("fail")
        return 0


def edit_distance(origin_sentence, speech_sentence):
    len1 = len(origin_sentence)
    len2 = len(speech_sentence)
    arr = [[0 for x in range(len2)] for y in range(len1)]
    for i in range(0, len1):
        arr[i][0] = i;
    for i in range(0, len2):
        arr[0][i] = i;

    for i in range(1, len1):
        char1 = origin_sentence[i]
        for j in range(1, len2):
            char2 = speech_sentence[j]

            cost1 = 0
            if char1 != char2:
                cost1 = 2  # cost for substitution
            arr[i][j] = min(arr[i - 1][j] + 1, arr[i][j - 1] + 1, arr[i - 1][j - 1] + cost1)

    cost = arr[len1 - 1][len2 - 1]

    return cost


import math
import pprint

import math


def LCS(sentence, parse_sentence, speech_sentence):
    len1 = len(parse_sentence)
    len2 = len(speech_sentence)
    combo = -1
    start = -1
    end = -1
    start_point = -1
    end_point = -1

    end_list = []
    lcs = [[0 for i in range(len2 + 1)] for j in range(len1 + 1)]

    for i in range(2, len1 + 1):
        flag = 0
        for j in range(2, len2 + 1):
            if parse_sentence[i - 2] == speech_sentence[j - 2] and parse_sentence[i - 1] == speech_sentence[j - 1]:
                if start == -1:
                    start = i - 2
                if (i - 2) <= len2:
                    end_list.append(i - 1)

                lcs[i][j] = lcs[i - 1][j - 1] + math.log2(i + 1)
                if i - combo == 1:
                    lcs[i][j] += math.log10(i + 1)
                flag = 1
            else:
                lcs[i][j] = max(lcs[i][j - 1], lcs[i - 1][j])
        if flag == 1:
            combo = i

    sum = (math.log2(math.factorial(len1 + 1)) + math.log10(math.factorial(len1 + 1)) - math.log10(2 * 3) - math.log2(
        2))
    similarity = lcs[-1][-1] / sum
    end_max = (len1 * similarity) * 10 / 6
    end_list.sort(reverse=True)

    if end_max < 5:
        end_max = 5
    for i in end_list:
        if i <= end_max:
            end = i
            break

    k = 0
    if start != -1 and end != -1:
        for i in range(start, end + 1):
            for j in range(k, len(sentence)):
                if parse_sentence[i] == sentence[j]:
                    if k == 0:
                        start_point = j
                    end_point = j
                    k = j + 1
                    break
    #print(start, end)
    #print(start_point, end_point)

    cnt = 0
    for i in sentence[end_point:]:
        if i == ' ':
            cnt += 1
        if (cnt > 3):
            break

    return similarity, start_point, end_point, cnt



def split_word(sentence, n):
    split_sentence = sentence.split()
    n_sentence = ""
    n_parse_sentence = ""
    if len(split_sentence) < n:
        n = len(split_sentence)
    for i in range(0,n):
        n_parse_sentence+=split_sentence[i]
        n_sentence+= split_sentence[i]+" "
    return n_sentence, n_parse_sentence