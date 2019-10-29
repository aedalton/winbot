# pylint: disable=missing-docstring
import json

import flask

from winbot.msg_generator import MsgGenerator


class AppFactory:  # pylint: disable=too-few-public-methods
    @classmethod
    def create(cls):
        """Create and configure an instance of the Flask application."""
        app = flask.Flask(__name__, instance_relative_config=True)

        # load the instance config, if it exists, when not testing
        app.config.from_object('winbot.config.AppSettings')

        msg_generator = MsgGenerator()

        @app.route('/health', methods=['GET'])
        def health():  # pylint: disable=unused-variable
            response = app.response_class(
                response=json.dumps({"health": "okay"}),
                status=200,
                mimetype='application/json'
            )
            return response

        @app.route('/win', methods=['POST'])
        def win():  # pylint: disable=unused-variable
            response_text = msg_generator.get_winner_msg(
                flask.request.form)
            if response_text is None:
                return None

            response = app.response_class(
                response=json.dumps({
                    "username": "Winning Alert",
                    "text": response_text
                }),
                status=200,
                mimetype='application/json'
            )
            return response

        return app
