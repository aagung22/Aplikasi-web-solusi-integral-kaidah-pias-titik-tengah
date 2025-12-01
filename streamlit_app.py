import streamlit as st
import numpy as np
from sympy import simbols, parse_expr, lambdify

# === fungsi inti: kaidah pias titik tengah 

def midpoint_rule(f, a, b, N):
  """
  Mengaproksimasi integral tentu f(x) dari a ke b 
  menggunakan kaidah pias titik tengah dengan N pias.
  """
    if N <= 0:
    return 0.0

  # Hitung lebar pias (Delta X)
    delta_x = (b - a) / N

  # Initialisasi Total Integral
    integral_sum = 0.0

  # Iterasi melalui setiap pias
    for i in range(N):
        # Hitung titik tengah pias ke-i
        # x_k = a + i * delta_x
        # x_mid = x_k + delta_x / 2
        x_mid = a + (i + 0.5) * delta_x
        
        # Tambahkan luas persegi panjang (f(x_mid) * delta_x)
        integral_sum += f(x_mid) * delta_x
        
    return integral_sum

# === UI/UX Streamlit
st.title("Solusi Integral Tentu Numerik")
st.header("Kaidha Pias Titik Tengah")

st.markdown("---")

# === Input Function
function_str = st.text_input(
  "1. Masukkan Fungsi f(x) (gunakan 'x' sebagai variabel, contoh : sin(x), x**2 + 2*x)",
  "x**2 + 1"
)

# === Input Batas dan Pias
st.subheader("2. Tentukan Batas Integrasi dan Jumlah Pias")
col1, col2, col3 = st.columns(3)
with col1:
    a = st.number_input("Batas Bawah (a)", value=0.0)
with col2:
    b = st.number_input("Batas Atas (b)", value=1.0)
with col3:
    # Menggunakan slider untuk N agar lebih interaktif
    N = st.slider("Jumlah Pias (N)", min_value=1, max_value=1000, value=100)

st.markdown("---")
