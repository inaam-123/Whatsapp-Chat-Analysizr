import re
import pandas as pd

def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\wm\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_massage': messages, 'date': dates})
    df['date'] = df['date'].str.split('-').str.get(0)
    df['date'] = pd.to_datetime(df['date'])
    user = []
    massage = []
    for i in df['user_massage']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            user.append(entry[1])
            massage.append(entry[2])
        else:
            user.append('Group_Notification')
            massage.append(entry[0])

    df['user'] = user
    df['massage'] = massage
    df.drop(columns=['user_massage'], axis=1, inplace=True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['hours'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df
