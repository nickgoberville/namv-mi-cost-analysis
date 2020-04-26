def gen():
    def init():
        return 0
    i = init()
    x = 0
    y = 20
    while True:
        val = (yield i)
        if val=='restart':
            i = init()
        x += 5
        y *= 10
        print(x, y)
        yield x, y