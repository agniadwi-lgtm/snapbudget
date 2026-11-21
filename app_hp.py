import os
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="SnapBudget", page_icon="💰")

st.title("💰 SNAPBUDGET")
st.caption("Pelacak Pengeluaran & Struk — oleh Agnia Dwi Nugrahaeni (042)")

# 1. Input Data Pengguna
nama_pengguna = st.text_input("Masukkan nama kamu:", placeholder="Contoh: Agnia")
batas_per_kategori = st.number_input(
    "Batas aman pengeluaran per kategori (Rp):",
    min_value=0,
    value=50000,
    step=5000,
)

st.subheader("Masukkan Pengeluaran (Rp)")
kategori = ["Makan & Minum", "Transportasi", "Kebutuhan Kuliah", "Hiburan"]
nominal = []

for kat in kategori:
  biaya = st.number_input(
      kat + " (Rp):", min_value=0, value=0, step=1000, key=kat
  )
  nominal.append(biaya)

# 2. Kamera HP Langsung untuk Foto Struk
st.subheader("Foto Struk / Nota Belanja")
foto_struk = st.camera_input("Ambil foto struk (opsional)")

# 3. Tombol Proses & Grafik
if st.button("Cek Anggaran & Lihat Grafik", type="primary"):
  if nama_pengguna.strip() == "":
    st.warning("Isi nama kamu dulu di atas ya!")
  else:
    st.success(f"Halo, {nama_pengguna}! Ini hasil analisis SnapBudget kamu:")

    # Cek batas aman vs melebihi batas
    kategori_boros = []
    for i in range(len(kategori)):
      nama_kat = kategori[i]
      nilai_kat = nominal[i]
      if nilai_kat > batas_per_kategori:
        selisih = nilai_kat - batas_per_kategori
        st.error(
            f"*{nama_kat}*: Rp {int(nilai_kat):,} → MELEBIHI BATAS (+Rp"
            f" {int(selisih):,})"
        )
        kategori_boros.append(nama_kat)
      else:
        sisa = batas_per_kategori - nilai_kat
        st.info(
            f"*{nama_kat}*: Rp {int(nilai_kat):,} → AMAN (Sisa Rp"
            f" {int(sisa):,})"
        )

    # Ringkasan Statistik
    total_keluar = sum(nominal)
    rata_rata = total_keluar / len(nominal)
    terbesar_nilai = max(nominal)
    terbesar_kat = kategori[nominal.index(terbesar_nilai)]

    st.write("---")
    st.write(f"*Total Pengeluaran:* Rp {int(total_keluar):,}")
    st.write(f"*Rata-rata per Kategori:* Rp {int(rata_rata):,}")
    st.write(
        f"*Pengeluaran Terbesar:* {terbesar_kat} (Rp"
        f" {int(terbesar_nilai):,})"
    )

    # Simpan foto struk ke folder bukti_struk
    if foto_struk is not None:
      folder_struk = "bukti_struk"
      os.makedirs(folder_struk, exist_ok=True)
      nama_file = (
          "snapbudget_" + nama_pengguna.lower().replace(" ", "_") + ".jpg"
      )
      path_struk = os.path.join(folder_struk, nama_file)
      with open(path_struk, "wb") as f:
        f.write(foto_struk.getbuffer())
      st.image(foto_struk, caption=f"Tersimpan di: {path_struk}", width=250)

    # Grafik Batang (hotpink & crimson)
    warna = [
        "crimson" if n > batas_per_kategori else "hotpink" for n in nominal
    ]
    fig, ax = plt.subplots(figsize=(7, 4))
    grafik = ax.bar(kategori, nominal, color=warna)
    ax.axhline(
        y=batas_per_kategori,
        color="purple",
        linestyle="--",
        label=f"Batas Aman (Rp {int(batas_per_kategori):,})",
    )
    ax.set_title(f"SnapBudget - Analisis Pengeluaran {nama_pengguna}")
    ax.set_ylabel("Nominal (Rp)")
    ax.legend()

    for bar in grafik:
      tinggi = bar.get_height()
      ax.text(
          bar.get_x() + bar.get_width() / 2,
          tinggi,
          f"Rp {int(tinggi):,}",
          ha="center",
          va="bottom",
          fontsize=8,
      )

    st.pyplot(fig)