import requests
from typing import List
from slaves import responses
from slaves import exceptions
import json
import time


class Api:
    def __init__(self, authorization: str):
        self._authorization = authorization

    def _call(self, method: str, api_method: str, response_type, payload=None):
        url = 'https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/' + api_method
        payload = payload or dict()
        headers = {
            "authorization": self._authorization,
        }
        if method == 'post':
            response = requests.post(url, headers=headers, json=payload)
        else:
            response = requests.get(url, headers=headers, params=payload)
        try:
            response = response.json()
        except json.decoder.JSONDecodeError as e:
            print(response.text)
            raise e
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            time.sleep(2)
            return self._call(method, api_method, response_type, payload)
        if 'error' in response:
            if response['error'].get('code') == 422:
                raise exceptions.SlaveIsLocked
        return response_type(**response)

    def start(self) -> responses.StartResponse:
        """
        Возвращает стартовую информацию
        """
        method = 'get'
        api_method = 'start'
        response_type = responses.StartResponse
        payload = None
        return self._call(method, api_method, response_type, payload)

    def user_get(self, user_id: int) -> responses.UserGetResponse:
        method = 'get'
        api_method = 'user'
        response_type = responses.UserGetResponse
        payload = {'id': user_id}
        return self._call(method, api_method, response_type, payload)

    def users_get(self, user_ids: List[int]) -> responses.UsersGetResponse:
        """
        Возвращает информацию о пользователях

        :param user_ids: список идентификаторов пользователей
        """
        method = 'post'
        api_method = 'user'
        response_type = responses.UsersGetResponse
        payload = {'ids': user_ids}
        return self._call(method, api_method, response_type, payload)

    def slave_list(self, user_id: int) -> responses.SlaveListResponse:
        """
        Возвращает список рабов

        :param user_id: идентификатор пользователя
        """
        method = 'get'
        api_method = 'slaveList'
        response_type = responses.SlaveListResponse
        payload = {'id': user_id}
        return self._call(method, api_method, response_type, payload)

    def buy_slave(self, user_id) -> responses.BuySlaveResponse:
        """
        Покупает раба

        :param user_id: идентификатор пользователя
        """
        method = 'post'
        api_method = 'buySlave'
        response_type = responses.BuySlaveResponse
        payload = {'slave_id': user_id}
        return self._call(method, api_method, response_type, payload)

    def sale_slave(self, user_id) -> responses.BuySlaveResponse:
        """
        Продает раба

        :param user_id: идентификатор пользователя
        """
        method = 'post'
        api_method = 'saleSlave'
        response_type = responses.BuySlaveResponse
        payload = {'slave_id': user_id}
        return self._call(method, api_method, response_type, payload)

    def buy_fetter(self, slave_id: int) -> responses.BuyFetterResponse:
        """
        Покупает оковы для раба

        :param slave_id: идентификатор раба
        """
        method = 'post'
        api_method = 'buyFetter'
        response_type = responses.BuyFetterResponse
        payload = {'slave_id': slave_id}
        return self._call(method, api_method, response_type, payload)

    def job_slave(self, name: str, slave_id: int) -> responses.JobSlaveResponse:
        """
        Отправляет раба на работу

        :param name: название работы
        :param slave_id: идентификатор раба
        """
        method = 'post'
        api_method = 'jobSlave'
        response_type = responses.JobSlaveResponse
        payload = {'name': name, 'slave_id': slave_id}
        return self._call(method, api_method, response_type, payload)

    def top_users(self) -> responses.TopUsersResponse:
        method = 'get'
        api_method = 'topUsers'
        response_type = responses.TopUsersResponse
        payload = None
        return self._call(method, api_method, response_type, payload)
