import time

from Ranker import Ranker


class Searcher:

    def __init__(self, docs_dictionary, main_dictionary, avdl, stem_suffix, ip, city_dictionary):
        self.main_dictionary = main_dictionary
        self.__ranker = Ranker(docs_dictionary, main_dictionary, avdl, len(docs_dictionary), stem_suffix, ip)
        self.__list_of_cities = []
        self.__city_dictionary = city_dictionary

     # will be trigger from controller
    def search(self, query_dict , addons_dict = None):
        '''
        searching docs that includes terms in query
        final rank in ranker class will be the final calculation
        :param query_dict: {term : { query : tf } }
        :param addons_dict: {term : { query : tf } } - optional
        '''

        query_dict = self.adjust_terms(query_dict)
        if addons_dict is not None: #title + description
            addons_dict = self.adjust_terms(addons_dict)
            all_terms = list(set(list(query_dict.keys()) + list(addons_dict.keys())))
            #all_terms = self.merge_all_terms_to_one_list(query_dict, addons_dict)
            self.__ranker.fill_mini_posting_file(sorted(all_terms, key=lambda v: v.upper()))
            if self.__list_of_cities is not None:
                self.remove_not_relevant_docs()
            ranked_titles = self.__ranker.rank(query_dict)
            ranked_addons = self.__ranker.rank(addons_dict)
            self.__ranker.calculate_final_rank(ranked_titles, ranked_addons) #saves the result in final_result &&& takes top 50

        else:
            self.__ranker.fill_mini_posting_file(sorted(query_dict.keys(), key=lambda v: v.upper()))
            if self.__list_of_cities is not None:
                self.remove_not_relevant_docs()
            ranked_docs = self.__ranker.rank(query_dict)
            self.__ranker.final_result = ranked_docs
            self.__ranker.final_result["999"] = self.__ranker.get_top_docs("999")

    def get_final_result(self):
        return self.__ranker.final_result

    def set_cities_filter_list(self, list):
        self.__list_of_cities = list

    def adjust_terms(self, query_dict):
        '''

        :param query_dict: {term : { query : tf } }
        :return:
        '''
        result = {}
        for term in query_dict:
            if term not in self.main_dictionary:
                value = query_dict[term]
                if term.lower() in self.main_dictionary:
                    if term.lower() not in result:
                        result[term.lower()] = value
                    else:  # exists in result -> merge
                        result[term.lower()] = self.mergi_mergi(result[term.lower()], value)
                elif term.upper() in self.main_dictionary:
                    if term.upper() not in result:
                        result[term.upper()] = value
                    else: #exists in result -> merge
                        result[term.upper()] = self.mergi_mergi(result[term.upper()], value)
                else:
                    #print (term + " not exists in main dic at all")
                    if term not in result:
                        result[term] = query_dict[term]
                    else:
                        result[term] = self.mergi_mergi(result[term], query_dict[term])
                    #not exists in the main dictionary
            else:
                if term not in result:
                    result[term] = query_dict[term]
                else:
                    result[term] = self.mergi_mergi(result[term], query_dict[term])
        return result

    def mergi_mergi(self, dic1, dic2):
        '''
        merge two dictionaries that looks like this: { Query:tf in query }
        :param dic1: first
        :param dic2: second
        :return: merged dictionary
        '''
        for q in dic1:
            if q in dic2:
                dic2[q] += dic1[q]
            else:
                dic2[q] = dic1[q]
        return dic2

    def merge_all_terms_to_one_list(self, query_dict, addons_dict):
        '''
        creates a list of merged terms
        :param query_dict: {term : { query : tf } }
        :param addons_dict: {term : { query : tf } }
        :return: list of terms
        '''
        result = []
        for term in query_dict:
            if term not in result:
                result.append(term)
        for term in addons_dict:
            if term not in result:
                result.append(term)
        return result

    def remove_not_relevant_docs(self):
        city_docs = [] # will contain list of all possible docs
        for city_name in self.__list_of_cities:
            city_docs = list(set(list(self.__city_dictionary[city_name].dic_doc_index.keys()) + city_docs))
        city_docs = {key : None for key in city_docs} #now, city_docs is dictionary for faster result
        self.__ranker.city_docs = city_docs


