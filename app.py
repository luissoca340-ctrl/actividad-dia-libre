from flask import Flask, render_template, send_from_directory
import requests
import os

carpeta_actual = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=carpeta_actual)

# Ruta principal que sirve el HTML
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para CSS 
@app.route("/styles.css")
def  styles():
    return send_from_directory(carpeta_actual, "styles.css")

# Ruta para la actividad aleatoria
@app.route("/actividad")
def obtener_actividad():
    try:
        response = requests.get("https://bored-api.appbrewery.com/random")
        response.raise_for_status()
        actividad = response.json().get("activity", "No hay actividad")
        return {"actividad": actividad}
    except Exception as e:
        return {"actividad": f"No se pudo cargar la actividad 😢 - {str(e)}"}

if __name__ == "__main__":
    app.run(debug=True)