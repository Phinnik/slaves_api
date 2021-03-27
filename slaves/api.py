import time
from json.decoder import JSONDecodeError
import typing

import requests

from slaves import exceptions
from slaves import responses


class Api:
    def __init__(self, authorization: str) -> None:
        self._authorization: str = authorization
        self._headers = {
            'Host': 'pixel.w84.vkforms.ru',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'authorization': self._authorization,
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
        self._url_base: str = 'https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/'
    
    def _call(
        self,
        response_type: typing.Type[responses.ResponseBase],
        json: typing.Optional[typing.Dict[str, typing.Union[int, str, typing.List[int]]]] = None,
        params: typing.Optional[typing.Dict[str, int]] = None,
    ):
        api_method: str = response_type.__name__
        api_method_without_response: str = api_method.replace('Response', '')
        api_method_without_capital_letter: str = api_method_without_response[0].lower() + api_method_without_response[1:]
        
        api_method_clean: str = api_method_without_capital_letter
        if api_method_clean == 'users':
            api_method_clean = 'user'
        
        url: str = self._url_base + api_method_clean
        
        if bool(json) == bool(params):
            raise exceptions.UnknownMethodError()
        elif json is not None and params is None:
            response = requests.post(url=url, headers=self._headers, json=json)
        else:
            response = requests.get(url=url, headers=self._headers, params=params)
        
        try:
            response_json: typing.Dict[str, typing.Any] = response.json()
        except JSONDecodeError as e:
            print(response.text)
            raise e
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            time.sleep(2)
            return self._call(response_type=response_type, json=json, params=params)
        if 'error' in response_json and response_json['error'].get('code') == 422:
            raise exceptions.SlaveIsLockedError()
        return response_type(**response_json)
    
    def start(self) -> responses.ResponseStart:
        """
        Возвращает стартовую информацию
        """
        return self._call(
            response_type=responses.ResponseStart,
        )
    
    def user_get(self, user_id: int) -> responses.ResponseUser:
        return self._call(
            response_type=responses.ResponseUser,
            params={'id': user_id},
        )
    
    def users_get(self, user_ids: typing.List[int]) -> responses.ResponseUsers:
        """
        Возвращает информацию о пользователях

        :param user_ids: список идентификаторов пользователей
        """
        return self._call(
            response_type=responses.ResponseUsers,
            json={'ids': user_ids},
        )
    
    def slave_list(self, user_id: int) -> responses.ResponseSlaveList:
        """
        Возвращает список рабов

        :param user_id: идентификатор пользователя
        """
        return self._call(
            response_type=responses.ResponseSlaveList,
            params={'id': user_id},
        )
    
    def buy_slave(self, user_id: int) -> responses.ResponseBuySlave:
        """
        Покупает раба

        :param user_id: идентификатор пользователя
        """
        return self._call(
            response_type=responses.ResponseBuySlave,
            json={'slave_id': user_id}
        )
    
    def sale_slave(self, user_id) -> responses.ResponseSaleSlave:
        """
        Продает раба

        :param user_id: идентификатор пользователя
        """
        return self._call(
            response_type=responses.ResponseSaleSlave,
            json={'slave_id': user_id},
        )
    
    def buy_fetter(self, slave_id: int) -> responses.ResponseBuyFetter:
        """
        Покупает оковы для раба

        :param slave_id: идентификатор раба
        """
        return self._call(
            response_type=responses.ResponseBuyFetter,
            json={'slave_id': slave_id},
        )
    
    def job_slave(self, name: str, slave_id: int) -> responses.ResponseJobSlave:
        """
        Отправляет раба на работу

        :param name: название работы
        :param slave_id: идентификатор раба
        """
        return self._call(
            response_type=responses.ResponseJobSlave,
            json={'name': name, 'slave_id': slave_id},
        )
    
    def top_users(self) -> responses.ResponseTopUsers:
        return self._call(
            response_type=responses.ResponseTopUsers,
        )
