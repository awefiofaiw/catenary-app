
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.integrate import quad

st.set_page_config(page_title="현수선 구조 계산기", layout="centered")

st.title("🧮 케이블 구조물 최적 설계 도우미")

st.write("입력한 거리(D)와 처짐 깊이(H)를 바탕으로 최적 a값, 곡선 그래프, 장력 방향, 퍼텐셜 에너지, 자재 길이를 시각화합니다.")

D = st.number_input("📏 거리 D (단위: m)", value=120.0, step=10.0)
H = st.number_input("📐 처짐 깊이 H (단위: m)", value=12.0, step=1.0)

if st.button("계산하기"):
    def equation(a):
        return a * np.cosh(D / (2 * a)) - a - H

    try:
        a_sol = fsolve(equation, D / 2)[0]
        if a_sol <= 0 or np.isnan(a_sol):
            raise ValueError("해를 찾을 수 없습니다.")
    except Exception as e:
        st.error("❌ 유효한 해를 찾을 수 없습니다. 입력값을 확인하세요.")
    else:
        st.success(f"✅ 계산된 최적 a값: {a_sol:.2f} m")

        x = np.linspace(-D/2, D/2, 500)
        y = a_sol * np.cosh(x / a_sol) - a_sol
        dy = np.sinh(x / a_sol)

        rho = 1  # 단위 질량
        g = 9.8  # 중력가속도

        def integrand(x):
            return rho * g * (a_sol * np.cosh(x / a_sol) - a_sol) * np.sqrt(1 + (np.sinh(x / a_sol))**2)

        U, _ = quad(integrand, -D/2, D/2)
        st.write(f"⚙️ 퍼텐셜 에너지: {U:,.2f} J")

        def arc_length(x):
            return np.sqrt(1 + (np.sinh(x / a_sol))**2)

        L, _ = quad(arc_length, -D/2, D/2)
        st.write(f"📏 예상 자재 길이: {L:.2f} m")

        fig, ax = plt.subplots()
        ax.plot(x, y, label="현수선 곡선")
        ax.quiver(x[::20], y[::20], 1, dy[::20], angles='xy', scale_units='xy', scale=10, color='r', width=0.002, label="장력 방향")
        ax.set_title("현수선 곡선 및 장력 방향")
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.legend()
        st.pyplot(fig)
