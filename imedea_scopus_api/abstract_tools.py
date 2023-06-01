import logging

def get_root(json_source):
    return json_source['abstracts-retrieval-response']


def get_doi(json_source):
    coredata = __coredata(json_source)
    return coredata['prism:doi'] if 'prism:doi' in coredata else None


def get_date(json_source):
    return __coredata(json_source)['prism:coverDate']


def get_title(json_source):
    return __coredata(json_source)['dc:title']


def get_volume(json_source):
    coredata = __coredata(json_source)
    return coredata['prism:volume'] if 'prism:volume' in coredata else None


def get_start_page(json_source):
    coredata = __coredata(json_source)
    return coredata['prism:startingPage'] if 'prism:startingPage' in coredata else None


def get_end_page(json_source):
    coredata = __coredata(json_source)
    return coredata['prism:endingPage'] if 'prism:endingPage' in coredata else None


def get_abstract(json_source):
    coredata = __coredata(json_source)
    return coredata['dc:description'] if 'dc:description' in coredata else None


def get_url(json_source):
    coredata = __coredata(json_source)
    url = coredata['prism:url'] if 'prism:url' in coredata else None
    return url


def get_doi_url(json_source):
    url = None
    doi = get_doi(json_source)
    if (doi):
        url = 'https://dx.doi.org/' + doi
    return url


def get_type(json_source):
    root = get_root(json_source)
    item = root['item'] if 'item' in root else None
    abstract_type = None
    if item:
        abstract_type = item['bibrecord']['head']['citation-info']['citation-type']['@code']
    return abstract_type


def get_issue_identifier_number(json_source):
    coredata = __coredata(json_source)
    return coredata['prism:issueIdentifier'] if 'prism:issueIdentifier' in coredata else None


def is_related_to_center(json_source, affiliation_id):
    related = False
    root = get_root(json_source)
    affiliation_list = root['affiliation'] if 'affiliation' in root else None
    if isinstance(affiliation_list, list):
        for affiliation in affiliation_list:
            id = affiliation['@id'] if '@id' in affiliation else None
            if affiliation_id == id:
                related = True
                break
    elif affiliation_list:
        id = affiliation_list['@id'] if '@id' in affiliation_list else None
        related = affiliation_id == id
    return related


def has_foreign_affiliations(json_source, affiliation_id):
    root = get_root(json_source)
    affiliation_list = root['affiliation'] if 'affiliation' in root else None
    if isinstance(affiliation_list, list):
        for affiliation in affiliation_list:
            id = affiliation['@id'] if '@id' in affiliation else None
            if affiliation_id != id:
                return True
    elif affiliation_list:
        id = affiliation_list['@id'] if '@id' in affiliation_list else None
        return affiliation_id != id
    else:
        return False


def get_language(json_source):
    root = get_root(json_source)
    language = None
    language_json = root['language'] if 'language' in root else None
    if language_json:
        language = language_json['@xml:lang'] if '@xml:lang' in language_json else None
        logging.info("Found language: %s", language)
    if not language:
        logging.warning("Language not found in json source, using default 'eng' language")
        language = 'eng'
    return language


def get_keywords(json_source):
    root = get_root(json_source)
    keywords = None
    keywords_json = root['authkeywords'] if 'authkeywords' in root else None
    if keywords_json:
        keywords_array = keywords_json['author-keyword']
        if keywords_array:
            vals = []
            if isinstance(keywords_array, list):
                for keyword in keywords_array:
                    vals.append(keyword['$'])
            elif isinstance(keywords_array, dict):
                vals.append(keywords_array['$'])
            keywords = "; ".join(vals)
    return keywords


def get_isbn(json_source, standard_format = False):
    isbn = None
    isbn_root = get_root(json_source)['item']['bibrecord']['head']['source']
    isbn_entity = isbn_root['isbn'] if 'isbn' in list(isbn_root.keys()) else None
    if isinstance(isbn_entity, list):
        for isbn_object in isbn_entity:
            if isbn_object['@type'] == 'print' if '@type' in list(isbn_object.keys()) else None:
                isbn = isbn_object['$']
    elif isinstance(isbn_entity, dict):
        if isbn_entity['@type'] == 'print' if '@type' in list(isbn_entity.keys()) else None:
            isbn = isbn_entity['$']
    if isbn and standard_format:
        isbn = isbn[0:3] + '-' + isbn[3] + '-' + isbn[4:7] + '-' + isbn[7:12] + '-' + isbn[12]
    return isbn


def get_eisbn(json_source, standard_format = False):
    isbn = None
    isbn_root = get_root(json_source)['item']['bibrecord']['head']['source']
    isbn_entity = isbn_root['isbn'] if 'isbn' in list(isbn_root.keys()) else None
    if isinstance(isbn_entity, list):
        for isbn_object in isbn_entity:
            if isbn_object['@type'] == 'electronic' if '@type' in list(isbn_object.keys()) else None:
                isbn = isbn_object['$']
    elif isinstance(isbn_entity, dict):
        if isbn_entity['@type'] == 'electronic' if '@type' in list(isbn_entity.keys()) else None:
            isbn = isbn_entity['$']
    if isbn and standard_format:
        isbn = isbn[0:3] + '-' + isbn[3] + '-' + isbn[4:7] + '-' + isbn[7:12] + '-' + isbn[12]
    return isbn


def get_publisher(json_source):
    return __coredata(json_source)['dc:publisher']


def get_authors(json_source):
    author_list = None
    root = get_root(json_source)
    authors = root['authors'] if 'authors' in root else None
    if authors:
        author_list = authors['author'] if 'author' in authors else None
    return author_list


def author_is_related_to_center(author_json, affiliation_id):
    o = author_json['affiliation'] if 'affiliation' in author_json else None
    if isinstance(o, list):
        for affiliation in o:
            if affiliation['@id'] == affiliation_id:
                return True
    elif isinstance(o, dict):
        return o['@id'] == affiliation_id
    return False


def get_author_affiliations_id(author_json):
    o = author_json['affiliation'] if 'affiliation' in author_json else None
    affiliations = []
    if isinstance(o, list):
        for aff in o:
            affiliations.append(aff['@id'])
    elif isinstance(o, dict):
        affiliations.append(o['@id'])
    return affiliations


def get_source(json_source):
    source = None
    if 'item' in list(json_source['abstracts-retrieval-response'].keys()):
        source = json_source['abstracts-retrieval-response']['item']['bibrecord']['head']['source']
    return source


def get_source_title(json_source):
    source = get_source(json_source)
    if not source:
        return None
    source_title = source['sourcetitle']
    if isinstance(source_title, dict):
        source_title = source_title['$']
    return source_title


def get_source_abbrev(json_source):
    source = get_source(json_source)
    source_title = None
    if source:
        source_title = source['sourcetitle-abbrev'] if 'sourcetitle-abbrev' in source else None
    return source_title


def get_source_type(json_source):
    source = get_source(json_source)
    type = None
    if source:
        type = source['@type'] if '@type' in source else None
    return type


def get_source_country_code(json_source):
    source = get_source(json_source)
    code = None
    if source:
        code = source['@country'] if '@country' in source else None
    return code


def get_source_publisher_name(json_source):
    publisher = None
    publisher_json = get_source(json_source)
    if publisher_json and 'publisher' in publisher_json and 'publishername' in publisher_json['publisher']:
        publisher = publisher_json['publisher']['publishername']
    return publisher


def get_source_srcid(json_source):
    source = get_source(json_source)
    id = None
    if source:
        id = source['@srcid'] if '@srcid' in source else None
    return id


def get_source_issn(json_source, standard_format = False):
    issn = None
    issn_json = get_source(json_source)
    if not 'issn' in issn_json:
        return None
    issn_json = issn_json['issn']
    if isinstance(issn_json, str):
        issn = str(issn_json)
        if standard_format:
            issn = issn[:4] + "-" + issn[4:]
        return issn
    if not isinstance(issn_json, list):
        issn_json = [issn_json]
    for o in issn_json:
        if o['@type'] == 'print':
            issn = o['$']
    if isinstance(issn, tuple):
        issn = issn[0]
    if issn and standard_format:
        issn = issn[:4] + "-" + issn[4:] #if issn else None
    return issn


def get_source_eissn(json_source, standard_format = False):
    eissn = None
    issn_json = get_source(json_source)
    if not 'issn' in issn_json:
        return None
    issn_json = issn_json['issn']
    if isinstance(issn_json, str):
        eissn = str(issn_json)
        if standard_format:
            eissn = eissn[:4] + "-" + eissn[4:]
        return eissn
    if not isinstance(issn_json, list):
        issn_json = [issn_json]
    for o in issn_json:
        if o['@type'] == 'electronic':
            eissn = o['$']
    if isinstance(eissn, tuple):
        eissn = eissn[0]
    if eissn and standard_format:
        eissn = eissn[:4] + "-" + eissn[4:]
    return eissn


def get_citedby_count(json_source):
    coredata = __coredata(json_source)
    return coredata['citedby-count'] if 'citedby-count' in coredata else 0


def __coredata(json_source):
    return json_source['abstracts-retrieval-response']['coredata']
