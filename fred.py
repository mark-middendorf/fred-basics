import requests
import json
import sys


class FredAPI:
    """Class that wraps FRED api calls

    initialize with an API key from FRED

    methods:
        category_api_str
        category_children_api_str
        category_series_api_str
        series_api_str
        series_obs_api_str
        tags_api_str
        api_request (static)
    """

    def __init__(self, api_key) -> None:
        self.api_key = api_key

    def category_api_str(self, category_id: int) -> str:
        """
        request string for api category call
        :param category_id: FRED category_id
        :return: FRED request string
        """
        request_str = (f"https://api.stlouisfed.org/fred/category?"
                       f"category_id={category_id}&api_key={self.api_key}&"
                       f"file_type=json")
        return request_str

    def category_children_api_str(self, category_id: int) -> str:
        """
        request string for api category/children call
        :param category_id: FRED category_id
        :return: FRED request string
        """
        request_str = (f"https://api.stlouisfed.org/fred/category/children?"
                       f"category_id={category_id}&api_key={self.api_key}&"
                       f"file_type=json")
        return request_str

    def category_series_api_str(self, category_id: int) -> str:
        """
        request string for api category/series call
        :param category_id: FRED category_id
        :return: FRED request string
        """
        request_str = (f"https://api.stlouisfed.org/fred/category/series?"
                       f"category_id={category_id}&api_key={self.api_key}&"
                       f"file_type=json")
        return request_str

    def category_series_paginator_api_str(self, category_id: int,
                                          offset: int) -> str:
        """
        request string for api category/series call
        :param category_id: FRED category_id
        :return: FRED request string
        """
        request_str = (f"https://api.stlouisfed.org/fred/category/series?"
                       f"category_id={category_id}&api_key={self.api_key}&"
                       f"file_type=json&offset={offset}")
        return request_str

    def series_api_str(self, series_id: str) -> str:
        """
        request string for api series call
        :param series_id: FRED series id as a string
        :return: FRED request string
        """
        request_str = (f"https://api.stlouisfed.org/fred/series?"
                       f"series_id={series_id}&api_key={self.api_key}&"
                       f"file_type=json")
        return request_str

    def series_category_api_str(self, series_id: str) -> str:
        """
        request string for api series/category call
        :param series_id: FRED series id as a string
        :return: FRED request string
        """
        request_str = (f"https://api.stlouisfed.org/fred/series/categories?"
                       f"series_id={series_id}&api_key={self.api_key}&"
                       f"file_type=json")
        return request_str

    def series_obs_api_str(self, series_id: str) -> str:
        """
        request string for api observation call
        :param series_id: FRED series id as a string
        :return: FRED request string
        """
        request_str = (f"https://api.stlouisfed.org/fred/series/observations?"
                       f"series_id={series_id}&api_key={self.api_key}&"
                       f"file_type=json")
        return request_str

    def tags_api_str(self) -> str:
        """
        request string for api observation call
        :return: FRED request string
        """
        request_str = (f"https://api.stlouisfed.org/fred/tags?"
                       f"api_key={self.api_key}&"
                       f"file_type=json")
        return request_str

    @staticmethod
    def api_request(api_str: str):
        """
        request.get() results transformed to JSON object
        :param api_str: series api string
        :return: json payload
        """
        try:
            response = requests.get(api_str)
            response.raise_for_status()
            j = json.loads(response.content)
            return j
        except requests.exceptions.RequestException as e:
            print('Request failed with exception:', e, file=sys.stderr)
            return None