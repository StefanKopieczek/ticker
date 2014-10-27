import requests
import re

from itertools import izip
from bs4 import BeautifulSoup

import ticker_api


class ParseError(Exception):
    pass


def company_query(symbols, fields=None):
    results = {}

    query_fields = None
    derived_fields = None
    if fields is None:
        query_fields = ticker_api.COMPANY['query_fields'].keys()
        derived_fields = ticker_api.COMPANY['derived_fields'].keys()
        fields = query_fields + derived_fields
    else:
        query_fields = [field for field in fields
                        if field in ticker_api.COMPANY['query_fields']]

        derived_fields = [field for field in fields
                          if field in ticker_api.COMPANY['derived_fields']]

    # Ensure that whenever we request a derived stat, we also request the stats
    # on which it depends.
    queried_fields = set(query_fields)
    for field in derived_fields:
        required = ticker_api.COMPANY['derived_fields'][field].prerequisites
        for prerequisite in required:
            if prerequisite not in queried_fields:
                queried_fields.add(prerequisite)

    # Build the URL parameters for the query.
    params = {
        's': ' '.join(symbols),
        'f': ''.join((ticker_api.COMPANY['query_fields'][field].key
                      for field in query_fields))
    }

    # Obtain the CSV data from Yahoo. Split by company and field, producing:
    # {company_symbol : {stat_name : stat_value}}
    r = requests.get(ticker_api.COMPANY['url'], params=params, stream=True)
    lines = (line.strip() for line in r.text.split('\n') if line is not u'')
    for idx, line in enumerate(lines):
        results[symbols[idx]] = {symbol: value.strip() for (symbol, value) in
                                 izip(fields, line.split(','))}

    requested_fields = set(fields)
    hidden_fields = requested_fields - queried_fields

    # Parse the stat_values out of their string representations into the
    # correct formats.
    for company, stats in results.iteritems():
        for field, value in stats.iteritems():
            if field in ticker_api.COMPANY['query_fields']:
                stats[field] = ticker_api.COMPANY['query_fields'][field].parser(
                    value)

        # Calculate any derived values based on the query results.
        for field in derived_fields:
            stats[field] = None
            stat = ticker_api.COMPANY['derived_fields'][field]
            for prerequisite in stat.prerequisites:
                if stats[prerequisite] is None:
                    break
            else:
                stats[field] = stat(stats)

        # Remove any stats needed for a derived value which the user did not
        # originally request.
        for field in hidden_fields:
            del stats[field]

    # Remove any stats needed for a derived value which the user did not
    # originally request.
    unrequested = set(stats.keys()) - (queried_fields | set(derived_fields))
    for field in unrequested:
        del stats[field]

    return results


def index(name):
    result = {}

    summary_request = requests.get(ticker_api.INDEX['summary_url'] % name)
    summary_data = summary_request.text
    summary = BeautifulSoup(summary_data)

    summary_block = None
    try:
        summary_block = summary.find_all(
            id=ticker_api.INDEX['summary_div_id'])[0]
    except IndexError as e:
        raise ParseError(e)

    summary_tables = summary_block.find_all('table')

    for table in summary_tables:
        for row in table.find_all('tr'):
            header, cell = row.th.get_text(), row.td.get_text()
            field, value = __parse_summary_row(header, cell)
            result[field] = value

    return result


def __parse_summary_row(field, value):
    field = field.lower()
    field = re.sub('[^a-z0-9_\s]+', '', field)
    field = re.sub('\s+', '_', field)
    return (field, value)


def __parse_bid_ask(full_str):
    value, size = full_str.split("x")
    value = value.strip()
    size = size.strip()
    return (value, size)


def __parse_currency_block(currency_str):
    match = re.search(r"Currency in ([^\.]+)", currency_str)
    if match:
        return match.group(1).lower()
    else:
        return None
