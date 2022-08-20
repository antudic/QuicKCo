import traceback




def formatTraceback(error):
    return ''.join(traceback.format_exception(None, error, error.__traceback__))


class Module:

    def __init__(self):
        self.name = "eval"


    def __call__(self, args):
        try: result = eval(args)
        except Exception as error:
            result = formatTraceback(error)

        return result
