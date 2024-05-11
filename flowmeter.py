from machine import Pin
import utime

# Configurar el pin del sensor
sensor_pin = Pin(28, Pin.IN, Pin.PULL_DOWN)

# Variable para contar los pulsos
contador_pulsos = 0

# Variable para acumular los litros totales
total_litros = 0

# Factor de escala para ajustar el medidor de flujo
factor_escala = 1.5  # Ajusta este valor según tus pruebas

# Variable para almacenar el tiempo del último pulso
ultimo_tiempo = utime.ticks_ms()

# Abrir el archivo en modo append
with open('flow_data.txt', 'a') as file:
    file.write("timestamp,pulses_per_minute,estimated_flow_min,estimated_flow_max,total_liters_accumulated\n")

# Función para incrementar el contador de pulsos cuando se detecta un pulso
def cuenta_pulsos(pin):
    global contador_pulsos
    contador_pulsos += 1

# Configurar interrupciones para contar los pulsos
sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=cuenta_pulsos)

# Función para calcular el flujo y acumular los litros totales
def calcular_flujo():
    global contador_pulsos, total_litros, ultimo_tiempo
    tiempo_actual = utime.ticks_ms()
    tiempo_transcurrido = utime.ticks_diff(tiempo_actual, ultimo_tiempo) / 1000  # Convertir a segundos
    if tiempo_transcurrido >= 1:  # Calcular el flujo cada segundo
        caudal = contador_pulsos / tiempo_transcurrido / 23 * factor_escala  # Calcular el flujo en litros por minuto
        if caudal < 0.3:  # Ajustar el flujo mínimo
            caudal = 0
        elif caudal > 10:  # Ajustar el flujo máximo
            caudal = 10
        total_litros += caudal / 60  # Acumular los litros totales
        caudal_min = caudal * 0.97  # Ajustar el caudal según el error de ±3%
        caudal_max = caudal * 1.03
        timestamp = utime.localtime()  # Obtener el timestamp actual
        with open('flow_data.txt', 'a') as file:
            file.write(f"{timestamp},{contador_pulsos},{caudal_min:.2f},{caudal_max:.2f},{total_litros:.2f}\n")
        print(f"Pulsos acumulados: {contador_pulsos}")
        print(f"Caudal estimado: {caudal:.2f} litros por minuto (min: {caudal_min:.2f}, max: {caudal_max:.2f})")
        print(f"Total acumulado: {total_litros:.2f} litros")
        # Reiniciar el contador de pulsos y actualizar el tiempo del último pulso
        contador_pulsos = 0
        ultimo_tiempo = tiempo_actual

# Bucle principal del programa
while True:
    utime.sleep_ms(100)  # Esperar 100 milisegundos
    calcular_flujo()

