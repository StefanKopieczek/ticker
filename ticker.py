import requests
import re
import sys

from bs4 import BeautifulSoup

import ticker_api


def company(symbol):
    result = {}
    r = requests.get(ticker_api.COMPANY['url'] % symbol)
    data = r.text
    soup = BeautifulSoup(data)
    tables = soup.find_all(id=ticker_api.COMPANY['div_id'])

    for table in tables:
        for row in table.find_all('tr'):
            header, cell = row.th.get_text(), row.td.get_text()
            field, value = __parse_company_row(header, cell)
            result[field] = value

    if 'bid' in result:
        # Split out e.g. "307.52 x 100" into two separate fields.
        result['bid'], result['bid_volume'] = __parse_bid_ask(result['bid'])

    if 'ask' in result:
        # Split out e.g. "307.52 x 100" into two separate fields.
        result['ask'], result['ask_volume'] = __parse_bid_ask(result['ask'])

    final = {}
    for field, value in result.iteritems():
        if field in ticker_api.COMPANY['field_name_map']:
            # Apply overrides to remap the scraped key names; e.g. we map
            # 'wk_range' to 'week_range'.
            field = ticker_api.COMPANY['field_name_map'][field]

        if field in ticker_api.COMPANY['parsers']:
            # If we know how to parse the value from a string into a native
            # type, do so (e.g. convert share prices to floats).
            try:
                value = ticker_api.COMPANY['parsers'][field](value)
            except ValueError:
                value = None

        final[field] = value

    return final


def __parse_company_row(field, value):
    field = field.lower()
    field = re.sub('[^a-z0-9_\s]+', '', field)
    field = re.sub('\s+', '_', field)
    return (field, value)


def __parse_bid_ask(full_str):
    value, volume = full_str.split("x")
    value = value.strip()
    volume = volume.strip()
    return (value, volume)

if __name__ == "__main__":
    print company(sys.argv[1])
