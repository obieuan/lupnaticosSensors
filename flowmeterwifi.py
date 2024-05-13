import machine
import utime
import network
import handleJson
import gc  # Garbage collector
from secrets import ssid, password, APIURL

sensor_pin = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_DOWN)
contador_pulsos = 0
total_litros = 0
factor_escala = 1.5
ultimo_tiempo = utime.ticks_ms()
ultimo_envio_tiempo = utime.ticks_ms()
tiempo_espera = 1000
sesion = 1

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            utime.sleep_ms(100)

conectar_wifi()

def cuenta_pulsos(pin):
    global contador_pulsos
    contador_pulsos += 1

sensor_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=cuenta_pulsos)

def calcular_flujo():
    global contador_pulsos, total_litros, ultimo_tiempo, ultimo_envio_tiempo
    tiempo_actual = utime.ticks_ms()
    if utime.ticks_diff(tiempo_actual, ultimo_tiempo) >= 1000:
        flujo = contador_pulsos * factor_escala / 23
        flujo = max(0, min(flujo, 10))
        total_litros += flujo / 60
        timestamp = utime.localtime()
        data = {
            "timestamp": timestamp,
            "pulses_per_minute": contador_pulsos,
            "estimated_flow_min": flujo * 0.97,
            "estimated_flow_max": flujo * 1.03,
            "total_liters_accumulated": total_litros,
            "sesion": sesion
        }
        if utime.ticks_diff(tiempo_actual, ultimo_envio_tiempo) >= tiempo_espera:
            gc.collect()  # Collect garbage before sending data
            print(f"Memoria libre antes del envío: {gc.mem_free()}")
            response = handleJson.post_json(APIURL, data)
            print(f"Memoria libre después del envío: {gc.mem_free()}")
            if response is not None and response.status_code == 200:
                print("Datos insertados correctamente")
            else:
                print("Error al insertar datos en la base de datos")
            ultimo_envio_tiempo = tiempo_actual
        contador_pulsos = 0
        ultimo_tiempo = tiempo_actual

while True:
    calcular_flujo()
    utime.sleep_ms(100)

