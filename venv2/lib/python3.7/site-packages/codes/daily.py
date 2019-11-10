"""insert space between Chinese and English"""


# def is_chinese(uchar):
#     " 判断一个 unicode 是否是汉字"
#     if '\u4e00' <= uchar <= '\u9fff':
#         return True


# def is_number(uchar):
#     "判断一个 unicode 是否是数字"
#     if '\u0030' <= uchar <= '\u0039':
#         return True


# def is_alphabet(uchar):
#     "判断一个 unicode 是否是英文字母"
#     if ('\u0041' <= uchar <= '\u005a') or ('\u0061' <= uchar <= '\u007a'):
#         return True


# def is_other(uchar):
#     "判断是否非汉字，数字和英文字符"
#     if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
#         return True


def chinese_or_english(char):
    """判断汉字或字母"""
    if '\u4e00' <= char <= '\u9fff':
        # 汉字
        return 'c'
    elif '\u0041' <= char <= '\u005a' or '\u0061' <= char <= '\u007a':
        # 字母
        return 'e'
    elif '\u0030' <= char <= '\u0039':
        return 'n'
    else:
        return None


def insert_space(sense):
    """
    在句子中的字母和汉字中间插入空格。
    :param sense:str,句子
    :return:str,句子
    """
    sense = sense.replace(' ', '')
    format_list = []
    index_list = []
    sense_list = []
    for char in sense:
        status = chinese_or_english(char)
        format_list.append(status)
    for index, value in enumerate(format_list):
        if index == 0:
            continue
        elif value is None or format_list[index - 1] is None:
            continue
        elif value == format_list[index - 1]:
            continue
        else:
            index_list.append(index)
    index_list.reverse()
    for i in index_list:
        sense_list.append(sense[i:])
        sense = sense[:i]
    sense_list.append(sense)
    sense_list.reverse()
    all_sense = ' '.join(sense_list).strip()
    return all_sense


if __name__ == "__main__":
    from sys import argv

    try:
        WORDS = insert_space(argv[1])
    except IndexError:
        WORDS = 'lose args'
    print(insert_space(WORDS))
