import re
import cloudscraper
import logging

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
    metavar="HEADERAUTH",
    action="append",
    help="""
        Fansly authorization token
    """,
)
@pluginargument(
    "header-user-agent",
    metavar="USERAGENT",
    action="append",
    help="""
        User agent from browser
    """,
)
class FANSLY(Plugin):
    _API_BASE = "https://apiv3.fansly.com/api/v1"

    _USERNAME_SCHEMA = validate.Schema(
        validate.parse_json(),
        {
            "response": [
                {
                    "id": int
                }
            ]
        },
        validate.get(
            ("response", 0, "id")
        ),
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
        validate.get(
            ("response", "stream", "playbackUrl")
        ),
    )

    def _get_streams(self):
        # Not working when set headers inside __init__ ?
        auth = self.get_option("header-auth")[0]
        user_agent = self.get_option("header-user-agent")[0]
        # TODO this was from some fansly scraper, maybe we just need authorization?
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://fansly.com/',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': auth,
            'User-Agent': user_agent,
        }
        params = {
            "ngsw-bypass": "true"
        }

        scraper = cloudscraper.create_scraper()
        try:
            user_id = self.match["user_id"]
            streaming_channel_response = scraper.get(
                f"{self._API_BASE}/streaming/channel/{user_id}",
                headers=headers,
                params=params)
            url = self._STREAMING_SCHEMA.validate(streaming_channel_response.text)

        except (PluginError, TypeError) as err:
            log.debug(err)
            return

        finally:
            scraper.close()

        yield from HLSStream.parse_variant_playlist(self.session, url).items()


__plugin__ = FANSLY
