from utils import log, ensure
import json


def numbered_element(s):
    if '.' in s:
        return float(s)
    else:
        return int(s)


def formatted_element(s):
    # 转换为 python 内置类型
    # 数字转换为数字，null 转换为 None， bool 转换为 python 对应类型，字符串去掉双引号
    num = '-0123456789'
    if s[0] == '"':
        return s[1:-1]
    elif s == 'null':
        return None
    elif s == 'true':
        return True
    elif s == 'false':
        return False
    elif s[0] in num:
        return numbered_element(s)
    else:
        return s  # {} [] : ,


def formatted_tokens(l):
    return [formatted_element(s) for s in l]


def tokenizer(s):
    # A super lazy one
    # will change it later
    # actully, there is something wrong about escape
    s = s.lstrip(' \n').rstrip(' \n')
    s = s.replace('{', ' { ')
    s = s.replace('}', ' } ')
    s = s.replace('[', ' [ ')
    s = s.replace(']', ' ] ')
    s = s.replace(',', ' , ')
    s = s.replace(':', ' : ')
    l = s.split()
    log(l)
    return formatted_tokens(l)


def parse_obj(l):
    r = {}
    l.pop(0)
    while l[0] != '}':
        k, d, v = l.pop(0), l.pop(0), parser(l)
        r.update({
            k: v,
        })
        if l[0] == ',':
            l.pop(0)
    l.pop(0)
    return r


def parse_array(l):
    r = []
    l.pop(0)
    while l[0] != ']':
        ele = parser(l)  # ,
        if l[0] == ',':
            l.pop(0)
        r.append(ele)
    l.pop(0)
    return r


def parser(l):
    if l[0] == '{':
        # object
        return parse_obj(l)
    elif l[0] == '[':
        # array
        return parse_array(l)
    else:
        return l.pop(0)


def test_tokenizer():
    s1 = '''{
    "employees": [
    { "firstName":-12.34 , "lastName":null },
    { "firstName":true , "lastName":["Smith\\"", 123] }
    ]
    }'''
    log(s1)
    log(tokenizer(s1))


def test_parser():
    s1 = '''{
        "employees": [
        { "firstName":-12.34 , "lastName":null },
        { "firstName":true , "lastName":["Smith\\"", 123] }
        ]
        }'''
    l = tokenizer(s1)
    obj = parser(l)
    log(s1)
    log(obj, type(obj))
    log(json.loads(s1), 'json loads')


def test():
    # test_tokenizer()
    test_parser()

if __name__ == '__main__':
    test()
