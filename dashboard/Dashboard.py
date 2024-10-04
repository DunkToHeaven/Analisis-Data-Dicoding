import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Load data
dongsi_all = pd.read_csv('/content/Dashboard/main_data.csv')

#Ubah kolom datetime menjadi tipe data datetime
dongsi_all['datetime'] = pd.to_datetime(dongsi_all[['year', 'month', 'day', 'hour']])

#Filter data waktu
min_date = dongsi_all['datetime'].min()
max_date = dongsi_all['datetime'].max()

with st.sidebar:
  #Menambahkan foto kota Dongsi
  st.image("/content/Dashboard/9f.jpg")

  #Menambahkan rentang waktu
  start_date, end_date = st.date_input(
      label='Rentang Waktu',
      min_value=min_date,
      max_value=max_date,
      value=[min_date, max_date]
  )

#Membuat filter
main_df = dongsi_all[(dongsi_all['datetime'] >= str(start_date)) & (dongsi_all['datetime'] <= str(end_date))]

#Menampilkan Header
st.header('Dashboard Analisis Kadar CO Kota Dongsi :sparkles:')

#Analisis rata-rata kadar CO per hari
st.subheader('Rata-rata Kadar CO per Hari')
daily_co = main_df.groupby(by=['year', 'month', 'day'])['CO'].mean().reset_index()
daily_co['datetime'] = pd.to_datetime(daily_co[['year', 'month', 'day']])
daily_co.sort_values(by = 'datetime', inplace=True)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_co['datetime'].dt.strftime('%d'),
    daily_co['CO'],
    marker='o',
    linewidth=2,
    color="#70823E"
)
ax.set_title('Rata-rata Kadar CO per Hari', loc='center', fontsize=18)
ax.set_ylabel('Rata-rata Kadar CO (ppm)', fontsize=12)
ax.set_xlabel('Tanggal', fontsize=12)
st.pyplot(fig)

#Analisis rata-rata kadar CO per jam dalam satu hari
st.subheader('Rata-rata Kadar CO per Jam')
hourly_co = main_df.groupby(by=['hour'])['CO'].mean().reset_index()

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hourly_co['hour'],
    hourly_co['CO'],
    marker='o',
    linewidth=2,
    color="#866C5A"
)
ax.set_title('Rata-rata Kadar CO per Jam', loc='center', fontsize=18)
ax.set_ylabel('Rata-rata Kadar CO (ppm)', fontsize=12)
ax.set_xlabel('Jam', fontsize=12)
st.pyplot(fig)

#Stat Temp, Tekanan, Kelembaban
st.subheader("Statistik Temperatur, Tekanan, dan Kelembaban")
temp, tek, kel = st.columns(3)

with temp:
    avg_temp = main_df['TEMP'].mean()
    st.metric("Rata-rata Temperatur (°C)", value=f"{avg_temp:.2f}")

with tek:
    avg_tek = main_df['PRES'].mean()
    st.metric("Rata-rata Tekanan (hPa)", value=f"{avg_tek:.2f}")

with kel:
    avg_kel = main_df['DEWP'].mean()
    st.metric("Rata-rata Titik Embun (°C)", value=f"{avg_kel:.2f}")
