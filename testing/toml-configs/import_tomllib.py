import tomllib

# in your python code
# from ini2toml.api import Translator

# profile_name = "repeatblocks_5.cfg"
# toml_str = Translator().translate("", profile_name)


class Config:
    def __init__(self):
        pass


config = Config()


# def present(data):
#     for section in data:
#         for value in data[section]:
#             if type(data[section][value]) is list :
#                 setattr(config, data[section], [])
#                 for listVal in data[section][value]:
#                     print(listVal)
#                     config.data[section].append(data[section][value])
#                     # setattr(config, value, data[section][value])
#             else :
#                 setattr(config, value, data[section][value])



with open("repeatblocks_5test.toml", "rb") as f:
    config = tomllib.load(f)

    print(config['displayconfig']['remapimageblocksection'][0])

    # present(data)
