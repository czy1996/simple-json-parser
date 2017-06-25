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
        return s.rstrip(' ')[1:-1]  # 去除补齐的空格
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


# def tokenizer(s):
#     # A super lazy one
#     # will change it later
#     # actully, there is something wrong about escape
#     s = s.lstrip(' \n').rstrip(' \n')
#     s = s.replace('{', ' { ')
#     s = s.replace('}', ' } ')
#     s = s.replace('[', ' [ ')
#     s = s.replace(']', ' ] ')
#     s = s.replace(',', ' , ')
#     s = s.replace(':', ' : ')
#     l = s.split()
#     log(l)
#     return formatted_tokens(l)
def escaped_char(s):
    """
    | \"
     | \\
     | \/
     | \b
     | \f
     | \n
     | \r
     | \t
     |  four-hex-digits
    """
    escape = {
        '\\"': '"',
        '\\\\': '\\',
        '\\/': '/',
        '\\b': '\b',
        '\\f': '\f',
        '\\n': '\n',
        '\\r': '\r',
        '\\t': '\t',
        # '\\u': '\u',
    }
    # log(escape.get(s), s, '')
    return escape.get(s) + ' '  # 处理转义字符后字符串长度 - 1，外层函数需要该长度用来跳过处理的字符串


def string_element(s):
    r = '"'
    ec = False
    ecs = 0
    for i, e in enumerate(s[1:]):
        if ec:
            ec = False
        elif e == '\\':
            ec = True
            ecs += 1
            r += escaped_char(s[i + 1:i + 3])[:-1]  # 去除空格
        elif e == '"':
            r += e
            break
        else:
            r += e
    return r + ' ' * ecs  # 空格移到最右


def common_element(s):
    end_tokens = ']}:,'
    if s[0] == '"':
        return string_element(s)
    for i, e in enumerate(s):
        if e in end_tokens:
            return s[:i].lstrip(' \n').rstrip(' \n')


def tokenizer(s):
    blank_tokens = '\n '
    tokens = '{}[],:'
    l = []
    count = 0
    for i, e in enumerate(s):
        if count > 0:
            count -= 1
            continue
        elif e in blank_tokens:
            continue
        elif e in tokens:
            l.append(e)
        else:
            ele = common_element(s[i:])
            count = len(ele) - 1
            token = formatted_element(ele)
            l.append(token)
    return l


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


def tree(s):
    l = tokenizer(s)
    return parser(l)


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
    log(obj, 'mine')
    log(json.loads(s1), 'json loads')
    log('cmp', obj == json.loads(s1))

    s2 = '''{
       "achievement" : [ "ach1", "ach2", "ach3" ],
       "age" : 23,
       "name" : "Tsybius",
       "partner" : {
          "partner_age" : 21,
          "partner_name" : "Galatea",
          "partner_sex_is_male" : false
       },
       "sex_is_male" : true
    }'''
    log(parser(tokenizer(s2)), 'mine')
    log(json.loads(s2), 'json loads')


def test_tree():
    slist = []
    s1 = '''{
    "employees": [
    { "firstName":-12.34 , "lastName":null },
    { "firstName":true , "lastName":["Smith\\"", 123] }
    ]
    }'''
    s2 = '''{
       "achievement" : [ "ach1", "ach2", "ach3" ],
       "age" : 23,
       "name" : "Tsybius",
       "partner" : {
          "partner_age" : 21,
          "partner_name" : "Galatea",
          "partner_sex_is_male" : false
       },
       "sex_is_male" : true
    }'''
    s3 = """[
  {
    "_id": "594e5c7e8db3214973779d1c",
    "index": 0,
    "guid": "e4f0759e-0eac-46ee-a6dd-0fa2020abe2b",
    "isActive": true,
    "balance": "$3,172.66",
    "picture": "http://placehold.it/32x32",
    "age": 39,
    "eyeColor": "green",
    "name": "Tameka Barrett",
    "gender": "female",
    "company": "EVENTAGE",
    "email": "tamekabarrett@eventage.com",
    "phone": "+1 (801) 584-2649",
    "address": "713 Ocean Court, Chestnut, New Hampshire, 7649",
    "about": "Minim deserunt anim dolor nostrud. Sunt cupidatat sit veniam est amet nisi irure est consectetur laboris aute ea laboris. Velit sunt nulla nostrud duis nisi eiusmod.\\r\\n",
    "registered": "2015-12-23T08:24:36 -08:00",
    "latitude": -72.514353,
    "longitude": -63.260597,
    "tags": [
      "consectetur",
      "irure",
      "eu",
      "labore",
      "ipsum",
      "occaecat",
      "cupidatat"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Beasley Clay"
      },
      {
        "id": 1,
        "name": "Gretchen Randolph"
      },
      {
        "id": 2,
        "name": "Elva Osborn"
      }
    ],
    "greeting": "Hello, Tameka Barrett! You have 7 unread messages.",
    "favoriteFruit": "apple"
  },
  {
    "_id": "594e5c7e5314b1d6fa5b9e9c",
    "index": 1,
    "guid": "ed2edb17-0fb5-4df3-8538-3eb6dcca2d68",
    "isActive": false,
    "balance": "$2,076.04",
    "picture": "http://placehold.it/32x32",
    "age": 40,
    "eyeColor": "brown",
    "name": "Oneal Duncan",
    "gender": "male",
    "company": "PLASTO",
    "email": "onealduncan@plasto.com",
    "phone": "+1 (988) 533-2530",
    "address": "263 Union Avenue, Wawona, New Mexico, 321",
    "about": "Proident tempor eu pariatur minim Lorem. Consectetur fugiat veniam et adipisicing ex enim incididunt mollit occaecat nostrud deserunt minim magna. Labore anim dolor sunt veniam. Est eu reprehenderit ut est aliqua eiusmod duis consequat amet fugiat. Proident excepteur laboris aliqua ex eu dolor officia duis exercitation ad proident sint id eu.\\r\\n",
    "registered": "2017-05-18T10:13:29 -08:00",
    "latitude": -2.838377,
    "longitude": -101.395343,
    "tags": [
      "dolore",
      "magna",
      "veniam",
      "aliquip",
      "dolor",
      "ad",
      "amet"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Brock Compton"
      },
      {
        "id": 1,
        "name": "Wright Cooke"
      },
      {
        "id": 2,
        "name": "Burnett Thompson"
      }
    ],
    "greeting": "Hello, Oneal Duncan! You have 2 unread messages.",
    "favoriteFruit": "apple"
  },
  {
    "_id": "594e5c7e2ea73f15f2f1bf1d",
    "index": 2,
    "guid": "7f76e8bb-e1bf-45bb-b0cf-082245c42e0f",
    "isActive": false,
    "balance": "$1459.86",
    "picture": "http://placehold.it/32x32",
    "age": 37,
    "eyeColor": "brown",
    "name": "Murray Juarez",
    "gender": "male",
    "company": "FURNITECH",
    "email": "murrayjuarez@furnitech.com",
    "phone": "+1 (931) 483-2554",
    "address": "868 Forbell Street, Nutrioso, South Dakota, 7391",
    "about": "Non sint magna id reprehenderit elit eiusmod esse adipisicing cillum sunt excepteur excepteur voluptate. Id laborum quis eiusmod sint id incididunt eu occaecat sit voluptate quis. Quis aliquip excepteur minim deserunt aliquip occaecat aliquip irure culpa sunt. Ad laboris sunt esse duis dolore nisi ipsum. Cillum ad nulla magna labore eu nulla in. Veniam sunt eiusmod culpa deserunt id.\\r\\n",
    "registered": "2014-08-06T05:29:12 -08:00",
    "latitude": 60.830669,
    "longitude": -103.817266,
    "tags": [
      "excepteur",
      "eiusmod",
      "dolor",
      "ad",
      "amet",
      "incididunt",
      "nisi"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Shepherd Gaines"
      },
      {
        "id": 1,
        "name": "Stevens Jimenez"
      },
      {
        "id": 2,
        "name": "Avis Mcknight"
      }
    ],
    "greeting": "Hello, Murray Juarez! You have 5 unread messages.",
    "favoriteFruit": "apple"
  },
  {
    "_id": "594e5c7eaa31ab4bea2c8491",
    "index": 3,
    "guid": "d6eb97ed-b862-4f17-88b7-0d0690aee5fa",
    "isActive": true,
    "balance": "$3636.93",
    "picture": "http://placehold.it/32x32",
    "age": 21,
    "eyeColor": "blue",
    "name": "Desiree Luna",
    "gender": "female",
    "company": "MEDIOT",
    "email": "desireeluna@mediot.com",
    "phone": "+1 (915) 409-3173",
    "address": "282 Perry Place, Waumandee, West Virginia, 9813",
    "about": "Nostrud do qui elit irure nostrud ad nulla laboris et sint enim enim. Elit qui labore elit dolore minim incididunt dolor officia duis eiusmod nostrud reprehenderit cupidatat Lorem. Sunt minim nisi incididunt ullamco adipisicing sit velit aliquip anim officia tempor nostrud voluptate. Occaecat cillum officia laborum anim aliqua elit qui nisi amet sint eiusmod. Laboris velit ut eu sit duis. Adipisicing id officia fugiat nostrud minim ut ex nostrud quis deserunt ullamco laborum.\\r\\n",
    "registered": "2015-07-07T02:04:49 -08:00",
    "latitude": 56.648276,
    "longitude": 140.799557,
    "tags": [
      "labore",
      "ipsum",
      "laboris",
      "magna",
      "est",
      "excepteur",
      "laboris"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Neva Hess"
      },
      {
        "id": 1,
        "name": "Farley Harding"
      },
      {
        "id": 2,
        "name": "Schmidt Powers"
      }
    ],
    "greeting": "Hello, Desiree Luna! You have 3 unread messages.",
    "favoriteFruit": "strawberry"
  },
  {
    "_id": "594e5c7e2b8148d9d23695fc",
    "index": 4,
    "guid": "7ee58d19-c628-4d1b-9e19-799d60c6867f",
    "isActive": false,
    "balance": "$1585.11",
    "picture": "http://placehold.it/32x32",
    "age": 31,
    "eyeColor": "brown",
    "name": "Jasmine Rios",
    "gender": "female",
    "company": "ATGEN",
    "email": "jasminerios@atgen.com",
    "phone": "+1 (983) 517-2761",
    "address": "179 Division Avenue, Alfarata, American Samoa, 5456",
    "about": "Ex amet exercitation consequat exercitation ad consequat sunt laboris minim reprehenderit cupidatat. Cillum commodo duis excepteur est id. Laboris est qui consequat eiusmod aliqua reprehenderit et consectetur. Velit laborum minim ex cillum culpa. Est nulla commodo esse et adipisicing cillum nostrud. Cupidatat velit dolore excepteur laborum.\\r\\n",
    "registered": "2015-01-14T07:01:11 -08:00",
    "latitude": 25.760085,
    "longitude": -118.941993,
    "tags": [
      "labore",
      "deserunt",
      "cupidatat",
      "aliquip",
      "non",
      "duis",
      "in"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Hahn Huffman"
      },
      {
        "id": 1,
        "name": "Jeannette Anthony"
      },
      {
        "id": 2,
        "name": "Gayle Duke"
      }
    ],
    "greeting": "Hello, Jasmine Rios! You have 6 unread messages.",
    "favoriteFruit": "banana"
  },
  {
    "_id": "594e5c7e71e4e1c58307b06b",
    "index": 5,
    "guid": "461a7212-30ca-4226-be6f-25d9f7547ab4",
    "isActive": true,
    "balance": "$1770.51",
    "picture": "http://placehold.it/32x32",
    "age": 39,
    "eyeColor": "brown",
    "name": "Wilkinson Gordon",
    "gender": "male",
    "company": "OLUCORE",
    "email": "wilkinsongordon@olucore.com",
    "phone": "+1 (855) 489-3579",
    "address": "849 Opal Court, Vienna, Michigan, 3409",
    "about": "Fugiat irure velit labore tempor. Aliqua reprehenderit deserunt et velit. Ea cillum aute sit non sunt ex culpa. Aliqua do do ad nostrud commodo deserunt excepteur. Ullamco et velit magna pariatur cupidatat. Minim id tempor ea dolore.\\r\\n",
    "registered": "2017-04-21T12:15:50 -08:00",
    "latitude": 25.323726,
    "longitude": 115.13254,
    "tags": [
      "culpa",
      "sunt",
      "nostrud",
      "ad",
      "amet",
      "excepteur",
      "exercitation"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Aguirre Bridges"
      },
      {
        "id": 1,
        "name": "Rowland Levy"
      },
      {
        "id": 2,
        "name": "Guy Roberts"
      }
    ],
    "greeting": "Hello, Wilkinson Gordon! You have 2 unread messages.",
    "favoriteFruit": "strawberry"
  }
]
    """
    slist.append(s1)
    slist.append(s2)
    slist.append(s3)
    for i, s in enumerate(slist):
        # log(tokenizer(s))
        ensure(json.loads(s) == tree(s), '*** {}'.format(str(i)))
        log(tree(s), 'tree')
        log(json.loads(s), 'jsonloads')

def test():
    # test_tokenizer()
    # test_parser()
    test_tree()

if __name__ == '__main__':
    test()
