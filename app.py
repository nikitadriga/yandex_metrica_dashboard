import streamlit as st
import pandas as pd
from metrika_client import get_daily_stats, get_devices, get_search_queries, get_traffic_sources, get_conversions
import plotly.express as px
from database import load_daily_stats
from datetime import date, timedelta
import plotly.express as px

st.set_page_config(page_title="Metrika Dashboard", layout="wide")

st.title("📊 Yandex Metrica Dashboard")

st.subheader("Период статистики")

period = st.radio(
    "Выберите период",
    ["7 дней", "30 дней", "90 дней", "365 дней"],
    horizontal=True,
    index=1
)

today = date.today()

if period == "7 дней":
    start_date = today - timedelta(days=7)
elif period == "30 дней":
    start_date = today - timedelta(days=30)
elif period == "90 дней":
    start_date = today - timedelta(days=90)
else:
    start_date = today - timedelta(days=365)

end_date = today

date1 = start_date.strftime("%Y-%m-%d")
date2 = end_date.strftime("%Y-%m-%d")


rows = load_daily_stats()

df = pd.DataFrame(rows, columns=["date", "visits", "users", "pageviews"])

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")
df = df[
    (df["date"] >= pd.to_datetime(date1)) &
    (df["date"] <= pd.to_datetime(date2))
]

col1, col2, col3 = st.columns(3)

col1.metric("Визиты", int(df["visits"].sum()))
col2.metric("Пользователи", int(df["users"].sum()))
col3.metric("Просмотры", int(df["pageviews"].sum()))

st.subheader("Динамика по дням")

fig = px.line(
    df,
    x="date",
    y=["visits", "users", "pageviews"],
    markers=True
)

fig.update_layout(
    xaxis_title="Дата",
    yaxis_title="Значения",
    legend_title="Метрики"
)

st.plotly_chart(fig, use_container_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["📱 Устройства", "🔎 Поисковые запросы", "🌐 Источники", "🎯 Конверсии"])


with tab1:
    st.subheader("Устройства")

    devices = get_devices(date1, date2)
    df_devices = pd.DataFrame(devices)

    if not df_devices.empty:
        fig = px.pie(
            df_devices,
            names="device",
            values="visits",
            title="Распределение по устройствам"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_devices, use_container_width=True)
    else:
        st.info("Данные по устройствам не найдены.")


with tab2:
    st.subheader("Поисковые запросы")

    queries = get_search_queries(date1, date2)
    df_queries = pd.DataFrame(queries)

    if not df_queries.empty:
        st.bar_chart(df_queries.set_index("query")["visits"])
        st.dataframe(df_queries, use_container_width=True)
    else:
        st.info("Поисковые запросы не найдены.")


with tab3:
    st.subheader("Источники трафика")

    sources = get_traffic_sources(date1, date2)
    df_sources = pd.DataFrame(sources)

    if not df_sources.empty:
        # преобразуем секунды в время
        df_sources["avg_time"] = pd.to_timedelta(df_sources["avg_time_sec"], unit="s")

        # оставляем только формат HH:MM:SS
        df_sources["avg_time"] = pd.to_timedelta(df_sources["avg_time_sec"], unit="s")
        df_sources["avg_time"] = df_sources["avg_time"].dt.floor("s").astype(str)
        df_sources["avg_time"] = df_sources["avg_time"].str.split(" ").str[-1]

        # удаляем сырые секунды
        df_sources = df_sources.drop(columns=["avg_time_sec"])

        st.bar_chart(df_sources.set_index("source")["visits"])
        st.dataframe(df_sources, use_container_width=True)

    else:
        st.info("Данные по источникам не найдены.")

with tab4:
    st.subheader("Конверсии")

    conversions = get_conversions(date1, date2)
    df_conversions = pd.DataFrame(conversions)

    if not df_conversions.empty:
        st.bar_chart(df_conversions.set_index("goal")["conversion_rate"])
        st.dataframe(df_conversions, use_container_width=True)
    else:
        st.info("Цели пока не добавлены. Добавь Goal ID в функцию get_conversions().")
