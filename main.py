import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt
import matplotlib as mpl
with st.echo(code_location='below'):
    def print_hi(name):
        st.write(f"## Не знаешь что послушать, {name}?")
    if __name__ == "__main__":
        name = st.text_input("Введите имя ", key= "text", value= "anonymous")
        print_hi(name)
    def get_data():
        data_url = (
            "https://github.com/anastasions/Spotify/raw/main/spoty.csv"
        )
        return (
            pd.read_csv(data_url).dropna(subset=["year released"])
            .assign(
                yearreleased =lambda x: pd.to_datetime(
                    x["year released"], format="%Y"
                )
            )
        )

    ddata=get_data()
    song = st.text_input("Напишите название вашей любимой иностранной песни", key="text", value="")
    def yoursong():
        for i in get_data()["title"]:
            if song == "":
                return (f"## ")
            if i== song:
                st.balloons()
                return (f"## Ваша песня была в топе Spotify!!!")
        return (f"## К сожалению, ваша любимая песня не была в топе ближайшие 10 лет :( ")
    st.write(yoursong())
    st.write(f"## Вы можете найти популярные песни прошлых лет и поностальгировать!")
    def song_release():
        year = st.sidebar.slider(" Выберите год, в котором хотите узнать 3 популярные песни", 2010, 2019)
        df_filter = ddata['year released'].isin([year])
        your= ddata[df_filter]["title"].head(3)
        return (your)
    st.sidebar.write(song_release())
    st.sidebar.write("Надеюсь, хоть что-то из списка приглянулось тебе!")

    def which_genre():
        genres = ddata.groupby(['top genre']).size().reset_index(name='count')
        return (genres)

    ch =which_genre()
    ch= ch.sort_values(by= 'count', ascending=False).iloc[:10]
    vals=ch['count']
    labels = ch['top genre']
    fig, ax = plt.subplots()
    ax.pie(vals, labels=labels, wedgeprops=dict(width=0.5))

    if st.checkbox('Здесь вы можете посмотреть популярные песни по жанрам'):
        gen = st.selectbox(
            "Выберите жанр",
            ddata["top genre"].value_counts().iloc[:30].index)

        df_selection = ddata[lambda x: x["top genre"] == gen]
        df_selection

    data_names = ch['top genre'].tolist()
    data_values = ch['count'].tolist()
    ### FROM: https://eax.me/python-matplotlib/
    dpi = 80
    mpl.rcParams.update({'font.size': 9})
    xs = range(len(data_names))
    ax = plt.axes()
    ax.xaxis.grid(True, zorder=1)
    ###END FROM
    choice=st.selectbox("Хочешь посмотреть количество песен по жанрам"
                        " на разных графиках? Жмякай ниже)",
                 ( '','Диаграмма',"Гистограмма", " Диаграмма рассеивания"))
    if choice == 'Диаграмма':
            plt.title('Распределение рейтингов по жанрам (%)')
            ### FROM: https://eax.me/python-matplotlib/
            fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
            plt.pie(
                data_values, autopct='%.1f', radius=1.1,
                    explode=[0.15] + [0 for _ in range(len(data_names) - 1)])
            plt.legend(
                bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
                    loc='lower left', labels=data_names)
            ###END FROM
            st.pyplot(fig)
    if choice == "Гистограмма":
        plt.title('Распределение рейтингов по жанрам (кол-во)')
        ###FROM: https://eax.me/python-matplotlib/
        bar = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
        plt.bar([x + 0.05 for x in xs], [d * 0.9 for d in data_values],
                width=0.2, color='purple', alpha=0.7, label='Genre',
                    zorder= 2)
        plt.xticks(xs, data_names)
        bar.autofmt_xdate(rotation = 25)
        plt.legend(loc='upper right')
        ###END FROM
        st.pyplot(bar)
    if choice ==" Диаграмма рассеивания":
        chart = alt.Chart(ch).mark_point().encode(
            x='top genre',
            y='count',
            color='count:N',
            size=alt.value(350)
        ).properties(
            height=500, width=600
            )
        st.altair_chart(
            (chart
                    + chart.transform_loess("top genre", "count").mark_line()
            ).interactive())
    st.write("Исполнитель тоже очень важен в выборе музыки, может быть здесь ты найдешь кого-то нового?)")
    def which_artist():
        arts = ddata.groupby(['artist', 'year released']).size().reset_index(name='countart')
        return arts

    ar=which_artist().sort_values(by='countart', ascending= False)
    art=st.selectbox("Выберите артиста, чтобы посмотреть сколько раз он был в топе", ar['artist'].unique())
    df_filter1= ar['artist'].isin([art])
    arr= ar[df_filter1].sort_values(by="year released", ascending= False)
    artists= arr[["year released", "countart"]]
    ###FROM : https://seaborn-pydata-org.translate.goog/examples/scatterplot_sizes.html?_x_tr_sl=en&_x_tr_tl=ru&_x_tr_hl=ru&_x_tr_pto=sc
    sns.set_theme(style="whitegrid")
    cmap = sns.cubehelix_palette( as_cmap=True)
    g = sns.relplot(
        data=artists,
        x="year released", y="countart",
        hue="year released", size="countart",
        palette=cmap, sizes=(100, 200),
    )
    g.set(xscale="linear", yscale="linear")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, "minor", linewidth=.25)
    g.despine(left=True, bottom=True)
    ###END FROM
    plt.xticks(rotation=45)
    st.pyplot(g)
    st.write("Нашёл понравившуюся песню?")
    if st.button("Да!"):
        st.write("Ура!")
    if st.button("Нет :("):
        st.write("Очень жаль, попробуй еще потыкать(")