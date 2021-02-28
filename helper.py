import json

class ConfigLoader:

    def __init__(self, config_path):
        self.config_path=config_path


    def load(self):
        try:
            config_file = open(self.config_path, "r")
            json_config = config_file.read()
            confs = json.loads(str(json_config))
            return confs

        except Exception as e:
            print("JSON Load Error")
            print(e)
