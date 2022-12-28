import os
import json


def start_train(model=None):
    os.system(f"sh ./launchers/launch_{model}.sh")


def get_eval_period(hist):
    i = 0
    while "metrics" not in hist[i]:
        i += 1
    return i + 1

def show_epoch_metrics(model=False):
    path = f"./outputs/exp_{model}/history.json" # fix

    if os.path.exists(path):

        with open(path, "r") as f:
            hist = json.load(f)

        ep = len(hist)
        loss = hist[ep-1]["train"]
        res = "Epoch: " + str(ep) + "\nLoss: " + str(round(loss,3))

        eval_period = get_eval_period(hist)
        tags = hist[eval_period-1]["metrics"].keys()
        metrics = hist[eval_period-1]["metrics"][list(tags)[0]].keys()

        if ep >= eval_period:
            for metric in metrics:
                res += f"\nLast {metric.upper()}:"
                for tag in tags:
                    res += f"\n\t\t{tag.upper()}: " + str(round(hist[ep // eval_period * eval_period - 1]["metrics"][tag][metric],3))
            return res

    return "Too early:("


def add_chat(id):
    with open("./bot_logs.json", "r") as f:
        json_ = json.load(f)

    if id not in json_["chat_ids"]:
        json_["chat_ids"].append(id)

    with open("./bot_logs.json", "w") as f:  # fix
        json.dump(json_, f)

def get_chats():
    with open("./bot_logs.json", "r") as f:
        json_ = json.load(f)

    chats = json_["chat_ids"]

    return chats if len(chats) else None