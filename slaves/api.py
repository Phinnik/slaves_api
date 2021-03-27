import time
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

import requests

from slaves.exceptions import SlaveIsLockedError
from slaves.exceptions import UnknownMethodError
from slaves.responses import ResponseBase
from slaves.responses import ResponseBuyFetter
from slaves.responses import ResponseBuySlave
from slaves.responses import ResponseJobSlave
from slaves.responses import ResponseSaleSlave
from slaves.responses import ResponseSlaveList
from slaves.responses import ResponseStart
from slaves.responses import ResponseTopUsers
from slaves.responses import ResponseUser
from slaves.responses import ResponseUsers


@dataclass
class Api:
    authorization: str
    url_base: str = 'https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/'
    
    def __post_init__(self):
        self._headers = {
            'Host': 'pixel.w84.vkforms.ru',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'authorization': self.authorization,
            'sec-ch-ua-mobile': '?1',
            'save-data': 'on',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; Redmi 8A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36',
            'origin': 'https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com/',
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8',

        }
    
    def _call(
        self,
        response_type: Type[ResponseBase],
        json: Optional[Dict[str, Union[int, str, List[int]]]] = None,
        params: Optional[Dict[str, int]] = None,
    ):
        api_method: str = response_type.__name__
        api_method_without_response: str = api_method.replace('Response', '')
        api_method_without_capital_letter: str = api_method_without_response[0].lower() + api_method_without_response[1:]
        
        api_method_clean: str = api_method_without_capital_letter
        if api_method_clean == 'users':
            api_method_clean = 'user'
        
        url: str = self.url_base + api_method_clean
        print('url', url)
        
        if bool(json) == bool(params):
            raise UnknownMethodError()
        elif json is not None and params is None:
            response = requests.post(url=url, headers=self._headers, json=json)
        else:
            response = requests.get(url=url, headers=self._headers, params=params)
        
        try:
            response_json: Dict[str, Any] = response.json()
        except JSONDecodeError as e:
            print(response.text)
            raise e
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            time.sleep(2)
            return self._call(response_type=response_type, json=json, params=params)
        if 'error' in response_json and response_json['error'].get('code') == 422:
            raise SlaveIsLockedError()
        return response_type(**response_json)
    
    def start(self) -> ResponseStart:
        """
        Возвращает стартовую информацию
        """
        return self._call(
            response_type=ResponseStart,
        )
    
    def user_get(self, user_id: int) -> ResponseUser:
        return self._call(
            response_type=ResponseUser,
            params={'id': user_id},
        )
    
    def users_get(self, user_ids: List[int]) -> ResponseUsers:
        """
        Возвращает информацию о пользователях
        
        :param user_ids: список идентификаторов пользователей
        """
        return self._call(
            response_type=ResponseUsers,
            json={'ids': user_ids},
        )
    
    def slave_list(self, user_id: int) -> ResponseSlaveList:
        """
        Возвращает список рабов
        
        :param user_id: идентификатор пользователя
        """
        return self._call(
            response_type=ResponseSlaveList,
            params={'id': user_id},
        )
    
    def buy_slave(self, user_id: int) -> ResponseBuySlave:
        """
        Покупает раба
        
        :param user_id: идентификатор пользователя
        """
        return self._call(
            response_type=ResponseBuySlave,
            json={'slave_id': user_id}
        )

    def buy_fetter(self, slave_id: int) -> responses.BuyFetterResponse:
        """
        Покупает оковы для раба
        
        :param slave_id: идентификатор раба
        """
        return self._call(
            response_type=ResponseBuyFetter,
            json={'slave_id': slave_id},
        )
    
    def job_slave(self, name: str, slave_id: int) -> ResponseJobSlave:
        """
        Отправляет раба на работу
        
        :param name: название работы
        :param slave_id: идентификатор раба
        """
        return self._call(
            response_type=ResponseJobSlave,
            json={'name': name, 'slave_id': slave_id},
        )
    
    def top_users(self) -> ResponseTopUsers:
        return self._call(
            response_type=ResponseTopUsers,
        )
