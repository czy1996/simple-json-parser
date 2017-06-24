from utils import log, ensure


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


def test_tokenizer():
    s1 = '''{
    "employees": [
    { "firstName":-12.34 , "lastName":null },
    { "firstName":true , "lastName":["Smith\\"", 123] }
    ]
    }'''
    log(s1)
    log(tokenizer(s1))


def test():
    test_tokenizer()


if __name__ == '__main__':
    test()
