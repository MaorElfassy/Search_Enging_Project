from nltk.tokenize import sent_tokenize, word_tokenize

class Parse:



    def tokenizeTexttoList(text):
        list = word_tokenize(text)
        return list

    @staticmethod
    def install_and_import(package):
        import importlib
        try:
            importlib.import_module(package)
        except ImportError:
            import pip
            pip.main(['install', package])
        finally:
            globals()[package] = importlib.import_module(package)


Parse.install_and_import('nltk')
text = 'Providing U.S. DavidFlores N.B.A. with his biggest victory. Miserden, who returned $68, $20.40 and $10.80, was on or near the lead throughout and got the best of Notorious Pleasure, the 3-1 choice, in the final yards. Three lengths back was </P>'
list = Parse.tokenizeTexttoList(text)
print (list)