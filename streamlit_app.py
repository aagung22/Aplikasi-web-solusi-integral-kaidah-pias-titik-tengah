import streamlit as st
import numpy as np
from sympy import symbols, parse_expr, lambdify

# === fungsi inti: kaidah pias titik tengah 

def midpoint_rule(f, a, b, N):
    """
    Mengaproksimasi integral tentu f(x) dari a ke b 
    menggunakan kaidah pias titik tengah dengan N pias.
    """
    # INDENTASI LEVEL 1: Kondisi awal
    if N <= 0:
        # INDENTASI LEVEL 2: Di dalam blok 'if'
        return 0.0

    # Hitung lebar pias (Delta X)
    delta_x = (b - a) / N

    # Initialisasi Total Integral
    integral_sum = 0.0

    # Iterasi melalui setiap pias
    for i in range(N):
        # Hitung titik tengah pias ke-i
        x_mid = a + (i + 0.5) * delta_x
        
        # Tambahkan luas persegi panjang (f(x_mid) * delta_x)
        integral_sum += f(x_mid) * delta_x
        
    return integral_sum

# === UI/UX Streamlit
st.title("Solusi Integral Tentu Numerik")
st.header("Kaidah Pias Titik Tengah")

st.markdown("---")

# === Input Function
function_str = st.text_input(
  "1. Masukkan Fungsi f(x) (gunakan 'x' sebagai variabel, contoh : sin(x), x**2 + 2*x)",
  "x**2 + 1"
)

# === Input Batas dan Pias
st.subheader("Tentukan Batas Integrasi dan Jumlah Pias")
col1, col2, col3 = st.columns(3)
with col1:
    a = st.number_input("Batas Bawah (a)", value=0.0)
with col2:
    b = st.number_input("Batas Atas (b)", value=1.0)
with col3:
    # Menggunakan slider untuk N agar lebih interaktif
    N = st.slider("Jumlah Pias (N)", min_value=1, max_value=1000, value=100)

st.markdown("---")

# Validasi input fungsi
try:
    x = symbols('x')
    expr = parse_expr(function_str, transformations='all')
    f_lambdified = lambdify(x, expr, modules=['numpy', 'math'])
    is_valid_function = True
except Exception as e:
    st.error(f"❌ Error dalam fungsi: {e}")
    st.info("Pastikan fungsi menggunakan sintaks Python yang valid. Contoh: x**2 + sin(x)*exp(x)")
    is_valid_function = False
    f_lambdified = None

st.markdown("---")

# === Perhitungan dan Visualisasi
if st.button("📊 Hitung Integral Numerik", type="primary") and is_valid_function:
    st.subheader("Hasil Perhitungan")
    
    # Hitung menggunakan kaidah titik tengah
    try:
        # Hitung nilai integral
        result_midpoint = midpoint_rule(f_lambdified, a, b, N)
        
        # Tampilkan hasil
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(
                label="Hasil Integral Numerik",
                value=f"{result_midpoint:.8f}",
                help="Hasil aproksimasi menggunakan kaidah titik tengah"
            )
        
        with col_res2:
            # Hitung error relatif jika fungsi dapat diintegralkan secara simbolis
            try:
                from sympy import integrate
                exact_integral = integrate(expr, (x, a, b))
                exact_value = float(exact_integral.evalf())
                error = abs(exact_value - result_midpoint)
                rel_error = (error / abs(exact_value)) * 100 if exact_value != 0 else float('inf')
                
                st.metric(
                    label="Error Relatif",
                    value=f"{rel_error:.4f}%",
                    delta=f"Error absolut: {error:.6f}",
                    help="Perbandingan dengan solusi eksak (jika tersedia)"
                )
                
                # Tampilkan nilai eksak
                st.info(f"**Nilai eksak (simbolis):** {exact_value:.8f}")
                
            except:
                st.info("⚠️ Tidak dapat menghitung nilai eksak secara simbolis")
        
        st.markdown("---")
        
        # === Visualisasi
        st.subheader("Visualisasi Kaidah Titik Tengah")
        
        # Generate data untuk plotting
        x_vals = np.linspace(a, b, 1000)
        y_vals = f_lambdified(x_vals)
        
        # Titik tengah untuk visualisasi
        delta_x = (b - a) / N
        x_midpoints = np.array([a + (i + 0.5) * delta_x for i in range(N)])
        y_midpoints = f_lambdified(x_midpoints)
        
        # Buat plot
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot fungsi asli
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {function_str}')
        
        # Plot persegi panjang titik tengah
        for i in range(N):
            x_left = a + i * delta_x
            x_right = a + (i + 1) * delta_x
            rect = plt.Rectangle(
                (x_left, 0), delta_x, y_midpoints[i],
                alpha=0.3, color='orange', edgecolor='red'
            )
            ax.add_patch(rect)
            
            # Titik tengah
            ax.plot(x_midpoints[i], y_midpoints[i], 'ro', markersize=4)
        
        # Konfigurasi plot
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('f(x)', fontsize=12)
        ax.set_title(f'Kaidah Titik Tengah untuk N = {N}', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xlim([a, b])
        
        # Otomatis atur ylim
        y_min, y_max = min(y_vals), max(y_vals)
        ax.set_ylim([min(0, y_min) - 0.1*(y_max-y_min), y_max + 0.1*(y_max-y_min)])
        
        st.pyplot(fig)
        
        st.markdown("---")
        
        # === Tabel Detail Perhitungan
        st.subheader("Detail Perhitungan per Pias")
        
        if N <= 20:  # Hanya tampilkan jika N kecil
            data = []
            for i in range(N):
                x_mid = a + (i + 0.5) * delta_x
                f_mid = f_lambdified(x_mid)
                area = f_mid * delta_x
                data.append({
                    "Pias ke-": i+1,
                    "x_tengah": f"{x_mid:.4f}",
                    "f(x_tengah)": f"{f_mid:.6f}",
                    "Luas": f"{area:.6f}"
                })
            
            # Tampilkan tabel
            import pandas as pd
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            # Hitung kumulatif
            st.write(f"**Total luas (integral) = {result_midpoint:.8f}**")
        else:
            st.info(f"Total {N} pias. Tabel hanya ditampilkan untuk N ≤ 20.")
            
        st.markdown("---")
        
        # === Analisis Konvergensi
        st.subheader("Analisis Konvergensi")
        
        # Hitung untuk berbagai nilai N
        N_values = [10, 20, 50, 100, 200, 500, 1000]
        results = []
        
        for n_val in N_values:
            if n_val <= N_values[-1]:
                res = midpoint_rule(f_lambdified, a, b, n_val)
                results.append(res)
        
        # Plot konvergensi
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.plot(N_values[:len(results)], results, 'bo-', linewidth=2)
        ax2.set_xlabel('Jumlah Pias (N)', fontsize=12)
        ax2.set_ylabel('Nilai Integral', fontsize=12)
        ax2.set_title('Konvergensi Kaidah Titik Tengah', fontsize=14)
        ax2.grid(True, alpha=0.3)
        ax2.set_xscale('log')
        
        st.pyplot(fig2)
        
        st.caption("Semakin besar N, hasil semakin konvergen ke nilai sebenarnya.")
        
    except Exception as e:
        st.error(f"❌ Error dalam perhitungan: {e}")
        st.info("Periksa batas integrasi dan fungsi yang dimasukkan.")

st.markdown("---")

# === Teori dan Penjelasan
with st.expander("📚 Teori Kaidah Titik Tengah"):
    st.markdown("""
    ### Rumus Kaidah Titik Tengah
    
    Untuk mengaproksimasi integral tentu:
    
    $$
    \int_{a}^{b} f(x) \, dx \approx \Delta x \sum_{i=1}^{N} f\left(x_i^{mid}\right)
    $$
    
    dengan:
    - $\Delta x = \\frac{b-a}{N}$ (lebar pias)
    - $x_i^{mid} = a + \\left(i - \\frac{1}{2}\\right) \Delta x$ (titik tengah pias ke-i)
    - $N$ = jumlah pias
    
    ### Contoh:
    Untuk $f(x) = x^2$ dari 0 ke 1 dengan N=4:
    - $\Delta x = 0.25$
    - Titik tengah: 0.125, 0.375, 0.625, 0.875
    - $I \approx 0.25[f(0.125) + f(0.375) + f(0.625) + f(0.875)] = 0.328125$
    
    ### Kelebihan:
    1. Sederhana dan mudah diimplementasi
    2. Akurat untuk fungsi yang smooth
    3. Error berkurang dengan $O(1/N^2)$
    
    ### Kekurangan:
    1. Kurang akurat untuk fungsi dengan variasi cepat
    2. Membutuhkan evaluasi fungsi di setiap titik tengah
    """)

# === Informasi Tambahan
st.sidebar.markdown("### 📝 Informasi Aplikasi")
st.sidebar.info("""
**Kaidah Titik Tengah (Midpoint Rule)**

Aplikasi ini mengaproksimasi integral tentu menggunakan metode numerik kaidah titik tengah.

**Cara penggunaan:**
1. Masukkan fungsi f(x)
2. Tentukan batas integrasi a dan b
3. Pilih jumlah pias N
4. Klik tombol hitung

**Contoh fungsi valid:**
- x**2 + 3*x + 1
- sin(x)*cos(x)
- exp(-x**2)
- 1/(1+x**2)
""")

# === Footer
st.markdown("---")
st.caption("Aplikasi Solusi Integral Numerik menggunakan Streamlit | Kaidah Pias Titik Tengah")
