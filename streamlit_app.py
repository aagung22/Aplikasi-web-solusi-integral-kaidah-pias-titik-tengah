import streamlit as st
import numpy as np
import pandas as pd
from sympy import symbols, parse_expr, lambdify, integrate

# === fungsi inti: kaidah pias titik tengah 
def midpoint_rule(f, a, b, N):
    """
    Mengaproksimasi integral tentu f(x) dari a ke b 
    menggunakan kaidah pias titik tengah dengan N pias.
    """
    if N <= 0:
        return 0.0

    delta_x = (b - a) / N
    integral_sum = 0.0

    for i in range(N):
        x_mid = a + (i + 0.5) * delta_x
        integral_sum += f(x_mid) * delta_x
        
    return integral_sum

# === UI/UX Streamlit
st.set_page_config(
    page_title="Kalkulator Integral Numerik",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Kalkulator Integral Numerik")
st.header("Menggunakan Kaidah Pias Titik Tengah")

st.markdown("---")

# === Sidebar untuk input
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    function_str = st.text_area(
        "**Fungsi f(x)**",
        value="x**2 + 1",
        help="Gunakan 'x' sebagai variabel. Contoh: sin(x), exp(-x**2), 1/(1+x**2)"
    )
    
    st.subheader("Batas Integrasi")
    col_a, col_b = st.columns(2)
    with col_a:
        a = st.number_input("Bawah (a)", value=0.0, step=0.1)
    with col_b:
        b = st.number_input("Atas (b)", value=1.0, step=0.1)
    
    N = st.slider(
        "**Jumlah Pias (N)**",
        min_value=1,
        max_value=500,
        value=100,
        help="Semakin besar N, semakin akurat hasilnya"
    )
    
    if st.button("🚀 Hitung Integral", type="primary", use_container_width=True):
        st.session_state.calculate = True
    else:
        if 'calculate' not in st.session_state:
            st.session_state.calculate = False

# === Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Visualisasi")
    
with col2:
    st.subheader("📋 Hasil")

# === Validasi dan pemrosesan fungsi
try:
    x = symbols('x')
    expr = parse_expr(function_str, transformations='all')
    f_lambdified = lambdify(x, expr, modules=['numpy', 'math'])
    
    # Tampilkan fungsi yang dimasukkan
    st.info(f"**Fungsi:** f(x) = `{function_str}`")
    
    if st.session_state.calculate:
        # === Perhitungan integral
        result = midpoint_rule(f_lambdified, a, b, N)
        
        with col2:
            # Kotak hasil
            st.metric(
                label="Hasil Integral Numerik",
                value=f"{result:.8f}",
                delta=f"N={N} pias"
            )
            
            # Coba hitung nilai eksak
            try:
                exact_integral = integrate(expr, (x, a, b))
                exact_value = float(exact_integral.evalf())
                error = abs(exact_value - result)
                
                st.metric(
                    label="Nilai Eksak",
                    value=f"{exact_value:.8f}"
                )
                
                st.metric(
                    label="Error",
                    value=f"{error:.8f}",
                    delta=f"{(error/exact_value*100 if exact_value != 0 else 0):.4f}%"
                )
            except:
                st.warning("Tidak dapat menghitung nilai eksak secara simbolis")
        
        with col1:
            # === Visualisasi dengan matplotlib
            import matplotlib.pyplot as plt
            
            # Data untuk plot
            x_vals = np.linspace(a, b, 1000)
            y_vals = f_lambdified(x_vals)
            delta_x = (b - a) / N
            
            # Buat plot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot fungsi
            ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {function_str}')
            
            # Tambahkan persegi panjang titik tengah
            for i in range(N):
                x_left = a + i * delta_x
                x_mid = a + (i + 0.5) * delta_x
                y_mid = f_lambdified(x_mid)
                
                # Rectangle
                rect = plt.Rectangle(
                    (x_left, 0), delta_x, y_mid,
                    alpha=0.3, color='orange', edgecolor='red', linewidth=0.5
                )
                ax.add_patch(rect)
                
                # Titik tengah
                ax.plot(x_mid, y_mid, 'ro', markersize=3)
            
            # Konfigurasi plot
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('f(x)', fontsize=12)
            ax.set_title(f'Visualisasi Kaidah Titik Tengah (N={N})', fontsize=14)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.legend(loc='upper left')
            ax.set_xlim([a, b])
            
            # Set y-limits
            y_min, y_max = min(y_vals), max(y_vals)
            margin = (y_max - y_min) * 0.1
            ax.set_ylim([y_min - margin, y_max + margin])
            
            # Tampilkan plot
            st.pyplot(fig)
        
        # === Tabel detail per pias (jika N kecil)
        if N <= 30:
            st.subheader("📊 Detail Perhitungan per Pias")
            
            data = []
            for i in range(N):
                x_mid = a + (i + 0.5) * delta_x
                f_val = f_lambdified(x_mid)
                area = f_val * delta_x
                
                data.append({
                    "Pias": i+1,
                    "x Tengah": f"{x_mid:.6f}",
                    "f(x)": f"{f_val:.6f}",
                    "Luas": f"{area:.6f}"
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, height=400)
            
            # Ringkasan
            st.success(f"**Total Integral ≈ {result:.8f}** (dijumlahkan dari {N} pias)")
        
        # === Analisis konvergensi
        st.subheader("📈 Analisis Konvergensi")
        
        # Hitung untuk berbagai N
        N_values = [10, 20, 50, 100, 200, 500]
        N_values = [n for n in N_values if n <= 500]
        
        convergence_data = []
        for n_val in N_values:
            val = midpoint_rule(f_lambdified, a, b, n_val)
            convergence_data.append(val)
        
        # Plot konvergensi
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(N_values, convergence_data, 'bo-', linewidth=2, markersize=6)
        ax2.axhline(y=exact_value if 'exact_value' in locals() else result, 
                   color='r', linestyle='--', alpha=0.5, label='Nilai Referensi')
        ax2.set_xlabel('Jumlah Pias (N)', fontsize=11)
        ax2.set_ylabel('Nilai Integral', fontsize=11)
        ax2.set_title('Konvergensi Hasil terhadap Jumlah Pias', fontsize=13)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_xscale('log')
        
        st.pyplot(fig2)
        
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.info("""
    **Pastikan fungsi menggunakan sintaks yang benar:**
    - Gunakan `x` sebagai variabel
    - Operator: `+`, `-`, `*`, `/`, `**` (pangkat)
    - Fungsi: `sin(x)`, `cos(x)`, `exp(x)`, `log(x)`, `sqrt(x)`
    - Contoh: `x**2 + sin(x)`, `exp(-x**2)`, `1/(1+x**2)`
    """)

# === Footer dan informasi
st.markdown("---")

with st.expander("ℹ️ Tentang Kaidah Titik Tengah"):
    st.markdown("""
    ### **Rumus Matematika:**
    
    $$
    \int_{a}^{b} f(x) \, dx \approx \Delta x \sum_{i=1}^{N} f\left(x_i^{mid}\right)
    $$
    
    **dengan:**
    - $\Delta x = \frac{b-a}{N}$ (lebar pias)
    - $x_i^{mid} = a + \left(i - \frac{1}{2}\right) \Delta x$ (titik tengah pias ke-i)
    
    ### **Contoh:**
    Untuk $\int_0^1 x^2 dx$ dengan N=4:
    - $\Delta x = 0.25$
    - $I \approx 0.25[f(0.125) + f(0.375) + f(0.625) + f(0.875)] = 0.328125$
    - Nilai eksak: $0.333333...$
    
    ### **Ketepatan:**
    - Error ~ $O\left(\frac{1}{N^2}\right)$
    - Lebih akurat daripada kaidah persegi panjang
    """)

st.caption("Dibuat dengan Streamlit | Kaidah Titik Tengah untuk Integral Numerik")
