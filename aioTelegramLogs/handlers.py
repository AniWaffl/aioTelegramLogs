import logging
from io import BytesIO
import aiohttp
import asyncio

from aioTelegramLogs.formatters import BaseFormatter, MarkdownFormatter, HtmlFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)
logger.propagate = False

__all__ = ['AioTGhandler']

class AioTGhandler(logging.Handler):
    BASE_URL = 'https://api.telegram.org'
    MAX_MESSAGE_LEN = 4096
    list_response = []

    def __init__(self, token: str, chat_id: list, level=logging.NOTSET, 
                 disable_notification=False, disable_web_page_preview=False):
        self.token = token
        self.disable_web_page_preview = disable_web_page_preview
        self.disable_notification = disable_notification
        self.chat_id = chat_id
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        super(AioTGhandler, self).__init__(level=level)

        self.setFormatter(HtmlFormatter())


    @classmethod
    def format_url(cls, token, method):
        return '%s/bot%s/%s' % (cls.BASE_URL, token, method)

    async def request(self, metod, **kwargs):
        url = self.format_url(self.token, metod)
        response = None

        try:
            async with aiohttp.ClientSession() as session:
                logger.info(f"Url = {url}, kwargs = {kwargs}")
                async with session.post(url=url, **kwargs) as response:
                    await asyncio.sleep(0.1)
                    return response.status

        except Exception as e:
            logger.error(e)

    async def send_message(self, text, **kwargs):
        data = {'text': text}
        data.update(kwargs)
        return await self.request('sendMessage', json=data)
        

    def send_document(self, text, document, **kwargs):
        data = {'caption': text}
        data.update(kwargs)
        return self.request('sendDocument', data=data, files={'document': ('traceback.txt', document, 'text/plain')})
        

    def emit(self, record):
        text = self.format(record)
        for chat_id in self.chat_id:
            data = {
                'chat_id': chat_id,
                'disable_web_page_preview': self.disable_web_page_preview,
                'disable_notification': self.disable_notification,
            }

            if getattr(self.formatter, 'parse_mode', None):
                data['parse_mode'] = self.formatter.parse_mode

            if len(text) < self.MAX_MESSAGE_LEN:
                
                response = self.loop.create_task(
                    self.send_message(text, **data)
                    )
            else:
                response = self.loop.create_task(
                    self.send_document(text[:1000], document=BytesIO(text.encode()), **data)
                    )
                    

        # if response and not response.get('ok', False):
        #     logger.warning('Telegram responded with ok=false status! {}'.format(response))
