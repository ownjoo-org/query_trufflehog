# pylint: disable=missing-docstring
import argparse
import json
from sys import stderr

from typing import Optional, Union
from requests import Session, Response, HTTPError


def main(
        domain: str,
        client_id: str,
        client_secret: str,
        proxies: Optional[dict] = None,
) -> Union[None, str, list, dict]:
    session = Session()
    session.proxies = proxies or {}

    headers: dict = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; Charset=UTF-8',
        'X-Thog-Key': client_id,
        'X-Thog-Secret': client_secret,
    }
    session.headers = headers

    params: dict = {
        'page': 1,
        'page_size': 250,
    }
    exception_message: str = 'Exception on page {page}: {exception}: {response}'
    errors_count: int = 0
    while True and errors_count < 5:
        try:
            resp_query: Response = session.get(
                url=f'https://{domain}/api/v2/secret_locations',
                params=params,
                headers=headers,
                proxies=proxies,
            )
            resp_query.raise_for_status()
            data_query: dict = resp_query.json()
            resources: list = data_query.get('results')
            yield from resources
            params['page'] += 1
            if len(resources) < 250:
                break
        except HTTPError as exc_http:
            errors_count += 1
            print(
                exception_message.format(
                    page=params.get('page'),
                    exception=exc_http,
                    response=exc_http.response.text,
                ),
                file=stderr,
            )
        except Exception as exc_query:
            errors_count += 1
            print(
                exception_message.format(
                    page=params.get('page'),
                    exception=exc_query,
                    response='',
                ),
                file=stderr,
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--domain',
        type=str,
        required=True,
        help="The FQDN/IP for your truffelhog host (not full URL)",
    )
    parser.add_argument(
        '--client_id',
        default=None,
        type=str,
        required=True,
        help='The API key ID to authenticate with',
    )
    parser.add_argument(
        '--client_secret',
        default=None,
        type=str,
        required=True,
        help='The secret for the API key',
    )
    parser.add_argument(
        '--proxies',
        type=str,
        required=False,
        help="JSON structure specifying 'http' and 'https' proxy URLs",
    )

    args = parser.parse_args()

    proxies: Optional[dict] = None
    if proxies:
        try:
            proxies: dict = json.loads(args.proxies)
        except Exception as exc_proxies:
            print(f'WARNING: failure parsing proxies: {exc_proxies}: proxies provided: {proxies}')

    for result in main(
        domain=args.domain,
        client_id=args.client_id,
        client_secret=args.client_secret,
        proxies=proxies,
    ):
        if isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps({"invalid_result": str(result)}, indent=2))
    else:
        print('No results found')
