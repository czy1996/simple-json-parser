def log(*args):
    print(args)


def ensure(condition, message):
    if not condition:
        print('*** 测试失败', message)
    else:
        print('*** 测试成功', message)
