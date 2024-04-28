import datetime
import uuid
import random
import json
import time

while True:
    ts = int(datetime.datetime.now().timestamp() * 1000)
    id = str(uuid.uuid4())
    count = random.randint(0, 1000)
    print(
        json.dumps({"ts": ts, "uuid": id, "count": count})
    )
