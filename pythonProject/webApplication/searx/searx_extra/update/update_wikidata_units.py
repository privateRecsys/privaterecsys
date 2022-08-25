#!/usr/bin/env python

import json
import collections

# set path
from os.path import join

from searx import searx_dir
from searx.engines.wikidata import send_wikidata_query


# the response contains duplicate ?item with the different ?symbol
# "ORDER BY ?item DESC(?rank) ?symbol" provides a deterministic result
# even if a ?item has different ?symbol of the same rank.
# A deterministic result 
# see:
# * https://www.wikidata.org/wiki/Help:Ranking
# * https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format ("Statement representation" section)
# * https://w.wiki/32BT
#   see the result for https://www.wikidata.org/wiki/Q11582
#   there are multiple symbols the same rank
SARQL_REQUEST = """
SELECT DISTINCT ?item ?symbol
WHERE
{
  ?item wdt:P31/wdt:P279 wd:Q47574 .
  ?item p:P5061 ?symbolP .
  ?symbolP ps:P5061 ?symbol ;
           wikibase:rank ?rank .
  FILTER(LANG(?symbol) = "en").
}
ORDER BY ?item DESC(?rank) ?symbol
"""


def get_data():
    results = collections.OrderedDict()
    response = send_wikidata_query(SARQL_REQUEST)
    for unit in response['results']['bindings']:
        name = unit['item']['value'].replace('http://www.wikidata.org/entity/', '')
        unit = unit['symbol']['value']
        if name not in results:
            # ignore duplicate: always use the first one
            results[name] = unit
    return results


def get_wikidata_units_filename():
    return join(join(searx_dir, "data"), "wikidata_units.json")


with open(get_wikidata_units_filename(), 'w') as f:
    json.dump(get_data(), f, indent=4, ensure_ascii=False)
