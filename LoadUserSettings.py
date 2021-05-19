import json


def LoadPrefix():
    with open("UserConfig.json", "r") as source:
        UserPrefs = json.load(source)
        return UserPrefs["Prefix"]

def ChangePrefix(Prefix):
    with open('UserConfig.json', 'r+') as f:
        data = json.load(f)
        data['Prefix'] = Prefix  # <--- add `id` value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part



