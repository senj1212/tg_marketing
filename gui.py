import logging
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.config import Config
from tg_client import ClientTg
from DataManager import DataManager
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import asyncio
from kivy.uix.checkbox import CheckBox
from kivy.uix.relativelayout import RelativeLayout


# class NullHandler(logging.Handler):
#     def emit(self, record):
#         pass
#
# logging.getLogger().setLevel(logging.CRITICAL)
#
# root_logger = logging.getLogger()
# root_logger.addHandler(NullHandler())
#
# for name in logging.Logger.manager.loggerDict.keys():
#     logging.getLogger(name).setLevel(logging.CRITICAL)
#     logging.getLogger(name).addHandler(NullHandler())

width = 420
height = 600
Window.size = (width, height)
Config.set('graphics', 'resizable', '0')
Config.write()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        line_entry = {
            "app id": None,
            "app hash": None,
            "session name": None,
            "phone": None
        }
        data = d_manager.load_data_from_json()

        base_layout = BoxLayout(orientation="vertical", spacing=30, padding=20, size_hint_y = 1, pos_hint = {'x': 0, 'y': 0.2})
        input_layout = BoxLayout(orientation="vertical", spacing=10, size_hint_y = None, height = 160)

        label = Label(text="AUTH",
                      font_size=30,
                      valign='top',
                      halign='right',
                      size_hint=(1, None),
                      padding= 30,
                      bold=True)
        label.bind(texture_size=label.setter('size'))
        base_layout.add_widget(label)

        for index, key in enumerate(line_entry.keys(), start=1):
            line_layout = BoxLayout(orientation="horizontal", spacing=15, height = 35, size_hint = (1, None))

            label = Label(text=key,
                          font_size=18,
                          halign='left',
                          valign='middle',
                          size_hint=(None, 1),
                          height=35)
            label.bind(texture_size=label.setter('size'))
            line_layout.add_widget(label)

            text_input = TextInput(hint_text=key,
                                   font_size=18)
            if key in data:
                text_input.text = data[key]
            line_layout.add_widget(text_input)

            input_layout.add_widget(line_layout)
            line_entry[key] = text_input

        base_layout.add_widget(input_layout)

        self.error_label = Label(text=" ",
                                font_size=20,
                                valign='middle',
                                size_hint=(1, None),
                                height=35,
                                color=(0.9, 0, 0, 1),
                                bold=True)
        self.error_label.bind(texture_size=self.error_label.setter('size'))
        base_layout.add_widget(self.error_label)

        func_formated_data = lambda instance: self.on_button_press(data={k: v.text for k, v in line_entry.items()})
        button = Button(text="LOGIN",
                        on_press=func_formated_data,
                        font_size=25,
                        height=50,
                        size_hint_x = 0.4,
                        size_hint_y = None,
                        pos_hint = {'center_x': 0.5, 'center_y': 0.5},
                        padding=40,
                        bold=True)

        base_layout.add_widget(button)
        self.add_widget(base_layout)

    def on_button_press(self, data):
        result = client.check_auth(data)
        if result[0] == 0:
            self.show_error_message(result[1])
        elif result[0] == 1:
            self.manager.current = "main"
        elif result[0] == 2:
            self.manager.current = "code"

    def show_error_message(self, text):
        self.error_label.text = text.upper()


class CodeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        base_layout = BoxLayout(orientation="vertical", spacing=30, padding=20, size_hint_y=1,
                                pos_hint={'x': 0, 'y': 0.4})

        label = Label(text="CODE",
                      font_size=30,
                      valign='top',
                      halign='right',
                      size_hint=(1, None),
                      padding=30,
                      bold=True)
        label.bind(texture_size=label.setter('size'))
        base_layout.add_widget(label)

        text_input = TextInput(hint_text="code",
                               font_size=18,
                               halign='center',
                               size_hint=(1, None),
                               height=35)

        base_layout.add_widget(text_input)

        self.error_label = Label(text=" ",
                                 font_size=20,
                                 valign='middle',
                                 size_hint=(1, None),
                                 height=35,
                                 color=(0.9, 0, 0, 1),
                                 bold=True)
        self.error_label.bind(texture_size=self.error_label.setter('size'))
        base_layout.add_widget(self.error_label)

        self.button = Button(text="SEND",
                             on_press=lambda instance: self.on_button_press(text_input.text),
                             font_size=25,
                             height=50,
                             size_hint_x=0.4,
                             size_hint_y=None,
                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                             padding=40,
                             bold=True)
        base_layout.add_widget(self.button)

        self.add_widget(base_layout)

    def on_button_press(self, code):
        result = client.check_code(code)
        if result[0] == 0:
            self.show_error_message(result[1])
        elif result[0] == 1:
            self.manager.current = "main"
        elif result[0] == 2:
            self.manager.current = "password"

    def show_error_message(self, text):
        self.error_label.text = text.upper()


class PasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        base_layout = BoxLayout(orientation="vertical", spacing=30, padding=20, size_hint_y=1,
                                pos_hint={'x': 0, 'y': 0.4})

        label = Label(text="PASSWORD",
                      font_size=30,
                      valign='top',
                      halign='center',
                      size_hint=(1, None),
                      padding=30,
                      bold=True)
        label.bind(texture_size=label.setter('size'))
        base_layout.add_widget(label)

        text_input = TextInput(hint_text="password",
                               font_size=18,
                               halign='center',
                               size_hint=(1, None),
                               height=35)

        base_layout.add_widget(text_input)

        self.error_label = Label(text=" ",
                                 font_size=20,
                                 valign='middle',
                                 size_hint=(1, None),
                                 height=35,
                                 color=(0.9, 0, 0, 1),
                                 bold=True)
        self.error_label.bind(texture_size=self.error_label.setter('size'))
        base_layout.add_widget(self.error_label)

        self.button = Button(text="SEND",
                             on_press=lambda instance: self.on_button_press(text_input.text),
                             font_size=25,
                             height=50,
                             size_hint_x=0.4,
                             size_hint_y=None,
                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                             padding=40,
                             bold=True)
        base_layout.add_widget(self.button)

        self.add_widget(base_layout)

    def on_button_press(self, password):
        result = client.check_password(password)
        if result[0] == 0:
            self.show_error_message(result[1])
        elif result[0] == 1:
            self.manager.current = "main"

    def show_error_message(self, text):
        self.error_label.text = text.upper()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        base_layout = BoxLayout(orientation="vertical",
                                spacing=30,
                                padding=20,
                                size_hint_y=1,
                                pos_hint={'x': 0, 'y': 0.1})
        input_layout = BoxLayout(orientation="vertical",
                                 spacing=10,
                                 size_hint_y=None,
                                 height=160)

        #title
        label = Label(text="SPAM",
                      font_size=30,
                      halign='right',
                      padding=30,
                      bold=True)
        label.bind(texture_size=label.setter('size'))
        base_layout.add_widget(label)


        # input keyword file
        line_layout = BoxLayout(orientation="horizontal", spacing=15, height=35, size_hint=(1, None))
        label = Label(text="keyword file",
                      font_size=18,
                      halign='left',
                      valign='middle',
                      size_hint=(None, 1),
                      height=35)
        label.bind(texture_size=label.setter('size'))
        line_layout.add_widget(label)

        keywords_input = TextInput(font_size=18, readonly=True, multiline=False)
        line_layout.add_widget(keywords_input)

        load_file_btn = Button(text='∞',
                               on_release= lambda instance: self.show_file_dialog(instance, keywords_input),
                               size=(35, 35),
                               size_hint=(None, 1))
        line_layout.add_widget(load_file_btn)
        input_layout.add_widget(line_layout)

        #input message file
        line_layout = BoxLayout(orientation="horizontal", spacing=15, height=35, size_hint=(1, None))
        label = Label(text="message file",
                      font_size=18,
                      halign='left',
                      valign='middle',
                      size_hint=(None, 1),
                      height=35)
        label.bind(texture_size=label.setter('size'))
        line_layout.add_widget(label)

        message_input = TextInput(font_size=18, readonly=True, multiline=False)
        line_layout.add_widget(message_input)

        load_file_btn = Button(text='∞',
                               on_release= lambda instance: self.show_file_dialog(instance, message_input),
                               size=(35, 35),
                               size_hint=(None, 1))
        line_layout.add_widget(load_file_btn)
        input_layout.add_widget(line_layout)

        # input count per keyword
        line_layout = BoxLayout(orientation="horizontal", spacing=15, height=35, size_hint=(1, None))
        label = Label(text="count per keyword",
                      font_size=18,
                      halign='left',
                      valign='middle',
                      size_hint=(None, 1),
                      height=35)
        label.bind(texture_size=label.setter('size'))
        line_layout.add_widget(label)

        count_per_keyword = TextInput(font_size=18, readonly=True, multiline=False, hint_text="count per keyword")
        line_layout.add_widget(count_per_keyword)
        input_layout.add_widget(line_layout)

        #input min count subs
        line_layout = BoxLayout(orientation="horizontal", spacing=15, height=35, size_hint=(1, None))
        label = Label(text="min count subs",
                      font_size=18,
                      halign='left',
                      valign='middle',
                      size_hint=(None, 1),
                      height=35)
        label.bind(texture_size=label.setter('size'))
        line_layout.add_widget(label)

        min_count_subs = TextInput(font_size=18, readonly=True, multiline=False, hint_text="min count subs")
        line_layout.add_widget(min_count_subs)
        input_layout.add_widget(line_layout)

        # check box unsubscribe_channel
        line_layout = BoxLayout(orientation="horizontal", spacing=15, height=35, size_hint=(1, None))
        label = Label(text="unsubscribe_channel",
                      font_size=18,
                      halign='left',
                      valign='middle',
                      size_hint=(None, 1),
                      height=35,)
        label.bind(texture_size=label.setter('size'))
        line_layout.add_widget(label)

        unsubscribe_channel = CheckBox(active=False, size_hint=(None, 1))
        line_layout.add_widget(unsubscribe_channel)
        input_layout.add_widget(line_layout)

        # check box only subscribe
        line_layout = BoxLayout(orientation="horizontal", spacing=15, height=35, size_hint=(1, None))
        label = Label(text="only subscribe",
                      font_size=18,
                      halign='left',
                      valign='middle',
                      size_hint=(None, 1),
                      height=35)
        label.bind(texture_size=label.setter('size'))
        line_layout.add_widget(label)

        only_subscribe = CheckBox(active=False, size_hint=(None, 1))
        line_layout.add_widget(only_subscribe)
        input_layout.add_widget(line_layout)


        base_layout.add_widget(input_layout)

        #error label
        self.error_label = Label(text=" ",
                                 font_size=20,
                                 valign='middle',
                                 size_hint=(1, None),
                                 height=35,
                                 color=(0.9, 0, 0, 1),
                                 bold=True)
        self.error_label.bind(texture_size=self.error_label.setter('size'))
        base_layout.add_widget(self.error_label)

        data_create = lambda instance: self.on_start(instance, {"keyword": keywords_input.text,
                                                                "text": message_input.text,
                                                                "count_per_keyword": count_per_keyword.text,
                                                                "min_count_subs": min_count_subs.text,
                                                                "unsubscribe_channel": unsubscribe_channel.active,
                                                                "only_subscribe": only_subscribe.active})
        self.button_start = Button(text="START",
                        on_press= data_create,
                        font_size=25,
                        height=50,
                        size_hint_x=0.4,
                        size_hint_y=None,
                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                        padding=40,
                        bold=True)

        base_layout.add_widget(self.button_start)

        # button go tu re_post
        r_layout = RelativeLayout()
        button = Button(text = ">",
                        size_hint = (None, None),
                        font_size = 24,
                        bold = True,
                        size = (40, 40),
                        pos = (360, 20),
                        on_press = self.open_page_posts)

        r_layout.add_widget(button)

        self.add_widget(r_layout)
        self.add_widget(base_layout)

    def open_page_posts(self, instance):
        self.manager.current = "main_re_post"

    def show_error_message(self, text):
        self.error_label.text = text.upper()

    def show_file_dialog(self, instance, input_line):
        file_chooser = FileChooserIconView(filters=["*.txt"], path = ".")
        file_chooser.bind(on_submit=lambda instance, selection, touch: self.file_selected(instance, selection, touch, input_line))
        self.popup = Popup(title="Выберите файл", content=file_chooser, size_hint=(None, None), size=(400, 400))
        self.popup.open()

    def file_selected(self, instance, selection, touch, input_line):
        if selection:
            input_line.text = selection[0]
        self.popup.dismiss()

    def on_start(self, instance, data):
        if self.button_start.text == "STOP":
            self.button_start.text = "START"
            client.worked = False
        result = client.check_spam_data(data)
        if result[0] == 0:
            self.show_error_message(result[1])
            return

        if self.button_start.text == "START":
            self.button_start.text = "STOP"

        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.start_spam(data))
        loop.close()


class MainRePostScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        base_layout = BoxLayout(orientation="vertical",
                                spacing=30,
                                padding=20,
                                size_hint_y=1,
                                pos_hint={'x': 0, 'y': 0.1})
        input_layout = BoxLayout(orientation="vertical",
                                 spacing=10,
                                 size_hint_y=None,
                                 height=160)

        # title
        label = Label(text="RE-POST",
                      font_size=30,
                      halign='right',
                      padding=30,
                      bold=True)
        label.bind(texture_size=label.setter('size'))
        base_layout.add_widget(label)

        # button go tu re_post
        r_layout = RelativeLayout()
        button = Button(text="<",
                        size_hint=(None, None),
                        font_size=24,
                        bold=True,
                        size=(40, 40),
                        pos=(20, 20),
                        on_press=self.open_spam)

        r_layout.add_widget(button)

        self.add_widget(r_layout)
        self.add_widget(base_layout)

    def open_spam(self, instance):
        self.manager.current = "main"



class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(CodeScreen(name="code"))
        sm.add_widget(PasswordScreen(name="password"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(MainRePostScreen(name="main_re_post"))
        return sm


if __name__ == "__main__":
    d_manager = DataManager()
    client = ClientTg(d_manager)
    MyApp().run()