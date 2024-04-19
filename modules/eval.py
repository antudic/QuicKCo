import traceback

def formatTraceback(error):
    return ''.join(traceback.format_exception(None, error, error.__traceback__))


class Module:

    def __init__(self):
        self.name    = "eval"
        self.modules = None


    def __call__(self, args):
        try: return str(eval(args))
        
        except Exception as error:
            return formatTraceback(error)
