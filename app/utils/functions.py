import json
import threading
import time

def mostrar_mensaje_con_progreso2(mensaje, funcion, *args, **kwargs):
    resultado = [None]  # Usamos una lista para capturar el resultado
    terminado = threading.Event()  # Evento para indicar cuando termina

    def operacion():
        resultado[0] = funcion(*args, **kwargs)
        terminado.set()  # Marca la operación como terminada

    # Iniciar la operación en un hilo separado
    hilo = threading.Thread(target=operacion)
    hilo.start()

    print(mensaje, end="", flush=True)
    while not terminado.is_set():  # Mientras no termine la operación
        time.sleep(0.5)
        print(".", end="", flush=True)

    print(" ¡Hecho!")
    hilo.join()  # Asegurar que el hilo termine
    return resultado[0]


def mostrar_mensaje_con_progreso(mensaje, evento_detener):
    def _mostrar():
        print(f"{mensaje}", end="", flush=True)
        while not evento_detener.is_set():
            for _ in range(3):
                if evento_detener.is_set():
                    break
                print(".", end="", flush=True)
                time.sleep(0.5)
            print("\b\b\b   \b\b\b", end="", flush=True)  # Borrar los puntos
        
        print(" ¡Hecho!")  # Indicar que se completó
    threading.Thread(target=_mostrar, daemon=True).start()


# def convertir_a_json(plan_comidas):
#     plan_json = {"dias": []}

#     for dia, comidas in enumerate(plan_comidas, start=1):
#         comidas_dia = {"dia": dia, "comidas": []}

#         for momento, comida in comidas.items():
#             comida_detalle = []
#             for item in comida:
#                 comida_detalle.append({
#                     "alimento": item.get("alimento", "Desconocido"),
#                     "cantidad": item.get("cantidad", "N/A"),
#                     "unidad": item.get("unidad", "")
#                 })
#             comidas_dia["comidas"].append({"nombre": momento, "tipo_comida": momento, "alimentos": comida_detalle})

#         plan_json["dias"].append(comidas_dia)

#     #return json.dumps(plan_json, ensure_ascii=False, indent=4)
#     return plan_comidas
def convertir_a_json(plan_comidas):
    plan_json = {"dias": []}

    for dia, comidas in enumerate(plan_comidas, start=1):
        comidas_dia = {"dia": dia, "comidas": []}

        for momento, comida in comidas.items():
            # Ajustar nombres personalizados para cada tipo de comida
            nombres_comida = {
                "desayuno": "Nombre para el desayuno",
                "almuerzo": "Nombre para el almuerzo",
                "cena": "Nombre para la cena"
            }

            nombre_comida = nombres_comida.get(momento, "Comida desconocida")

            # Verificar que 'comida' sea un diccionario antes de intentar acceder a sus claves
            if isinstance(comida, dict):
                calorias_objetivo = comida.get("calorias_objetivo", 0)
                alimentos = []

                # Iterar sobre la lista de alimentos que está en la clave 'comida'
                for item in comida.get("comida", []):  # Aquí 'comida' es una lista
                    if isinstance(item, dict):  # Si el item es un diccionario
                        alimentos.append({
                            "alimento": item.get("alimento", "Desconocido"),
                            "cantidad": item.get("cantidad", "N/A"),
                            "unidad": item.get("unidad", "")
                        })
                    elif isinstance(item, str):  # Si el item es una cadena
                        alimentos.append({
                            "alimento": item,
                            "cantidad": "N/A",
                            "unidad": ""
                        })
            elif isinstance(comida, list):  # Si 'comida' es una lista
                calorias_objetivo = 0
                alimentos = []

                # Iterar directamente sobre la lista de alimentos
                for item in comida:  # Aquí 'comida' es una lista
                    if isinstance(item, dict):  # Si el item es un diccionario
                        alimentos.append({
                            "alimento": item.get("alimento", "Desconocido"),
                            "cantidad": item.get("cantidad", "N/A"),
                            "unidad": item.get("unidad", "")
                        })
                    elif isinstance(item, str):  # Si el item es una cadena
                        alimentos.append({
                            "alimento": item,
                            "cantidad": "N/A",
                            "unidad": ""
                        })

            else:
                # Si 'comida' no es un diccionario ni una lista, asigna valores por defecto o maneja el error
                calorias_objetivo = 0
                alimentos = []

            # Añadir la comida al día
            comidas_dia["comidas"].append({
                "nombre": nombre_comida,
                "tipo_comida": momento,
                "alimentos": alimentos
            })

        plan_json["dias"].append(comidas_dia)

    return plan_json
