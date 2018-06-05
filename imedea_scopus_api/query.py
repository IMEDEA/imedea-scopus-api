
#
# Helper classes
#


class DocType:

    def __init__(self, doc_type):
        self.value = doc_type

    def get_value(self):
        return self.value


class SourceType:

    def __init__(self, source_type):
        self.value = source_type

    def get_value(self):
        return self.value


class SubjectArea:

    def __init__(self, subject_area):
        self.value = subject_area

    def get_value(self):
        return self.value

#
# Main Query class
#


class Query:

    DOC_TYPE_ARTICLE = DocType('ar')
    DOC_TYPE_ABSTRACT_REPORT = DocType('ab')
    DOC_TYPE_ARTICLE_IN_PRESS = DocType('ip')
    DOC_TYPE_BOOK = DocType('bk')
    DOC_TYPE_BUSINESS_ARTICLE = DocType('bz')
    DOC_TYPE_BOOK_CHAPTER = DocType('ch')
    DOC_TYPE_CONFERENCE_PAPER = DocType('cp')
    DOC_TYPE_CONFERENCE_REVIEW = DocType('cr')
    DOC_TYPE_EDITORIAL = DocType('ed')
    DOC_TYPE_ERRATUM = DocType('er')
    DOC_TYPE_LETTER = DocType('le')
    DOC_TYPE_NOTE = DocType('no')
    DOC_TYPE_PRESS_RELEASE = DocType('pr')
    DOC_TYPE_REVIEW = DocType('re')
    DOC_TYPE_SHORT_SURVEY = DocType('sh')

    SRC_TYPE_JOURNAL = SourceType('j')
    SRC_TYPE_BOOK = SourceType('b')
    SRC_TYPE_BOOK_SERIES = SourceType('k')
    SRC_TYPE_CONFERENCE_PROCEEDING = SourceType('p')
    SRC_TYPE_REPORT = SourceType('r')
    SRC_TYPE_TRADE_PUBLICATION = SourceType('d')

    SBJ_AREA_AGRICULTURAL_AND_BIOLOGICAL_SCIENCES = SubjectArea('AGRI')
    SBJ_AREA_ARTS_AND_HUMANITIES = SubjectArea('ARTS')
    SBJ_AREA_BIOCHEMISTRY_GENETICS_AND_MOLECULAR_BIOLOGY = SubjectArea('BIOC')
    SBJ_AREA_BUSINESS_MANAGEMENT_AND_ACCOUNTING = SubjectArea('BUSI')
    SBJ_AREA_CHEMICAL_ENGINEERING = SubjectArea('CENG')
    SBJ_AREA_CHEMISTRY = SubjectArea('CHEM')
    SBJ_AREA_COMPUTER_SCIENCE = SubjectArea('COMP')
    SBJ_AREA_DECISION_SCIENCES = SubjectArea('DECI')
    SBJ_AREA_DENTISTRY = SubjectArea('DENT')
    SBJ_AREA_EARTH_AND_PLANETARY_SCIENCES = SubjectArea('EART')
    SBJ_AREA_ECONOMICS_ECONOMETRICS_AND_FINANCE = SubjectArea('ECON')
    SBJ_AREA_ENERGY = SubjectArea('ENER')
    SBJ_AREA_ENGINEERING = SubjectArea('ENGI')
    SBJ_AREA_ENVIRONMENTAL_SCIENCE = SubjectArea('ENVI')
    SBJ_AREA_HEALTH_PROFESSIONS = SubjectArea('HEAL')
    SBJ_AREA_IMMUNOLOGY_AND_MICROBIOLOGY = SubjectArea('IMMU')
    SBJ_AREA_MATHEMATICS = SubjectArea('MATH')
    SBJ_AREA_TRADE_PUBLICATION = SubjectArea('MEDI')
    SBJ_AREA_MEDICINE = SubjectArea('NEUR')
    SBJ_AREA_NURSING = SubjectArea('NURS')
    SBJ_AREA_PHARMACOLOGY_TOXICOLOGY_AND_PHARMACEUTICS = SubjectArea('PHAR')
    SBJ_AREA_PHYSICS_AND_ASTRONOMY = SubjectArea('PHYS')
    SBJ_AREA_PSYCHOLOGY = SubjectArea('PSYC')
    SBJ_AREA_SOCIAL_SCIENCES = SubjectArea('SOCI')
    SBJ_AREA_VETERINARY = SubjectArea('VETE')
    SBJ_AREA_MULTIDISCIPLINARY = SubjectArea('MULT')

    def __init__(self):
        self.query = []

    #
    # Operators
    #

    def and_(self):
        self.query.append('AND')
        return self

    def or_(self):
        self.query.append('OR')
        return self

    def not_(self):
        self.query.append('NOT')
        return self

    #
    # Pars
    #
    def open_par(self):
        self.query.append('(')
        return self

    def close_par(self):
        self.query.append(')')
        return self

    #
    # Fields
    #

    def abstract(self, *abstract_content):
        self.__extend('ABS', *abstract_content)
        return self

    def affiliation(self, *affiliation_content):
        """AFFILCITY + AFFILCOUNTRY + AFFILORG"""
        self.__extend('AFFIL', *affiliation_content)
        return self

    def affiliation_id(self, *af_id):
        self.__extend('AF-ID', *af_id)
        return self

    def all(self, *all_content):
        """All fields ABS, AFFIL...."""
        self.__extend('ALL', *all_content)
        return self

    def article_number(self, *article_number_content):
        self.__extend('ARTNUM', *article_number_content)
        return self

    def author_identifier_number(self, *author_id):
        self.__extend('AU-ID', *author_id)
        return self

    def author(self, *author_name):
        self.__extend('AUTH', *author_name)
        return self

    def author_collab(self, *author_collab_content):
        self.__extend('AUTHCOLLAB', *author_collab_content)
        return self

    def author_first(self, author_first_content):
        self.__extend('AUTHFIRST', *author_first_content)
        return self

    def author_last_name(self, author_last_name_content):
        self.__extend('AUTHLASTNAME', *author_last_name_content)
        return self

    def author_name(self, author_last_name, author_name):
        author_tuple = ('AUTHLASTNAME', '(', author_last_name, ')', 'AUTHFIRST', '(', author_name, ')')
        self.__extend('AUTHOR-NAME', *author_tuple)
        return self

    def cas_registry_number(self, *cas_registry_number_content):
        self.__extend('CASREGNUMBER', *cas_registry_number_content)
        return self

    def chemical(self, *chemical_content):
        """Comination of CHEMNAME and CASREGNUMBER"""
        self.__extend('CHEM', *chemical_content)
        return self

    def chemical_name(self, *chemical_name_content):
        self.__extend('CHEMNAME', *chemical_name_content)
        return self

    def coden(self, *coden_content):
        self.__extend('CODEN', coden_content)
        return self

    def conference_information(self, *conference_information_content):
        """Combination of CONFNAME, CONFSPONSORS AMD CONFLOC (location)"""
        self.__extend('CONF', *conference_information_content)
        return self

    def conference_location(self, *conference_location_content):
        self.__extend('CONFLOC', *conference_location_content)
        return self

    def conference_name(self, *conference_name_content):
        self.__extend('CONFNAME', *conference_name_content)
        return self

    def conference_sponsors(self, *conference_sponsors_content):
        self.__extend('CONFSPONSORS', *conference_sponsors_content)
        return self

    def document_type(self, *document_type_content):
        l = []
        for dc in document_type_content:
            if isinstance(dc, DocType):
                l.append(dc.get_value())
                l.append("OR")
                continue
            print (str(dc) + " not instance of DocType query helper, "
                   "use any DOC_TYPE_* attributes of Query class. Exiting...")
            exit(-1)
        if l:
            l.pop()
        self.__extend('DOCTYPE', *tuple(l))
        return self

    def doi(self, *doi_content):
        self.__extend('DOI', *doi_content)
        return self

    def editor_first_name(self, *editor_first_name_content):
        self.__extend('EDFIRST', *editor_first_name_content)
        return self

    def editor(self, *editor_content):
        """Combined fields EDFIRST AND EDLASTNAME"""
        self.__extend('EDITOR', *editor_content)
        return self

    def editor_last_name(self, *editor_last_name_content):
        self.__extend('EDLASTNAME', *editor_last_name_content)
        return self

    def eid(self, *eid_content):
        self.__extend('EID', *eid_content)
        return self

    def eissn(self, *eissn_content):
        self.__extend('EISSN', *eissn_content)
        return self

    def exact_source_title(self, *exact_source_title_content):
        self.__extend('EXACTSRCTITLE', *exact_source_title_content)
        return self

    def first_author(self, *first_author_content):
        self.__extend('FIRSTAUTH', *first_author_content)
        return self

    def funding_sponsor_acronym(self, *funding_sponsor_acronym_content):
        self.__extend('FUND-ACR', *funding_sponsor_acronym_content)
        return self

    def funding_grant_number(self, *funding_grant_number_content):
        self.__extend('FUND-NO', *funding_grant_number_content)
        return self

    def funding_sponsor(self, *funding_sponsor_content):
        self.__extend('FUND-SPONSOR', *funding_sponsor_content)
        return self

    def index_terms(self, *index_terms_content):
        self.__extend('INDEXTERMS', *index_terms_content)
        return self

    def isbn(self, *isbn_content):
        self.__extend('ISBN', *isbn_content)
        return self

    def issn(self, *issn_content):
        self.__extend('ISSN', *issn_content)
        return self

    def issnp(self, *issnp_content):
        self.__extend('ISSNP', *issnp_content)
        return self

    def issue(self, *issue_content):
        self.__extend('ISSUE', *issue_content)
        return self

    def keywords(self, *keywords_content):
        self.__extend('KEY', *keywords_content)
        return self

    def language(self, *language_content):
        self.__extend('LANGUAGE', *language_content)
        return self

    def manufacturer(self, *manufacturer_content):
        self.__extend('MANUFACTURER', *manufacturer_content)
        return self

    def page_first(self, *page_first_content):
        self.__extend('PAGEFIRST', *page_first_content)
        return self

    def page_last(self, *page_last_content):
        self.__extend('PAGELAST', *page_last_content)
        return self

    def pages(self, *pages_content):
        self.__extend('PAGES', *pages_content)
        return self

    def publication_item_identifier(self, *publication_item_identifier_content):
        self.__extend('PII', *publication_item_identifier_content)
        return self

    def pubmed_identifier(self, *pubmed_identifier_content):
        self.__extend('PMID', *pubmed_identifier_content)
        return self

    def publication_date_text(self, *publication_date_text_identifier):
        self.__extend('PUBDATETXT', *publication_date_text_identifier)
        return self

    def publication_year(self, operator, year):
        self.query.extend(['PUBYEAR', ' ', operator, ' ', year])
        return self

    def references(self, subquery):
        """ Combined field for REFAUTH, REFTITLE, REFSRCTITLE, REFPUBYEAR, REFPAGE"""
        if not isinstance(subquery, Query):
            print ("References is a combined field for REFAUTH, REFTITLE, REFSRCTITLE, REFPUBYEAR AND REFPAGE. "
                   "Create a query object with these fields to perform a combined search")
            exit(-1)
        self.__extend('REF', *tuple(subquery.query))
        return self

    def reference_article_number(self, *reference_article_number_content):
        self.__extend('REFARTNUM', *reference_article_number_content)
        return self

    def reference_authors(self, *reference_authors_content):
        self.__extend('REFAUTH', *reference_authors_content)
        return self

    def reference_page(self, *reference_page_content):
        self.__extend('REFPAGE', *reference_page_content)
        return self

    def reference_first_page(self, *reference_first_page_content):
        self.__extend('REFPAGEFIRST', *reference_first_page_content)
        return self

    def reference_publication_year(self, year):
        self.query.extend(['REFPUBYEAR', 'IS', year])
        return self

    def reference_source_title(self, *reference_source_title_content):
        self.__extend('REFSRCTITLE', *reference_source_title_content)
        return self

    def reference_title(self, *reference_title_content):
        self.__extend('REFTITLE', *reference_title_content)
        return self

    def sequence_bank(self, *sequence_back_content):
        self.__extend('SEQBANK', *sequence_back_content)
        return self

    def sequence_bank_accession_number(self, *sequence_bank_accession_number_content):
        self.__extend('SEQNUMBER', *sequence_bank_accession_number_content)
        return self

    def source_title(self, *source_title_content):
        self.__extend('SRCTITLE', *source_title_content)
        return self

    def source_type(self, *source_type_content):
        l = []
        for st in source_type_content:
            if isinstance(st, SourceType):
                l.append(st.get_value())
                l.append("OR")
                continue
            print (str(st) + " not instance of SourceType query helper, "
                             "use any SRC_TYPE_* attributes of Query class. Exiting...")
            exit(-1)
        if l:
            l.pop()
        self.__extend('SRCTYPE', *tuple(l))

    def subject_area(self, *subject_area_content):
        l = []
        for sa in subject_area_content:
            if isinstance(sa, SubjectArea):
                l.append(sa.get_value())
                l.append("OR")
                continue
            print (str(sa) + " not instance of SubjectArea query helper, "
                             "use any SBJ_AREA_* attributes of Query class. Exiting...")
            exit(-1)
        if l:
            l.pop()
        self.__extend('SUBJAREA', *tuple(l))

    def title(self, *title_content):
        self.__extend('TITLE', *title_content)
        return self

    def title_abstract_or_keywords(self, *title_abstract_or_keywords_content):
        self.__extend('TITLE-ABS-KEY', *title_abstract_or_keywords_content)
        return self

    def title_abstract_keywords_or_author_names(self, *content):
        self.__extend('TITLE-ABS-KEY-AUTH', *content)
        return self

    def tradename(self, *tradename_content):
        self.__extend('TRADENAME', *tradename_content)
        return self

    def volume(self, *volume_content):
        self.__extend('VOLUME', *volume_content)
        return self

    def website(self, *website_content):
        self.__extend('WEBSITE', *website_content)
        return self

    #
    # Get joined query
    #
    def get_query(self):
        return " ".join(self.query)

    #
    # Private
    #

    def __extend(self, key, *value):
        joined_value = " ".join(value)
        self.query.extend([key, "(", joined_value, ")"])

