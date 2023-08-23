import json
import os

class DataManager:
    def __init__(self):
        self.keywords_file = None
        self.text_file = None
        self._gen_keywords = None
        self.count_keywords = None


    def set_keywords_file(self, path):
        if os.path.exists(path):
            self.keywords_file = path
            return True
        return False

    def set_message_text_file(self, path):
        if os.path.exists(path):
            self.text_file = path
            return True
        return False

    def load_keywords(self):
        with open(self.keywords_file,'r') as file:
            l_keywords = file.read().split(', ')
            self.count_keywords = len(l_keywords)
            for i in l_keywords:
                yield i

    def get_keywords_generator(self):
        self._gen_keywords = self.load_keywords()
        return self._gen_keywords

    def get_message_text(self):
        with open(self.text_file, 'r') as file:
            return file.read()

    @staticmethod
    def save_data_in_json(data: dict):
        json_object = json.dumps(data, indent=4)
        with open("save.json", "w") as file:
            file.write(json_object)

    @staticmethod
    def load_data_from_json():
        if os.path.exists("save.json"):
            with open("save.json", "r") as file:
                data = json.load(file)
                return data
        return None