import logging

import requests

from unione.exceptions.unione_exception import UniOneException

logger = logging.getLogger('unione')


class UniOne:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._api_url = 'https://eu1.unione.io/ru/transactional/api/v1/'

    def send_email(self, to_email: str, from_email: str, from_name: str, subject: str, body_html: str, **kwargs):
        params = {
            'recipients': [
                {
                    'email': to_email
                }
            ],
            'body': {
                'html': body_html
            },
            'subject': subject,
            'from_email': from_email,
            'from_name': from_name
        }

        return self._request('email/send', params)

    def _request(self, method: str, params: dict) -> dict:
        headers = {
            'X-API-KEY': self._api_key,
            'Content-Type': 'application/json'
        }
        data = {'message': params}
        r = requests.post(f'{self._api_url}{method}.json', json=data, headers=headers)
        if r.status_code != 200:
            logger.error(f'request error {r.status_code} {r.text}')
            raise UniOneException(f'request error')
        return r.json()