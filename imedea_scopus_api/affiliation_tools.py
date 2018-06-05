

def get_root(json_source):
    return json_source['affiliation-retrieval-response']


def get_name(json_source):
    return get_root(json_source)['affiliation-name']


def get_city(json_source):
    root = get_root(json_source)
    return root['city'] if 'city' in root else None


def get_country_iso3_code(json_source):
    return get_root(json_source)['institution-profile']['address']['@country']


