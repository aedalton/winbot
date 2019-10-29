import logging

from winbot.app import AppFactory


logger = logging.getLogger(__name__)

logger.info("Starting up Winbot app")
app = AppFactory.create()
