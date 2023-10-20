import logging
from typing import List

import requests

from unione.exceptions.unione_exception import UniOneException

logger = logging.getLogger('unione')


class UniOne:
    def __init__(self, api_key: str):
        self._api_url = 'https://eu1.unione.io/ru/transactional/api/v1/'

        self._headers = {
            'X-API-KEY': api_key
        }

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

    def send_emails(self, recipients: List[dict], from_email: str, from_name: str, subject: str = None,
                    body_html: str = None,
                    **kwargs) -> dict:
        """
        sending a message to multiple recipients
        recipients - [
              {
                "email": "user@example.com",
                "substitutions": {
                  "CustomerId": 12452,
                  "to_name": "John Smith"
                },
                "metadata": {
                  "campaign_id": "email61324",
                  "customer_hash": "b253ac7"
                }
              }
            ]
        :return:
        """
        if not body_html and not kwargs.get('template_id'):
            raise UniOneException('body_html or template_id is required')

        params = {
            'recipients': recipients,
            'from_email': from_email,
            'from_name': from_name
        }
        if subject:
            params['subject'] = subject
        if body_html:
            params['body'] = {
                'html': body_html
            }
        else:
            params['template_id'] = kwargs['template_id']

        return self._request('email/send', params)

    def _request(self, method: str, params: dict) -> dict:
        data = {'message': params}
        try:
            r = requests.post(f'{self._api_url}{method}.json', json=data, headers=self._headers, timeout=3)
        except requests.exceptions.RequestException as e:
            logger.exception(e)
            raise UniOneException(f'request error {e}')
        if r.status_code != 200:
            logger.error(f'request error {r.status_code} {r.text}')
            raise UniOneException(f'request error')
        return r.json()
