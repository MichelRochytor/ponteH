import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def carregar_dados(caminho: str, label: str) -> tuple[np.ndarray | None, np.ndarray | None, bool]:
    try:
        df = pd.read_csv(caminho)
        pwm = pd.to_numeric(df['PWM'], errors='coerce').to_numpy(dtype=float)
        ticks = pd.to_numeric(df['Ticks'], errors='coerce').to_numpy(dtype=float)
        return pwm, ticks, True
    except Exception as e:
        print(f"Aviso: Não foi possível carregar {caminho} ({label}).")
        return None, None, False

# 1. CARREGAR DADOS REAIS
# Sem engrenagem
pwm_tb_se, ticks_tb_se, ok_tb_se = carregar_dados('dados/tb6612fng.csv', 'TB6612FNG (Sem Engr)')
pwm_drv_se, ticks_drv_se, ok_drv_se = carregar_dados('dados/drv8833.csv', 'DRV8833 (Sem Engr)')
pwm_l298_se, ticks_l298_se, ok_l298_se = carregar_dados('dados/l298nmini.csv', 'L298N Mini (Sem Engr)')

# Com engrenagem
pwm_tb_ce, ticks_tb_ce, ok_tb_ce = carregar_dados('dadosengrenagem/tb6612fng.csv', 'TB6612FNG (Com Engr)')
pwm_drv_ce, ticks_drv_ce, ok_drv_ce = carregar_dados('dadosengrenagem/drv8833.csv', 'DRV8833 (Com Engr)')
pwm_l298_ce, ticks_l298_ce, ok_l298_ce = carregar_dados('dadosengrenagem/l298nmini.csv', 'L298N Mini (Com Engr)')

# Normalização baseada no valor máximo do TB6612 (1127 ticks) para comparar eficiência absoluta
MAX_REF = 1127

# --- CONFIGURAÇÃO DO GRÁFICO ---
plt.style.use('seaborn-v0_8-muted')
fig, ax = plt.subplots(figsize=(14, 8))

# Plotagem: Sem Engrenagem
if ok_tb_se:
    assert pwm_tb_se is not None and ticks_tb_se is not None
    ax.plot(pwm_tb_se, (ticks_tb_se / MAX_REF) * 100, '-', label='TB6612FNG (Sem Engrenagem)', color='#FFD700', lw=3, zorder=10)
if ok_drv_se:
    assert pwm_drv_se is not None and ticks_drv_se is not None
    ax.plot(pwm_drv_se, (ticks_drv_se / MAX_REF) * 100, '-', label='DRV8833 (Sem Engrenagem)', color='#1E90FF', lw=3, zorder=9)
if ok_l298_se:
    assert pwm_l298_se is not None and ticks_l298_se is not None
    ax.plot(pwm_l298_se, (ticks_l298_se / MAX_REF) * 100, '-', label='L298N Mini (Sem Engrenagem)', color='#333333', lw=3, zorder=8)

# Plotagem: Com Engrenagem
if ok_tb_ce:
    assert pwm_tb_ce is not None and ticks_tb_ce is not None
    ax.plot(pwm_tb_ce, (ticks_tb_ce / MAX_REF) * 100, '--', label='TB6612FNG (Com Engrenagem)', color='#FFD700', lw=2, zorder=7)
if ok_drv_ce:
    assert pwm_drv_ce is not None and ticks_drv_ce is not None
    ax.plot(pwm_drv_ce, (ticks_drv_ce / MAX_REF) * 100, '--', label='DRV8833 (Com Engrenagem)', color='#1E90FF', lw=2, zorder=6)
if ok_l298_ce:
    assert pwm_l298_ce is not None and ticks_l298_ce is not None
    ax.plot(pwm_l298_ce, (ticks_l298_ce / MAX_REF) * 100, '--', label='L298N Mini (Com Engrenagem)', color='#333333', lw=2, zorder=5)

# --- ELEMENTOS VISUAIS ---
ax.set_title('Comparativo de Performance Real: Drivers de Motor (Com e Sem Engrenagem)', fontsize=18, fontweight='bold')
ax.set_xlabel('Duty Cycle PWM (%)', fontsize=12)
ax.set_ylabel('Eficiência / Velocidade Relativa (%)', fontsize=12)

# Grade e Legenda
ax.grid(True, which='both', linestyle='--', alpha=0.4)
ax.legend(loc='upper left', frameon=True, shadow=True, fontsize=11)

plt.tight_layout()
plt.show()