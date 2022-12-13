import traceback
import json

def formatTraceback(error):
    return ''.join(traceback.format_exception(None, error, error.__traceback__))


class Module:

    def __init__(self):
        self.name    = "text"
        self.modules = None
        self.texts   = None

        self.load()


    def __call__(self, args):
        try: return self.interpreter(args)

        except Exception as error:
            return formatTraceback(error)


    def interpreter(self, args):
        args = args.split(" ")

        if len(args) == 1:
            if args[0] in ["ls", "list"]:
                return ", ".join(list(self.texts.keys()))

        elif len(args) == 2:

            if args[0] == "get":
                try: return self.texts[args[1]]
                except KeyError: return f"no text named {args[1]}"

            elif args[0] in ["del", "delete", "remove", "rem"]:
                try: del self.texts[args[1]]
                except KeyError: return

        elif len(args) > 2 and args[0] == "set":
            name = args[1]
            textBlock = " ".join(args[2:])
            
            self.texts[name] = textBlock

            self.save()

        else: return


    def load(self):
        with open("./modules/text/texts.json", "r") as file:
            self.texts = json.load(file)


    def save(self):
        with open("./modules/text/texts.json", "w") as file:
            json.dump(self.texts, file)
