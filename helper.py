import streamlit as st
from urlextract import URLExtract
from wordcloud import WordCloud
extractor = URLExtract()
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
       df= df[df['user'] == selected_user]

    # fetch_messages
    num_messages = df.shape[0]

    # fetch_words

    words = []
    for i in df['massage']:
        words.extend(i.split())

    # media_files

    media = df[df['massage'] =='<Media omitted>\n'].shape[0]

    #fetch_links

    links=[]
    for i in df['massage']:
        links.extend(extractor.find_urls(i))


    return num_messages,len(words),media,len(links)


def most_busy_user(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'precent'})
    return x,df

def wordcloud(selected_user,df):
    if selected_user != 'Overall':
       df= df[df['user'] == selected_user]


    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['massage'].str.cat(sep=' '))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()
    if selected_user != 'Overall':
       df= df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group_Notification']
    temp1 = temp[temp['massage'] != '<Media omitted>\n']
    li = []

    for message in temp1['massage']:
        for word in message.lower().split():
            if word not in stopwords:
                li.append(word)
    return pd.DataFrame(Counter(li).most_common(20))


def most_common_emoji(selected_user,df):
    if selected_user != 'Overall':
       df= df[df['user'] == selected_user]


    emojis=[]
    for massage in df['massage']:
        emojis.extend([c for c in massage if c in emoji.UNICODE_EMOJI['en']])
    emji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emji_df

def user_time(selected_user,df):
    if selected_user != 'Overall':
       df= df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['massage'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    dailytimeline = df.groupby('only_date').count()['massage'].reset_index()
    return dailytimeline

def busy_day(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def busy_month(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


