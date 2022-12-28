import time
import os
import json
import argparse

import random


parser = argparse.ArgumentParser("src.fake_train")
parser.add_argument('-e','--experiment', help='current_experiment')

EXCEPTION_PERIOD = random.uniform(5, 10)


if __name__ == '__main__':
    args = parser.parse_args()
    print(f"\nStart train {args.experiment.upper()}\n")

    start_time = time.time()

    try:
        while True:
            time.sleep(2)
            a = 1234 * 5678
            if time.time() - start_time > EXCEPTION_PERIOD:
                raise Exception
    except Exception as e:
        # Telegram Stuff
        with open("./bot_logs.json", "r") as f:
            json_ = json.load(f)
        json_.update({"error": repr(e)})
        with open("./bot_logs.json", "w") as f:
            json.dump(json_, f)



