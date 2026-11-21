import os
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="SnapBudget", page_icon="💰")

st.title("SNAPBUDGET")
st.caption("Pelacak Pengeluaran & Struk — oleh Agnia Dwi Nugrahaeni (042)")

nama_pengguna = st.text_input("Masukkan nama kamu:", placeholder="Contoh: Agnia")
batas_per_kategori = st.number_input(
    "Batas aman pengeluaran per kategori (Rp):",
    min_value=0,
    value=50000,
    step=5000,
)

st.subheader("Masukkan Pengeluaran (Rp)")
kategori = ["Makan & Minum", "Transportasi", "Kebutuhan Kuliah", "Hiburan"]
nominal = [
    st.number_input(kat + " (Rp):", min_value=0, value=0, step=1000, key=kat)
    for kat in kategori
]

st.subheader("Foto Struk / Nota Belanja")
foto_struk = st.camera_input("Ambil foto struk (opsional)")

if st.button("Cek Anggaran & Lihat Grafik", type="primary"):
  if nama_pengguna.strip() == "":
    st.warning("Isi nama kamu dulu di atas ya!")
  else:
    st.success(f"Halo, {nama_pengguna}! Ini hasil analisis SnapBudget kamu:")
    for i in range(len(kategori)):
      nama_kat, nilai_kat = kategori[i], nominal[i]
      if nilai_kat > batas_per_kategori:
        st.error(
            f"*{nama_kat}*: Rp {int(nilai_kat):,} → MELEBIHI BATAS (+Rp"
            f" {int(nilai_kat - batas_per_kategori):,})"
        )
      else:
        st.info(
            f"*{nama_kat}*: Rp {int(nilai_kat):,} → AMAN (Sisa Rp"
            f" {int(batas_per_kategori - nilai_kat):,})"
        )

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

    if foto_struk is not None:
      os.makedirs("bukti_struk", exist_ok=True)
      path_struk = os.path.join(
          "bukti_struk",
          "snapbudget_" + nama_pengguna.lower().replace(" ", "_") + ".jpg",
      )
      with open(path_struk, "wb") as f:
        f.write(foto_struk.getbuffer())
      st.image(foto_struk, caption=f"Tersimpan di: {path_struk}", width=250)

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
          fontsize=
