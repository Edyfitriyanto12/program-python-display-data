from tabulate import tabulate

# Data sensor (contoh data)
data_sensor = [
    {"Sensor": "Sensor 1", "Suhu": 25.5, "Kelembaban": 60, "Tekanan": 1013, "Kualitas Udara": "Baik"},
    {"Sensor": "Sensor 2", "Suhu": 26.0, "Kelembaban": 58, "Tekanan": 1012, "Kualitas Udara": "Baik"},
    {"Sensor": "Sensor 3", "Suhu": 24.8, "Kelembaban": 62, "Tekanan": 1014, "Kualitas Udara": "Sedang"},
    {"Sensor": "Sensor 4", "Suhu": 27.2, "Kelembaban": 55, "Tekanan": 1011, "Kualitas Udara": "Baik"}
]

# Menampilkan masing-masing data sensor
print("Data Sensor Individual:")
for data in data_sensor:
    print(f"\n{data['Sensor']}:")
    # Membuat tabel untuk setiap sensor
    table = [
        ["Suhu (°C)", data["Suhu"]],
        ["Kelembaban (%)", data["Kelembaban"]],
        ["Tekanan (hPa)", data["Tekanan"]],
        ["Kualitas Udara", data["Kualitas Udara"]]
    ]
    print(tabulate(table, headers=["Parameter", "Nilai"], tablefmt="grid"))
    print("-" * 30)

# Menampilkan gabungan semua data sensor
print("\nGabungan Data Semua Sensor:")
# Menyiapkan data untuk tabel gabungan
headers = ["Sensor", "Suhu (°C)", "Kelembaban (%)", "Tekanan (hPa)", "Kualitas Udara"]
rows = []
for data in data_sensor:
    rows.append([
        data["Sensor"],
        data["Suhu"],
        data["Kelembaban"],
        data["Tekanan"],
        data["Kualitas Udara"]
    ])

# Menampilkan tabel gabungan
print(tabulate(rows, headers=headers, tablefmt="grid"))
