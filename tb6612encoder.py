from machine import Pin, PWM
import time

# --- Configuração dos Motores (TB6612FNG) ---
#AIN1_PIN = 15  
#AIN2_PIN = 26
#PWMA_PIN = 14
#BIN1_PIN = 27
#BIN2_PIN = 26
#PWMB_PIN = 29
AIN1_PIN = 27
AIN2_PIN = 26
PWMA_PIN = 29

# --- Configuração dos Encoders ---c
# C1 no GP10 e C2 no GP9
ENCODER_C1 = Pin(10, Pin.IN, Pin.PULL_UP)
ENCODER_C2 = Pin(9, Pin.IN, Pin.PULL_UP)

#ENCODER_C1_2 = Pin(12,Pin.IN, Pin.PULL_UP)
#ENCODER_C2_2 = Pin(13,Pin.IN,Pin.PULL_UP )
# --- Variáveis de Controle ---

PWM_FREQ = 10000
MAX_DUTY = 65535
ticks_totais = 0
dados_coletados = [] # Armazena (PWM, Ticks)

# --- Inicialização Hardware ---
ain1 = Pin(AIN1_PIN, Pin.OUT)
ain2 = Pin(AIN2_PIN, Pin.OUT)
#bin1 = Pin(BIN1_PIN, Pin.OUT)
#bin2 = Pin(BIN2_PIN, Pin.OUT)

pwm_a = PWM(Pin(PWMA_PIN))
pwm_a.freq(PWM_FREQ)
#pwm_b = PWM(Pin(PWMB_PIN))
#pwm_b.freq(PWM_FREQ)

# --- Função de Interrupção do Encoder ---
def contador_pulso(pino):
    global ticks_totais
    ticks_totais += 1

# Configura a interrupção no Canal A (C1)
ENCODER_C1.irq(trigger=Pin.IRQ_RISING, handler=contador_pulso)

def mover_motor(velocidade):
    """ Define a direção e o PWM do motor """
    velocidade = max(min(velocidade, 100), -100)
    
    if velocidade > 0:
        ain1.value(1)
        ain2.value(0)
    #    bin1.value(1)
    #    bin2.value(0)
    elif velocidade < 0:
        ain1.value(0)
        ain2.value(1)
    #    bin1.value(0)
    #    bin2.value(1)
    else:
        ain1.value(0)
        ain2.value(0)
    #    bin1.value(0)
    #    bin2.value(0)

    valor_pwmA = int(abs(velocidade) / 100 * MAX_DUTY)
    #valor_pwmB = int(abs(velocidade) / 100 * MAX_DUTY)

    pwm_a.duty_u16(valor_pwmA)
    #pwm_b.duty_u16(valor_pwmB)

# --- Rotina de Teste Automatizado ---
print("Iniciando Teste de Linearidade - RoboAp")
print("Aguarde 3 segundos...")
time.sleep(3)

# Cabeçalho CSV para você copiar depois
print("\n--- COPIE OS DADOS ABAIXO ---")
print("PWM,Ticks")

try:
    # Sweep de 0 a 100 de 1 em 1
    for pwm_teste in range(0, 101, 1):
        ticks_totais = 0 # Zera a contagem para este nível
        
        mover_motor(pwm_teste)
        
        # Tempo para estabilizar e contar (500ms por ponto)
        time.sleep(0.5)
        
        # Salva o resultado
        print(f"{pwm_teste},{ticks_totais}")
        dados_coletados.append((pwm_teste, ticks_totais))

    # Para o motor ao final
    mover_motor(0)
    print("--- FIM DO TESTE ---")

except KeyboardInterrupt:
    mover_motor(0)
    print("\nTeste interrompido pelo usuário.")