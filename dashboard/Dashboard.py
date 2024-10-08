import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Load data
dongsi_all = pd.read_csv("main_data.csv")

#Ubah kolom datetime menjadi tipe data datetime
dongsi_all['datetime'] = pd.to_datetime(dongsi_all[['year', 'month', 'day', 'hour']])

#Filter data waktu
min_date = dongsi_all['datetime'].min()
max_date = dongsi_all['datetime'].max()

with st.sidebar:
  #Menambahkan foto kota Dongsi
  st.image("dashboard/9f.jpg")

# Membuat opsi pemilihan tahun
year_options = dongsi_all['datetime'].dt.year.unique()  # Mendapatkan nilai tahun unik
year_selected = st.selectbox('Pilih Tahun', year_options)  # Menampilkan pilihan tahun

# Menentukan bulan yang valid berdasarkan tahun yang dipilih
if year_selected == 2013:
    month_options = dongsi_all[dongsi_all['datetime'].dt.year == 2013]['datetime'].dt.month.unique()
elif year_selected == 2017:
    month_options = dongsi_all[dongsi_all['datetime'].dt.year == 2017]['datetime'].dt.month.unique()
else:
    month_options = list(range(1, 13))  # Untuk tahun selain 2013 dan 2017, tampilkan bulan 1-12

# Menampilkan pilihan bulan hanya yang sesuai dengan tahun yang dipilih
selected_month = st.selectbox('Pilih Bulan', month_options)

# Memfilter data hanya berdasarkan bulan dan tahun yang dipilih
main_df = dongsi_all[
    (dongsi_all['datetime'].dt.month == selected_month) &
    (dongsi_all['datetime'].dt.year == year_selected)
]

#Menampilkan Header
st.header('Dashboard Analisis Kadar CO Kota Dongsi')

#Analisis rata-rata kadar CO per hari
st.subheader('Rata-rata Kadar CO per Hari')
daily_co = main_df.groupby(by=['year', 'month', 'day'])['CO'].mean().reset_index() #Menghitung kadar CO per hari
daily_co['datetime'] = pd.to_datetime(daily_co[['year', 'month', 'day']]) #Mengubah type data menjadi datetime
daily_co.sort_values(by = 'datetime', inplace=True)

# Membuat figure dan axis untuk bar dan line chart
fig, ax1 = plt.subplots(figsize=(16, 8))

# Plot Bar
ax1.bar(
    daily_co['datetime'].dt.strftime('%d'),
    daily_co['CO'],
    color="lightblue",
    alpha=0.6,
    label='Kadar CO (Bar)'
)

# Membuat twin axis untuk plot garis
ax2 = ax1.twinx()
ax2.plot(
    daily_co['datetime'].dt.strftime('%d'),
    daily_co['CO'],
    marker='o',
    linewidth=2,
    color="#70823E",
    label='Kadar CO (Line)'  # Label line chart
)

# Menambahkan judul dan label sumbu
ax1.set_ylabel('Rata-rata Kadar CO (ppm)', fontsize=12)
ax1.set_xlabel('Tanggal', fontsize=12)
ax2.get_yaxis().set_visible(False)

# Menambahkan legenda
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Menampilkan plot di Streamlit
st.pyplot(fig)

#Analisis rata-rata kadar CO per jam dalam satu hari
st.subheader('Rata-rata Kadar CO per Jam')
daily_co = main_df.groupby(by=['hour'])['CO'].mean().reset_index()

# Membuat figure dan axis untuk bar dan line chart
fig1, ax1 = plt.subplots(figsize=(16, 8))

# Plot Bar
ax1.bar(
    daily_co['hour'],
    daily_co['CO'],
    color="lightblue",
    alpha=0.6,
    label='Kadar CO (Bar)'
)

# Membuat axis kedua untuk line chart
ax2 = ax1.twinx()
ax2.plot(
    daily_co['hour'],
    daily_co['CO'],
    marker='o',
    linewidth=2,
    color="#866C5A",
    label='Kadar CO (Line)'
)

# Menambahkan judul dan label sumbu
ax1.set_ylabel('Rata-rata Kadar CO (ppm) - Bar', fontsize=12)
ax1.set_xlabel('Jam', fontsize=12)
ax2.get_yaxis().set_visible(False)

# Menambahkan legenda
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Menampilkan plot di Streamlit
st.pyplot(fig1)

# Membuat figure baru untuk Heatmap
st.subheader('Heatmap Korelasi')
# Menghitung hubungan dengan metode pearson
corr_dongsi = dongsi_all[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr(method='pearson')

# Membuat figure untuk heatmap
fig2, ax3 = plt.subplots(figsize=(10, 8))  # Figure baru untuk heatmap
sns.heatmap(corr_dongsi, annot=True, cmap='coolwarm', ax=ax3)
ax3.set_title('Correlation Matrix of Pollutants (Pearson)')

# Menampilkan heatmap di Streamlit
st.pyplot(fig2)
