import matplotlib.pyplot as plt
import streamlit as st
import preprocessor,helper



st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file=st.sidebar.file_uploader('Choose a File')
if uploaded_file is not  None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)


    # fetch_unique_user
    user_list=df['user'].unique().tolist()
    user_list.remove('Group_Notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)


    if st.sidebar.button("Show Analysis"):


        num_messages,words,media,links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)


        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media")
            st.title(media)

        with col4:
            st.header("Total Links")
            st.title(links)

         # Monthly_Timeline
        st.title('Monthly Timeline')
        timeline = helper.user_time(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['massage'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily_timeline

        st.title('Daily Timeline')
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['massage'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title('Activity_Map')
        col1,col2 = st.columns(2)
        with col1:
            day = helper.busy_day(selected_user, df)
            st.header('Most Busy Daily')
            fig,ax = plt.subplots()
            ax.bar(day.index,day.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        with col2:
            month = helper.busy_month(selected_user, df)
            st.header('Most Busy Month')
            fig,ax = plt.subplots()
            ax.bar(month.index,month.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        #fetch_busy_user
        if selected_user == "Overall":
            st.title("Top Five Busy Users")
            x,new_df=helper.most_busy_user(df)
            fig,ax =plt.subplots()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        new_wc=helper.wordcloud(selected_user,df)
        st.title("WordCloud")
        fig,ax = plt.subplots()
        ax.imshow(new_wc)
        st.pyplot(fig)


        common_words=helper.most_common_words(selected_user,df)
        st.title("Most_Common_Words")
        fig,ax = plt.subplots()
        ax.bar(common_words[0],common_words[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        emoji_df=helper.most_common_emoji(selected_user,df)
        st.title('Emoji Analysis')
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%0.2f')
            st.pyplot(fig)
