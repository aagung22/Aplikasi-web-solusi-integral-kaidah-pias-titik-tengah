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
