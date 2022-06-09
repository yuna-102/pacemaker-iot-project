import pandas as pd
import time
import datetime

df = pd.DataFrame(columns=["id", "date", "comsumed_calories", "running_distance"])
id = "1"
cal = 0
running_distance = 0

for i in range(10):
    start_time = datetime.datetime.now()
    time.sleep(0.5)
    end_time = datetime.datetime.now()
    cal += 1
    running_distance += 2
    df = df.append(
        {
            "id": id,
            "date": end_time,
            "comsumed_calories": cal,
            "running_distance": running_distance,
        },
        ignore_index=True,
    )
    print(df)

df.to_csv("test.csv", index=False)


