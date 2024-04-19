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
                if self.texts:
                    return ", ".join(list(self.texts.keys()))
                else:
                    return "No saved texts."

            elif args[0] in ["text", "help"]:
                return "No argument supplied.\ntext ls: List all saved texts\ntext [name of saved text]: Retrieve the saved text\ntext set [name of text] [text]: save `text` as `name of text` (can overwrite) (spaces are not allowed in text names)\ntext rm [name of text]: discard the given text"
            
            else: 
                try: return self.texts[args[0]]
                except KeyError: return f"Unknown argument \"{args[0]}\""

        elif len(args) == 2:
            # user entered: text [get/del/delete/remove/rem/unknown] [name of text/unknown]

            if args[0] == "get":
                try: return self.texts[args[1]]
                except KeyError: return f"no text named {args[1]}"

            elif args[0] in ["del", "delete", "remove", "rem", "rm"]:
                try: del self.texts[args[1]]
                except KeyError: return

        elif len(args) > 2:
            if args[0] in ["set", "save"]:
                # user entered: text [set] [name of text] *[text to save]

                name = args[1]
                textBlock = " ".join(args[2:])
                
                self.texts[name] = textBlock

                self.save()
            
            else:
                # user entered: text *[unknown]
                return f"Unknown argument \"{args[0]}\""

        else:
            # user entered: text
            return 



    def load(self):
        with open("./modules/text/texts.json", "r") as file:
            self.texts = json.load(file)


    def save(self):
        with open("./modules/text/texts.json", "w") as file:
            json.dump(self.texts, file, indent="    ", sort_keys=True)
