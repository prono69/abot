#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
import os
import sys
from user import User
from pyrogram import Client
from presets import Presets as Msg
from pyrogram.enums import ParseMode
from aiohttp import web
from plugins import web_server


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
    from sample_config import LOGGER
else:
    from config import Config
    from config import LOGGER

PORT = "8080"

class Bot(Client):
    USER: User = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            name="bot_session",
            # in_memory=True,
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.TG_BOT_TOKEN,
            workers=50,
            plugins={
                "root": "plugins"
            },
            sleep_threshold=5,
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        bot_me = self.USER_ID
        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"@{usr_bot_me.username}  started! "
        )
        self.USER, self.USER_ID = await User().start()
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        try:
            await self.USER.send_message(usr_bot_me.username, "%session_start%")
        except Exception:
            print(Msg.BOT_BLOCKED_MSG)
            sys.exit()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")

        