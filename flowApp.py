import flet as ft
import requests
import threading

def fetch_total_liters_from_server(sesion_id):
    url = "http://localhost/lupnaticos/leerflow.php"  # Reemplaza con la URL real de tu script PHP
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json={'sesion': sesion_id}, headers=headers)
        response.raise_for_status()  # Esto lanzará una excepción si el código de estado HTTP no es 200
        data = response.json()
        return data.get("total_liters_accumulated", 0)
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return 0
    except ValueError as e:
        print(f"Error al decodificar JSON: {e}")
        return 0

def update_liters_label(page, txt_number, sesion_id):
    while True:
        total_liters = fetch_total_liters_from_server(sesion_id)
        txt_number.value = str(total_liters)
        page.update()
        threading.Event().wait(1)  # Espera un segundo antes de la próxima actualización

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    sesion_id = 1  # Suponemos que siempre es 1 para este ejemplo
    total_liters = fetch_total_liters_from_server(sesion_id)

    txt_number = ft.TextField(value=str(total_liters), text_align=ft.TextAlign.RIGHT, width=100)
    txt_number.expand = True

    page.add(
        ft.Row(
            [
                txt_number,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    # Iniciar un hilo para actualizar el valor cada segundo
    threading.Thread(target=update_liters_label, args=(page, txt_number, sesion_id), daemon=True).start()

ft.app(main)
