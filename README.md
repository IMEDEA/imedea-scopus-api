# imedea-scopus-api
Python2 implementation for SCOPUS API.
This library works by retrieving data in JSON format.

## Installation
Install from github repository

`pip2 install git+https://github.com/IMEDEA/imedea-scopus-api`

or upgrade adding --upgrade

`pip2 install --upgrade git+https://github.com/IMEDEA/imedea-scopus-api`
## Example usage
Use of and IDE with autocomplete capabilities such as PyCharm is recommended.

```python
import json
from imedea_scopus_api import query, elsclient, abstract_tools, affiliation_tools

if __name__ == '__main__':

    # Query object to search for data
    q = query.Query()
    q.author('Balle')
    q.and_()
    q.affiliation_id('60017294')
    q.and_()
    q.subject_area(q.SBJ_AREA_PHYSICS_AND_ASTRONOMY, q.SBJ_AREA_EARTH_AND_PLANETARY_SCIENCES)
    q.and_()
    q.publication_year('>', '2011') # <,=,> are ok. Not allowed by scopus >=, <=
    q.and_()
    q.publication_year('<', '2014')
    q.and_()
    q.document_type(q.DOC_TYPE_ARTICLE, #Ors here...
                    q.DOC_TYPE_LETTER,
                    q.DOC_TYPE_REVIEW,
                    q.DOC_TYPE_EDITORIAL,
                    q.DOC_TYPE_NOTE)
    q.and_()
    q.source_type(q.SRC_TYPE_JOURNAL)
    # ...and many more q.methods, see query.py
    # q.or_() q.open_par() q.close_par() allowed too
    # Many query rules (not all) can be set with many values separated by commas,
    # in this case "ors" are applied q.author('Balle', 'Vizoso'....)
    # its the same as q.author('Balle').or_().author('Vizoso')...
    # Note q returns self, so rules can be set as q.rule1.rule2...
    
    # Your center credentials                
    api = 'your_api_key_here'
    choice = 'your_choice_if_any_here'
    # If working with a ssh tunnel to an allowed ip
    # set to None or do not user parameter if not necessary
    tunnel_url = 'localhost'
    tunnel_port = 1234

    # Main elsclient object construction
    ec = elsclient.ELSClient(api=api, choice=choice, tunnel_url=tunnel_url, tunnel_port=tunnel_port)

    # Search of data via query object created before with many configurable
    # parameters (default are ok to use too)
    search_result = ec.scopus_search(
        q,
        suppress_nav_links= True,
        view = ec.VIEW_COMPLETE,
        # date="2000-2010", # If you want the date here
        start=0,
        count=25,
        sort=[ec.SORT_PUBLICATION_YEAR_ASC, ec.SORT_PUBLICATION_NAME_ASC, ec.SORT_CREATOR_DESC]
    )
    
    # Print all results
    print json.dumps(search_result)
    
    # We could loop over publications with
    if search_result:
        for pub in search_result['search-results']['entry']:
            print json.dumps(pub)
    
    # Another way to get data is first getting all identifiers (not start
    # and not count needed here, it's done internally)
    scopus_identifiers = ec.get_all_identifiers(q) # The same query

    for scopus_identifier in scopus_identifiers:
        # Now we can retrieve abstract with
        abstract = ec.get_abstract_by_scopus_id(scopus_identifier)
        print json.dumps(abstract)
        #We have abstract tools too to get particular information:
        print abstract_tools.get_title(abstract)
        print abstract_tools.get_citedby_count(abstract)
        print abstract_tools.get_authors(abstract)
        print abstract_tools.get_doi(abstract)
        # ... and many more methods to retrieve info from abstract

    # We can retrieve affiliation info too with
    affiliation = ec.get_affiliation_by_affiliation_id('aff_id_here')
    # or
    # affiliation = ec.get_affiliation_by_eid('aff_eid_here')
    # And affiliations tools
    print affiliation_tools.get_name(affiliation)
    print affiliation_tools.get_city(affiliation) # and so on
    # you can handle affiliation json by your own too
    print json.dumps(affiliation)
    
    # Author data
    author = ec.get_author_by_author_id('author_id_here')
    # or author = ec.get_author_by_eid('author_eid_here')
    # or author=ec.get_author_by_orcid('author_orcid_here')
    # NO author tools yet :( author field access must be done "by hand"
    print json.dumps(author)
    
    # Journal data
    journal = ec.get_journal_metrics('issn_here', initial_year=1999, end_year=2002)
    # No journal tools neither :(
    print json.dumps(journal)
```
