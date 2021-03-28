import sys

sys.path.append('..')

import unittest
import json
from slaves import Api
from slaves import responses
from slaves import exceptions


class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        with open('test_config.json', 'r') as f:
            config = json.load(f)
            self.api = Api(config['authorization'])
            self.bad_api = Api('BAD AUTHORIZATION STRING')

    def test_start(self):
        start_response = self.api.start()
        self.assertIsInstance(start_response, responses.StartResponse)

    def test_user_get(self):
        user_get_response = self.api.user_get(1)
        self.assertIsInstance(user_get_response, responses.UserGetResponse)

    def test_users_get(self):
        users_get_response = self.api.users_get([1])
        self.assertIsInstance(users_get_response, responses.UsersGetResponse)

    def test_slave_list(self):
        slave_list_response = self.api.slave_list(1)
        self.assertIsInstance(slave_list_response, responses.SlaveListResponse)

    def test_buy_slave(self):
        pass

    def test_sale_slave(self):
        pass

    def test_buy_fetter(self):
        pass

    def test_job_slave(self):
        pass

    def test_top_users(self):
        top_users_response = self.api.top_users()
        self.assertIsInstance(top_users_response, responses.TopUsersResponse)

    def test_bad_authorization_exception(self):
        self.assertRaises(exceptions.InvalidSign, self.bad_api.start)
