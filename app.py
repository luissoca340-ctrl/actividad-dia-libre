from flask import Flask, render_template, send_from_directory, request
import requests
import os
from deep_translator import GoogleTranslator  #*** USAMOS deep-translator
 
carpeta_actual = os.path.dirname(os.path.abspath(_file_))
app = Flask(_name_, template_folder=carpeta_actual)
 
historial_actividades = []
 
@app.route("/")
def home():
    return render_template("index.html")
 
@app.route("/styles.css")
def styles():
    return send_from_directory(carpeta_actual, "styles.css")
 
#======================
@app.route("/actividad")
def obtener_actividad():
    tipo = request.args.get("tipo", "").strip().lower()
 
    # Tipos válidos de la API
    tipos_validos = ["education", "recreational", "social", "diy", "charity",
                     "cooking", "relaxation", "music", "busywork"]
 
    # URL base
    url = "https://bored-api.appbrewery.com/random"
 
    try:
        # Llamamos a la API hasta que obtengamos un tipo correcto
        while True:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            actividad = data.get("activity", "No hay actividad")
            actividad_tipo = data.get("type", "")
 
            # Si no hay filtro o el tipo coincide, salimos
            if tipo == "" or actividad_tipo == tipo:
                break
 
        #*** TRADUCCIÓN CON deep-translator
        actividad_es = GoogleTranslator(source='en', target='es').translate(actividad)
        #*** GUARDAMOS EN ESPAÑOL
        historial_actividades.append(actividad_es)  
        #*** DEVOLVEMOS EN ESPAÑOL
        return {"actividad": actividad_es}  
 
    except Exception as e:
        return {"actividad": f"No se pudo cargar la actividad 😢 - {str(e)}"}
#======================
 
@app.route("/historial")
def ver_historial():
    return {"historial": historial_actividades}
 
if _name_ == "_main_":
    app.run(debug=True)