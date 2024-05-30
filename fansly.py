import re
import logging
import requests

from streamlink.plugin import Plugin, pluginmatcher, pluginargument
from streamlink.plugin.api import validate
from streamlink.stream import HLSStream
from streamlink.exceptions import PluginError

log = logging.getLogger(__name__)


@pluginmatcher(
    re.compile(
        r"https?://(?:www\.)?fansly\.com/live/(?P<user_id>\d+)$",
    ),
    name="live_stream",
)
@pluginargument(
    "header-auth",
    required=True,
    metavar="HEADERAUTH",
    action="append",
    help="Fansly authorization token",
)
@pluginargument(
    "header-user-agent",
    required=True,
    metavar="USERAGENT",
    action="append",
    help="User agent from browser",
)
class Fansly(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _API_BASE = "https://apiv3.fansly.com/api/v1"

    _USERNAME_SCHEMA = validate.Schema(
        validate.parse_json(),
        {
            "response": [{"id": int}]
            },
        validate.get(("response", 0, "id")),
    )

    _ACCOUNT_SCHEMA = validate.Schema(
        validate.parse_json(),
        {
            "response": [{"username": str}]
            },
        validate.get(("response", 0, "username")),
    )

    _STREAMING_SCHEMA = validate.Schema(
        validate.parse_json(),
        {
            "response": {
                "stream": {
                    "playbackUrl": validate.url(path=validate.endswith(".m3u8")),
                }
            }
        },
        validate.get(("response", "stream", "playbackUrl")),
    )

    def _get_streams(self):
        try:
            auth_option = self.get_option("header-auth")[0]
            user_agent_option = self.get_option("header-user-agent")[0]
            headers = {
                "authorization": auth_option,
                "User-Agent": user_agent_option,
            }

            user_id = self.match["user_id"]

            # This is needed for user_id match to get username
            account_url = f"{self._API_BASE}/account?ids={user_id}"
            account = requests.get(
                account_url,
                headers=headers,
            )
            self.author = self._ACCOUNT_SCHEMA.validate(account.text)

            # This is needed for username match to get user_id
            # url = f"{self._API_BASE}/account?usernames={username}",
            # _USERNAME_SCHEMA

            stream_url = f"{self._API_BASE}/streaming/channel/{user_id}"
            stream_meta = requests.get(
                stream_url,
                headers=headers,
            )
            url = self._STREAMING_SCHEMA.validate(stream_meta.text)
            if (url is None):
                raise Exception(f"Could not get stream URL from {stream_url}")
        except (PluginError, TypeError) as err:
            log.debug(err)
            return

        yield from HLSStream.parse_variant_playlist(self.session, url).items()


__plugin__ = Fansly
