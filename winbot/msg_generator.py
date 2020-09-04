# pylint: disable=missing-docstring
import slack

from winbot import config, utils


LOGGER = utils.get_logger("WINBOT")


class RequestParsingException(Exception):
    pass


class MemberNotFoundException(Exception):
    pass


SLACK_CONN = slack.WebClient(token=config.SLACK_API_TOKEN)


class MembersCache():
    def __init__(self):
        self.client = SLACK_CONN
        self.__all_slack_members = self.client.users_list().data["members"]
        self.__channel_members = self.client.conversations_members(
            channel=config.SLACK_CHANNEL_ID)["members"]

    def refresh_channel_members(self):
        c_members = self.client.conversations_members(
            channel=config.SLACK_CHANNEL_ID)["members"]

        channel_delta = len(c_members) - len(self.__channel_members)

        if channel_delta:
            # re-call the slack_members
            self.__all_slack_members = self.client.users_list()

        self.__channel_members = c_members

        return self.__channel_members

    @property
    def channel_members(self):
        # get info for the `#winning` channel
        channel_members_detail = {}

        for member in self.__all_slack_members:
            if member["id"] in self.__channel_members:
                name = member["real_name"]
                channel_members_detail[name] = member
        return channel_members_detail


class MsgGenerator:
    def __init__(self):
        self.client = SLACK_CONN
        self.members_store = MembersCache()

    @staticmethod
    def _get_owner_text(msg):
        LOGGER.info("Getting Owner text from message %s", msg)
        msg_values = msg.split("\n")
        # quick and dirty method --
        try:
            # owner text
            owner_text = msg_values[2]
            if owner_text.startswith("Owner"):
                return owner_text
        except IndexError as err:
            LOGGER.debug("WARNING: Owner text not found in message")
            raise RequestParsingException("Owner text not found %s" % err)
        return None

    def get_owner_name(self, request_text):
        LOGGER.info("Getting Win Owner Member Name")
        text = self._get_owner_text(request_text)
        owner_name = text.split(":", 1)[1]
        owner_name = owner_name.strip().replace("*", "")
        return owner_name

    def get_owner_member_id(self, owner_name):
        LOGGER.info("Getting Win Owner Member ID")
        members = self.members_store.channel_members
        found = members.get(owner_name, None)
        if found:
            return found["id"]
        for key, value in members.items():
            member_id = value["id"]

            # Try to find a POSSIBLE last name
            # example -- greynolds
            last_name = value["name"][1:]
            if last_name in owner_name:
                return member_id

            for part in owner_name.split():
                # example --
                # Alex in real_name: Alex Dalton
                # Dalton in name: adalton
                if part in value["real_name"] or part in value["name"]:
                    return member_id
        LOGGER.debug("WARNING: Owner of win not found")
        raise MemberNotFoundException("Owner %s not found" % owner_name)

    def _get_winner_msg(self, request_text):
        owner_name = self.get_owner_name(request_text)
        owner_member_id = self.get_owner_member_id(owner_name)

        if owner_member_id:
            LOGGER.info("Responding to Owner")
            msg = "Congrats <@{}>! ".format(owner_member_id)
            msg += "please fill out the form {}".format(config.GOOGLE_FORM_URL)
            self.client.chat_postMessage(channel=owner_member_id,
                                         text=msg)

        msg = "Congrats {}! ".format(owner_name)
        return msg

    def get_winner_msg(self, request_form):
        request_text = request_form["text"]
        try:
            LOGGER.info("Attempting to Send Winner Message")
            return self._get_winner_msg(request_text)
        except (RequestParsingException, MemberNotFoundException) as error:
            LOGGER.debug("WARNING: Attempt to Send Winner Message FAILED")
            LOGGER.exception("WARNING: %s", error)
            return None
