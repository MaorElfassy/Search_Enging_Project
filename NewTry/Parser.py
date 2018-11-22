
__punctuations_set = {'[', '(', '{', '`', ')', '<', '|', '&', '~', '+', '^', '@', '*', '?', '.',
                      '>', ';', '_', '\'', ':', ']', '\\', "}", '!', '=', '#', ',', '\"'}

__months_set = {'january':'01', 'jan':'01', 'february':'02', 'feb':'02', 'march':'03', 'mar':'03', 'april':'04', 'apr':'04',
                'may':'05', 'june':'06', 'jun':'06', 'july':'07', 'jul':'07', 'august':'08', 'aug':'08', 'september':'09',
                'sep':'09', 'october':'10', 'oct':'10', 'november':'11', 'nov':'11', 'december':'12', 'dec':'12'}

def clean_term_from_punctuations(term):
    length = term.__len__()
    while length > 0 and term[len(term)-1] in __punctuations_set:
        term = term[:-1]
        length -= 1
    while length > 0 and term[0] in __punctuations_set:
        term = term[1:]
        length -= 1
    return term


def isNumeric(word):
    return word.isdigit() or word.replace(',','').replace('.','').replace('$','').replace('m','').replace("bn",'').isdigit()

def get_clear_number(word):
    return word.replace('$','').replace('m','').replace("bn",'')

def get_bn_ot_m(word):
    if "bn" in word:
        return "B"
    elif "m" in word:
        return "M"
    elif "t" in word:
        return "T"
    else: return ""

def parse(dictionary):
    for doc in dictionary:
        text = dictionary[doc]
        if text is not None or text is not "":
            index = 0
            splited = text.split()
            length_of_splited_text = len(splited)
            while index < length_of_splited_text:
                new_term =""
                original_term = splited[index]
                term = clean_term_from_punctuations(original_term)
                if isNumeric(term): #for numbers , pruces, percentage, dates(!!!!!!!!!!!!!)
                    if '$' in term:
                        if index + 1 != length_of_splited_text:
                            next_word = splited[index + 1].lower()
                            if next_word in ["million", "billion", "trillion"]:
                                new_term = price_format(get_clear_number(term), next_word[0].upper()) # $ price million/billion,trillion
                                index = index + 2
                            else:
                                new_term = price_format(get_clear_number(term)) # S price
                                index = index + 1
                        else: #last one in text
                            new_term = price_format(get_clear_number(term)) # $ price
                            index = index + 1
                    else: # no $
                        if index + 1 != length_of_splited_text:
                            next_word = splited[index + 1].lower()
                            if next_word in ["percentage","percent"]:
                                new_term = percentage_format(term) # number percent/percentage
                                index = index + 2
                            elif next_word == "dollars":
                                new_term = price_format(get_clear_number(term),get_bn_ot_m(term)) # price dollars
                                index = index + 2
                            elif next_word in ["million", "billion", "trillion"]:
                                if index + 3 != length_of_splited_text:
                                    third_word = splited[index+2]
                                    fourth_word = splited[index+3].lower()
                                    if third_word == "U.S" and fourth_word == "dollars":
                                        new_term = price_format(get_clear_number(term),next_word[0].upper()) # price million/trillion/billion U.S dollars
                                        index = index + 4
                                    else:
                                        new_term = number_kbmt_format(term, next_word) # number million/billion/trillion
                                        index = index + 2
                                else:
                                    new_term = number_kbmt_format(term, next_word)# number million/billion/trillion
                                    index = index + 2
                            elif next_word == "thousand":
                                new_term = number_kbmt_format(term, next_word) # number thousand
                                index = index + 2
                            elif index + 2 != length_of_splited_text:
                                third_word = splited[index+2].lower()
                                if third_word == "dollars" and '/' in next_word and isNumeric(next_word.replace('/','')):
                                    new_term = fraction_price_format(get_clear_number(term), get_clear_number(next_word)) #number fraction dollars
                                    index = index + 3
                            elif next_word in __months_set:
                                new_term = dd_month_format(term, next_word) # DD Month
                                index = index + 2
                            else:
                                new_term = number_format(term) # number
                                index = index + 1
                        else: #last number in text
                            new_term = number_format(term) # number
                            index = index + 1
                else: # take care of words
                    if term.lower() in __months_set.keys():
                        if index + 1 != length_of_splited_text:
                            next_word = splited[index+1]
                            if next_word.isDigit() and len(next_word)<=2:
                                new_term = dd_month_format(next_word,term) # DD month
                                index = index + 2
                            elif next_word.isDigit() and len(next_word)==4:
                                new_term = month_year_format(next_word,term) # month year
                                index = index + 2
                    elif term.lower() == "between" and index + 3 <length_of_splited_text:
                        number1 = splited[index + 1]
                        if isNumeric(number1):
                            and_= splited[index + 2]
                            if and_ == "and":
                                number2 = splited[index + 3]
                                if isNumeric(number2):
                                    new_term = "between " + number1 + " and " + number2 #between n1 and n2
                                    index = index + 4
                    elif '-' in term:
                        new_term = term
                        index = index + 1
                    else: # upper/lower case regular word
                        new_term = upper_lower_case_format(term)
                        index = index + 1
                ###################################DONE WITH PARSING########################################



                    #Todo: advance the index
                    #Todo: take care of upper/lower cases
                    #Todo: add functions as needed
                #todo: check in indexer if term exist upper/lower ->> merging the keys




