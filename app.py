from flask import Flask, render_template, send_from_directory
import requests
import os

# Carpeta donde está este archivo
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=carpeta_actual)

# ---------------- HISTORIAL ----------------
historial_actividades = []  # Lista en memoria para guardar actividades anteriores

@app.route("/")
def home():
    # Servimos la página principal
    return render_template("index.html")

@app.route("/styles.css")
def styles():
    # Servimos el archivo CSS
    return send_from_directory(carpeta_actual, "styles.css")

@app.route("/actividad")
def obtener_actividad():
    try:
        # Llamamos a la API de actividades aleatorias
        response = requests.get("https://bored-api.appbrewery.com/random")
        response.raise_for_status()
        actividad = response.json().get("activity", "No hay actividad")

        # Guardamos la actividad en el historial
        historial_actividades.append(actividad)

        return {"actividad": actividad}
    except Exception as e:
        # En caso de error devolvemos un mensaje
        return {"actividad": f"No se pudo cargar la actividad 😢 - {str(e)}"}

@app.route("/historial")
def ver_historial():
    # Devolvemos la lista completa de actividades guardadas
    return {"historial": historial_actividades}

if __name__ == "__main__":
    app.run(debug=True)