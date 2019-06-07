# pylint: disable=missing-docstring
import os


SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_CHANNEL_ID = os.environ["SLACK_CHANNEL_ID"]
GOOGLE_FORM_URL = os.environ["GOOGLE_FORM_URL"]


class AppSettings:  # pylint: disable=too-few-public-methods
    DEBUG = False
