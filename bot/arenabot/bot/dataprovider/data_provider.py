#!/usr/bin/env python3

import logging
import time
import requests
from requests.exceptions import HTTPError

from .back_config import *


class DataProvider(object):
    """
    Class for providing data to the bot from backend. Uses requests to get and post data.
    """

    def __init__(self, back_url) -> None:
        logging.info("Creating date provider")

        self.topic_emojis = {}
        self.backend_base_url = back_url

        t0 = time.time()
        self.topics = None
        while time.time() - t0 < BACKEND_CONNECTION_TIME:
            try:
                self.topics = self._get_topics()
                break
            except HTTPError:
                logging.info(
                    "Couldn't establish connection with backend. Trying again")
            time.sleep(SLEEPING_TIME_CONNECTION)
        if not self.topics:
            raise HTTPError(HTTP_ERROR_MESSAGE)

        for t in self.topics.values():
            self.topic_emojis[t[EMOJI_ACCESSOR]] = t['id']

    def _get_topics(self):
        r = DataProvider._make_get(self.backend_base_url + TOPICS_URL)
        if r is None:
            raise HTTPError(HTTP_ERROR_MESSAGE)
        gotted_topics = r.json()
        topics = {}
        for t in gotted_topics:
            topics[t['id']] = t
        return topics

    def get_questions(self, amount, topic):
        r = DataProvider._make_get(
            self.backend_base_url + QUESTIONS_URL + f"?{TOPIC_QUERY}={topic}&{AMOUNT_QUERY}={amount}")
        if r is None:
            raise HTTPError(HTTP_ERROR_MESSAGE)
        return r.json()

    def get_player_sessions(self, uid, amount=10):
        r = DataProvider._make_get(
            self.backend_base_url + PLAYERS_URL +
            f"/{uid}" + f"?{AMOUNT_QUERY}={amount}"
        )
        if r is None:
            raise HTTPError(HTTP_ERROR_MESSAGE)
        if r.status_code == 204:
            raise ValueError

        return r.json()

    def get_session_info(self, sid):
        r = DataProvider._make_get(
            self.backend_base_url + SESSIONS_URL + f"?{ID_QUERY}={sid}"
        )
        if r is None:
            raise HTTPError(HTTP_ERROR_MESSAGE)
        if r.status_code == 204:
            raise ValueError
        return r.json()

    def send_session_info(self, data):
        r = DataProvider._make_post(
            self.backend_base_url + SESSIONS_URL, data=data)  # another one

    @ staticmethod
    def _make_get(url, headers={}):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            logging.info(f"{http_error} in get request to {url}.")
        except Exception as err:
            logging.info(f"Error {err} occured in request to {url}.")
        else:
            return response

    @ staticmethod
    def _make_post(url, headers={}, data={}):
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
        except HTTPError as http_error:
            logging.info(f"{http_error} in post request to {url}.")
        except Exception as err:
            logging.info(f"Error {err} occured in request to {url}.")
        else:
            return response

    def get_topic_str(self, tid):
        return self.topics[tid][NAME_ACCESSOR] + self.topics[tid][EMOJI_ACCESSOR]
