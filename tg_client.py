from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PasswordHashInvalidError, ApiIdInvalidError, ChatWriteForbiddenError
from telethon.tl.types import InputPeerChat, Channel, InputPeerChannel
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.channels import JoinChannelRequest

class ClientTg:
    def __init__(self, d_manager):
        self.app_id = None
        self.app_hash = None
        self.session_name = None
        self.phone = None
        self.worked = False
        self.current_progres = 0
        self.d_manager = d_manager
        self.client = None
        self.count_per_keyword = 1
        self.min_count_subs = 0
        self.data_spam = None

    def create(self):
        try:
            self.client = TelegramClient(self.session_name, self.app_id, self.app_hash)
        except ValueError:
            return 3
        self.client.connect()
        if not self.client.is_user_authorized():
            try:
                self.client.send_code_request(self.phone)
                return 1
            except ApiIdInvalidError:
                return 3
        else:
            return 0

    def check_auth(self, data):
        if '' in data.values():
            return (0, "Empty field")

        self.app_id = data['app id']
        self.app_hash = data['app hash']
        self.session_name = data['session name']
        self.phone = data['phone']

        c = self.create()

        self.d_manager.save_data_in_json(data)

        if c == 0:
            return (1, "Goode")
        elif c == 1:
            return (2, "Code")
        else:
            return (0, "Invalid data")

    def check_code(self, code):
        try:
            self.client.sign_in(self.phone, code)
            return (1, "Good")
        except PhoneCodeInvalidError:
            return(0, "Invalid code")
        except SessionPasswordNeededError:
            return(2, "Password")

    def check_password(self, password):
        try:
            self.client.sign_in(password=password)
            return (1, "Good")
        except PasswordHashInvalidError:
            return(0, "Invalid password")


    def check_spam_data(self, data):
        count_per_keyword = data["count_per_keyword"]
        min_count_subs = data["min_count_subs"]

        if not self.d_manager.set_keywords_file(data["keyword"]):
            return (0, "Invalid keyword file")
        elif not self.d_manager.set_message_text_file(data["text"]):
            if not data['only_subscribe']:
                return (0, "Invalid message text file")
        elif not count_per_keyword.isdigit():
            return (0, "Value count per keyword must be integer")
        elif not min_count_subs.isdigit():
            return (0, "Value min count subs must be integer")

        self.count_per_keyword = int(count_per_keyword) if int(count_per_keyword) > 0 else 1
        self.min_count_subs = int(min_count_subs) if int(min_count_subs) >= 0 else 0
        return (1, "Good data")

    async def start_spam(self, data):
        self.worked = not self.worked
        self.data_spam = data
        if self.worked:
            await self._work()

    async def _work(self):
        self.current_progres = 0
        g_keywords = self.d_manager.get_keywords_generator()
        while self.worked:
            try:
                keyword = next(g_keywords)
            except StopIteration:
                self.worked = False
                break
            async for group in self.find_groops(keyword):
                print(group)
                # print(self.send_message(group['name']))
                # self.current_progres += (1 - 0) / (self.d_manager.count_keywords - 0)
                if self.current_progres >= 1:
                    self.current_progres = 1
                    self.worked = False
        print("break")


    async def find_groops(self, keyword):
        result = await self.client(SearchRequest(q=keyword, limit=self.count_per_keyword))
        for dialog in result.chats:
            if isinstance(dialog, Channel):
                title = dialog.title
                id = dialog.id
                name = dialog.username
                subs = dialog.participants_count
                if int(subs) >= self.min_count_subs:
                        yield {"title": title, "id": id, "name": name, "subs": subs}


    def send_message(self, username):
        try:
            print(username)
            # self.client(JoinChannelRequest(username))
            # if not self.data_spam['only_subscribe']:
            #     self.client.send_message(username, self.d_manager.get_message_text())
            #     print(f"{username} send {self.d_manager.get_message_text()}")
            # if self.data_spam['unsubscribe_channel']:
            #     self.client.delete_dialog(username)
            return True
        except:
            return False
