#!/usr/bin/env python3

import logging
import requests
from requests.exceptions import HTTPError

from .back_config import *


class DataProvider(object):
    """
    Class for providing data to the bot from backend. Uses requests to get and post data.
    """

    def __init__(self) -> None:
        logging.info("Creating date provider")

        self.topics = DataProvider.__get_topics()
        self.topic_emojis = {}

        for t in self.topics.values():
            self.topic_emojis[t[EMOJI_ACCESSOR]] = t['id']

    def __get_topics():
        r = DataProvider.__make_get(BACKEND_BASE_URL + TOPICS_URL)
        if r is None:
            raise ValueError("Couldn't get data from backend.")
        gotted_topics = r.json()
        topics = {}
        for t in gotted_topics:
            topics[t['id']] = t
        return topics

    def get_questions(amount, topic):
        r = DataProvider.__make_get(
            BACKEND_BASE_URL + QUESTIONS_URL + f"?{TOPIC_QUERY}={topic}&{AMOUNT_QUERY}={amount}")
        if r is None:
            raise ValueError("Couldn't get data from backend.")
        return r.json()

    def __make_get(url, headers={}):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            logging.info(f"{http_error} in get request to {url}.")
        except Exception as err:
            logging.info(f"Error {err} occured in request to {url}.")
        else:
            return response
