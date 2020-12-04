import urllib
import urllib2
import logging

import utils
from auth import Auth
from query import Query


class View:
    def __init__(self, type):
        self.type = type


class Sort:
    def __init__(self, type):
        self.type = type


class ELSClient:

    VIEW_STANDARD = View('STANDARD')
    VIEW_COMPLETE = View('COMPLETE')

    SORT_ART_NUM_ASC = Sort('+artnum')
    SORT_ART_NUM_DESC = Sort('-artnum')
    SORT_CITED_BY_COUNT_ASC = Sort('+citedby-count')
    SORT_CITED_BY_COUNT_DESC = Sort('-citedby-count')
    SORT_COVER_DATE_ASC = Sort('+coverDate')
    SORT_COVER_DATE_DESC = Sort('-coverDate')
    SORT_CREATOR_ASC = Sort('+creator')
    SORT_CREATOR_DESC = Sort('-creator')
    SORT_ORIG_LOAD_DATE_ASC = Sort('+orig-load-date')
    SORT_ORIG_LOAD_DATE_DESC = Sort('+orig-load-date')
    SORT_PAGE_COUNT_ASC = Sort('+pagecount')
    SORT_PAGE_COUNT_DESC = Sort('-pagecount')
    SORT_PAGE_FIRST_ASC = Sort('+pagefirst')
    SORT_PAGE_FIRST_DESC = Sort('-pagefirst')
    SORT_PAGE_RANGE_ASC = Sort('+pageRange')
    SORT_PAGE_RANGE_DESC = Sort('-pageRange')
    SORT_PUBLICATION_NAME_ASC = Sort('+publicationName')
    SORT_PUBLICATION_NAME_DESC = Sort('-publicationName')
    SORT_PUBLICATION_YEAR_ASC = Sort('+pubyear')
    SORT_PUBLICATION_YEAR_DESC = Sort('-pubyear')
    SORT_REVELANCY_ASC = Sort('+revelancy')
    SORT_REVELANCY_DESC = Sort('-revelancy')
    SORT_VOLUME_ASC = Sort('+volume')
    SORT_VOLUME_DESC = Sort('-volume')

    def __init__(self, api_key, choice=None, tunnel_url=None, tunnel_port=None):
        self.auth = Auth(api_key, choice=choice, tunnel_url=tunnel_url, tunnel_port=tunnel_port)
        self.header = self.auth.getheader()
        self.custom_header = dict()

    #
    #   Headers
    #
    def __get_header(self):
        new_header = self.header
        if self.custom_header:
            for k, v in self.custom_header.iteritems():
                new_header[k] = v
        return new_header

    #
    #   Abstract Retrieval
    #

    def get_abstract_by_doi(self, doi):
        """Returns the abstract of publication via its 'doi' identifier"""
        return self.__get_abstract(doi, 'doi')

    def get_abstract_by_eid(self, eid):
        """Returns the abstract of publication via its 'eid' identifier"""
        return self.__get_abstract(eid, 'eid')

    def get_abstract_by_scopus_id(self, scopus_id):
        """Returns the abstract of publication via its 'scopus' identifier"""
        return self.__get_abstract(scopus_id, 'scopus_id')

    def get_abstract_by_pii(self, pii):
        """Returns the abstract of publication via its 'pii' identifier"""
        return self.__get_abstract(pii, 'pii')

    def __get_abstract(self, identifier, identifier_type):
        url = "https://api.elsevier.com/content/abstract/" + identifier_type + "/" + identifier
        json_data = None
        try:
            json_data = utils.get_json_from_url(url, self.__get_header())
        except urllib2.HTTPError as e:
            print "Error getting abstract"
            utils.print_http_error(e)
            raise e
        return json_data

    #
    # Author Retrieval
    #

    def get_author_by_author_id(self, author_id):
        return self.__get_author(author_id, 'author_id')

    def get_author_by_eid(self, eid):
        return self.__get_author(eid, 'eid')

    def get_author_by_orcid(self, orcid):
        return self.__get_author(orcid, 'orcid')

    def __get_author(self, identifier, identifier_type):
        url = "https://api.elsevier.com/content/author/" + identifier_type + "/" + identifier
        json_data = None
        try:
            json_data = utils.get_json_from_url(url, self.__get_header())
        except urllib2.HTTPError as e:
            print "Error retrieving author information"
            utils.print_http_error(e)
            raise e
        return json_data

    #
    # Affiliation retrieval
    #

    def get_affiliation_by_affiliation_id(self, affiliation_id):
        return self.__get_affiliation(affiliation_id, "affiliation_id")

    def get_affiliation_by_eid(self, eid):
        return self.__get_affiliation(eid, 'eid')

    def __get_affiliation(self, identifier, identifier_type):
        url = "https://api.elsevier.com/content/affiliation/" + identifier_type + "/" + identifier
        json_data = None
        try:
            json_data = utils.get_json_from_url(url, self.__get_header())
        except urllib2.HTTPError as e:
            print "Error retrieving affiliation information"
            utils.print_http_error(e)
            raise e
        return json_data

    #
    # Journal
    #
    def get_journal_metrics(self, issn, initial_year=1900, end_year=2100):
        url = ''.join((
                "https://api.elsevier.com/content/serial/title?issn=" + issn,
                "&view=",
                self.VIEW_STANDARD.type,
                "&date=" + str(initial_year) + "-" + str(end_year)
               ))
        json_data = None
        try:
            json_data = utils.get_json_from_url(url, self.__get_header())
        except urllib2.HTTPError as e:
            print "Error retrieving journal metrics -> " + url
            utils.print_http_error(e)
            raise e
        return json_data

    #
    # Scopus search
    #
    def scopus_search(self,
                      query,
                      view=VIEW_STANDARD,
                      suppress_nav_links=False,
                      date=None,
                      start=0,
                      count=25,
                      field=None,
                      sort=None):
        if not isinstance(query, Query):
            print("Query parameter must be set and should be an instance of Query class. Exiting...")
            exit(-1)
        if not isinstance(view, View):
            print("View parameter must be an instance of inner View class. Check attributes starting with View_* in "
                  "ElsClient object. "
                  "Program will exit...")
            exit(-1)
        if not isinstance(suppress_nav_links, bool):
            print("suppress_nav_links parameter should be either True or False. Exiting...")
            exit(-1)
        query_quoted = urllib.quote_plus(query.get_query())
        url = "https://api.elsevier.com/content/search/scopus?" \
              "view=" + view.type + \
              "&query=" + query_quoted + \
              "&suppressNavLinks=" + str(suppress_nav_links).lower()
        if date:
            url += "&date=" + date
        if field:
            url += "&field=" + field
        url += "&start=" + str(start) + "&count=" + str(count)
        if sort:
            if not isinstance(sort, list) and not isinstance(sort, tuple):
                print "Sort parameter must be either a list or tuple of a maximum of 3 Sort elements. Program will exit..."
                exit(-1)
            if len(sort) > 3:
                print "Sort parameter has a maximum of 3 elements. Program will exit..."
                exit(-1)
            l = []
            for s in sort:
                if not isinstance(s, Sort):
                    print("All elements of sort parameter must be of Sort class. Check attributes starting with Sort_* "
                          "in ElsClient object. Program will exit...")
                    exit(-1)
                l.append(s.type)
            sort_joined = ",".join(l)
            url += "&sort=" + sort_joined

        json_data = None
        try:
            json_data = utils.get_json_from_url(url, self.__get_header())
        except urllib2.HTTPError as e:
            print "Error while retrieving information from SCOPUS:"
            utils.print_http_error(e)
            raise e

        return json_data

    #
    # Retrieve all scopus identifiers without paging
    #
    def get_all_identifiers(self, query):
        if not isinstance(query, Query):
            logging.fatal("query parameter must be an instance of query. Exiting...")
            exit(-1)
        try:
            j = self.scopus_search(query, start=0, field='identifier')
        except Exception as e:
            raise e
        next_start, should_loop, result_list = self.__process_query_json(j)
        while should_loop:
            j = self.scopus_search(query, start=next_start)
            next_start, should_loop, l2 = self.__process_query_json(j)
            result_list.extend(l2)
        return result_list

    def __process_query_json(self, j):
        j = j['search-results']
        start = int(j['opensearch:Query']['@startPage'])
        count = len(j['entry'])
        total = int(j['opensearch:totalResults'])
        next_start = start + count
        should_loop = next_start < total
        l = []
        for o in j['entry']:
            if 'dc:identifier' in o:
                l.append(o['dc:identifier'])
        return next_start, should_loop, l