from machine import Pin, PWM
import time

# --- Configuração dos Motores (DRV8833) ---
IN1_PIN = 0  # GPIO 0
IN2_PIN = 1  # GPIO 1

# --- Configuração dos Encoders ---
ENCODER_C1 = Pin(4, Pin.IN, Pin.PULL_UP)
# O C2 geralmente é usado para direção, mas para o gráfico de RPM o C1 basta
ENCODER_C2 = Pin(5, Pin.IN, Pin.PULL_UP) 

# --- Variáveis de Controle ---
PWM_FREQ = 10000
MAX_DUTY = 65535
ticks_totais = 0

# --- Inicialização Hardware ---
in1 = PWM(Pin(IN1_PIN))
in2 = PWM(Pin(IN2_PIN))
in1.freq(PWM_FREQ)
in2.freq(PWM_FREQ)

# --- Função de Interrupção do Encoder ---
def contador_pulso(pino):
    global ticks_totais
    ticks_totais += 1

# Configura a interrupção no Canal A (C1)
ENCODER_C1.irq(trigger=Pin.IRQ_RISING, handler=contador_pulso)

def mover_motor(velocidade):
    """
    Lógica DRV8833:
    Frente: IN1 (PWM), IN2 (0)
    Ré: IN1 (0), IN2 (PWM)
    """
    velocidade = max(min(velocidade, 100), -100)
    valor_pwm = int(abs(velocidade) / 100 * MAX_DUTY)

    if velocidade > 0:
        in1.duty_u16(valor_pwm)
        in2.duty_u16(0)
    elif velocidade < 0:
        in1.duty_u16(0)
        in2.duty_u16(valor_pwm)
    else:
        in1.duty_u16(0)
        in2.duty_u16(0)

# --- Rotina de Teste Automatizado ---
print("Iniciando Teste DRV8833 - RoboAp")
print("Aguarde 3 segundos...")
time.sleep(3)

print("\n--- COPIE OS DADOS ABAIXO ---")
print("PWM,Ticks")

try:
    # Varredura de 0 a 100 de 1 em 1
    for pwm_teste in range(0, 101, 1):
        ticks_totais = 0 # Zera contagem
        
        mover_motor(pwm_teste)
        
        # Mantém o mesmo tempo de amostragem do teste anterior (0.5s)
        time.sleep(0.5)
        
        # Exibe no terminal para o CSV
        print(f"{pwm_teste},{ticks_totais}")

    # Finaliza
    mover_motor(0)
    print("--- FIM DO TESTE ---")

except KeyboardInterrupt:
    mover_motor(0)
    print("\nTeste interrompido.")