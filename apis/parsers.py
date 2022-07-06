def list_parser(item_parser=int):
    def f(value):
        try:
            return [item_parser(v.strip()) for v in value.split(',')]
        except:
            raise ValueError()

    return f
