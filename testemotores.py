from machine import Pin, PWM
import time

# --- Configuração do Motor A (TB6612FNG) ---
AIN1_PIN = 26
AIN2_PIN = 15
PWMA_PIN = 14

# --- Configuração do Motor B (TB6612FNG) ---
# ATENÇÃO: Ajuste estes pinos conforme a sua ligação no Raspberry Pi Pico!
BIN1_PIN = 27  
BIN2_PIN = 28  
PWMB_PIN = 29  

# --- Configuração dos Encoders ---
# Motor A (C1 e C2)
ENCODER_A_C1 = Pin(12, Pin.IN, Pin.PULL_UP)
ENCODER_A_C2 = Pin(13, Pin.IN, Pin.PULL_UP)

# Motor B (C1 e C2)
ENCODER_B_C1 = Pin(9, Pin.IN, Pin.PULL_UP)
ENCODER_B_C2 = Pin(10, Pin.IN, Pin.PULL_UP)

# --- Variáveis de Controle ---
PWM_FREQ = 10000
MAX_DUTY = 65535
ticks_motorA = 0
ticks_motorB = 0
dados_coletados = [] # Armazena (Motor, PWM, Ticks)

# --- Inicialização Hardware ---
ain1 = Pin(AIN1_PIN, Pin.OUT)
ain2 = Pin(AIN2_PIN, Pin.OUT)
bin1 = Pin(BIN1_PIN, Pin.OUT)
bin2 = Pin(BIN2_PIN, Pin.OUT)

pwm_a = PWM(Pin(PWMA_PIN))
pwm_a.freq(PWM_FREQ)

pwm_b = PWM(Pin(PWMB_PIN))
pwm_b.freq(PWM_FREQ)

# --- Funções de Interrupção dos Encoders ---
def contador_pulso_A(pino):
    global ticks_motorA
    ticks_motorA += 1

def contador_pulso_B(pino):
    global ticks_motorB
    ticks_motorB += 1

# Configura as interrupções nos Canais A (C1) de ambos os motores
ENCODER_A_C1.irq(trigger=Pin.IRQ_RISING, handler=contador_pulso_A)
ENCODER_B_C1.irq(trigger=Pin.IRQ_RISING, handler=contador_pulso_B)

# --- Funções de Controle de Movimento ---
def mover_motor_A(velocidade):
    """ Define a direção e o PWM do Motor A """
    velocidade = max(min(velocidade, 100), -100)
    if velocidade > 0:
        ain1.value(1)
        ain2.value(0)
    elif velocidade < 0:
        ain1.value(0)
        ain2.value(1)
    else:
        ain1.value(0)
        ain2.value(0)
    valor_pwm = int(abs(velocidade) / 100 * MAX_DUTY)
    pwm_a.duty_u16(valor_pwm)

def mover_motor_B(velocidade):
    """ Define a direção e o PWM do Motor B """
    velocidade = max(min(velocidade, 100), -100)
    if velocidade > 0:
        bin1.value(1)
        bin2.value(0)
    elif velocidade < 0:
        bin1.value(0)
        bin2.value(1)
    else:
        bin1.value(0)
        bin2.value(0)
    valor_pwm = int(abs(velocidade) / 100 * MAX_DUTY)
    pwm_b.duty_u16(valor_pwm)

# --- Rotina de Teste Automatizado ---
print("Iniciando Teste de Linearidade - RoboAp (2 Motores)")
print("Aguarde 3 segundos...\n")
time.sleep(3)

print("--- COPIE OS DADOS ABAIXO ---")
print("Motor,PWM,Ticks")

try:
    # ==============================
    # TESTE DO MOTOR A
    # ==============================
    print("\n--- Testando Motor A ---")
    for pwm_teste in range(0, 101, 1):
        ticks_motorA = 0 # Zera a contagem para este nível
        
        mover_motor_A(pwm_teste)
        
        # Tempo para estabilizar e contar (500ms por ponto)
        time.sleep(0.5)
        
        # Salva o resultado
        print(f"A,{pwm_teste},{ticks_motorA}")
        dados_coletados.append(("A", pwm_teste, ticks_motorA))

    # Para o motor A ao final
    mover_motor_A(0)
    
    # Pausa entre os testes
    print("Pausa de 2 segundos antes de iniciar o Motor B...")
    time.sleep(2)

    # ==============================
    # TESTE DO MOTOR B
    # ==============================
    print("\n--- Testando Motor B ---")
    for pwm_teste in range(0, 101, 1):
        ticks_motorB = 0 # Zera a contagem para este nível
        
        mover_motor_B(pwm_teste)
        
        # Tempo para estabilizar e contar (500ms por ponto)
        time.sleep(0.5)
        
        # Salva o resultado
        print(f"B,{pwm_teste},{ticks_motorB}")
        dados_coletados.append(("B", pwm_teste, ticks_motorB))

    # Para o motor B ao final
    mover_motor_B(0)
    
    print("\n--- FIM DOS TESTES ---")

except KeyboardInterrupt:
    mover_motor_A(0)
    mover_motor_B(0)
    print("\nTeste interrompido pelo usuário.")