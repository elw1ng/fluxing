import json

def loadKeysTelega():
    with open("../data/keys.json", "r") as file:
        keys_data = file.read()
    return json.loads(keys_data)

def saveKeysTelega(keys):

    keys_data = json.dumps(keys)
    with open("../data/keys.json", "w") as file:
        file.write(keys_data)

def onlySaveKeys(keys):

    keys_data = json.dumps(keys)
    with open("../data/keys.json", "w") as file:
        file.write(keys_data)


def reset():
    keys_data = json.dumps(dct)
    with open("data/keys.json", "w") as file:
        file.write(keys_data)


def saveKeys(keys):

    keys_data = json.dumps(keys)
    with open("data/keys.json", "w") as file:
        file.write(keys_data)


def loadKeys():
    with open("data/keys.json", "r") as file:
        keys_data = file.read()

    return json.loads(keys_data)


def loadKeysGui():
    with open("data/keys.json", "r") as file:
        keys_data = file.read()

    return json.loads(keys_data)


dct = {
       "base": {
                        "activate_key": "",
                        "key1": {"name": "", "value": ""},
                        "key2": {"name": "", "value": ""},
                        "key3": {"name": "", "value": ""},
                        "key4": {"name": "", "value": ""},
                        "key5": {"name": "", "value": ""},
                        "key6": {"name": "", "value": ""},
                    },

       "fluxing": {
                        "activate_key": "f1",
                        "key1": {"name": "selfcast", "value": "v"},
                        "key2": {"name": "moveback", "value": "s"},
                        "key3": {"name": "moveforward", "value": "w"},
                        "key4": {"name": "moveleft", "value": "a"},
                        "key5": {"name": "moveright", "value": "d"},
                        "key6": {"name": "power", "value": "2"},
                        "key7": {"name": "summon", "value": "3"},
                        "key8": {"name": "barrier", "value": "4"},
                        "key9": {"name": "kau", "value": "5"},
                        "key10": {"name": "returnifNoAnswerTimer", "value": "8"},
                        "key11": {"name": "MoveForwardMultiplier", "value": "0.9925"},
                        "key12": {"name": "MaxMoveBackTimer", "value": "1.8"},
                        "key13": {"name": "StopifInactive", "value": "4"},
                        "key14": {"name": "MaxSpiritSize", "value": "40"},
                        "key15": {"name": "SpiritFile", "value": "spirit1.png"},
                        "key16": {"name": "Prefire", "value": "1.2"},
                        "key17": {"name": "USER ID", "value": ""},
                        "key18": {"name": "TOKEN", "value": ""},
                    }
       }


if __name__ == "__main__":
    onlySaveKeys(dct)
    # print(loadKeys())

