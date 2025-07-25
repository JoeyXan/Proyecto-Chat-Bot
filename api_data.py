from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(title="API Encuestas e Inscripciones")

# Rutas relativas a la carpeta actual
ruta_encuesta = r"C:\Users\VivoBook\Downloads\Proyecto Chat Bot\Encuesta para el proyecto _Asistente Institucional_  (respuestas).xlsx"
ruta_inscripcion = r"C:\Users\VivoBook\Downloads\Proyecto Chat Bot\Inscripción ImpulsaT - TECAZUAY (respuestas) (1).xlsx"

# Carga los datos con manejo de errores
try:
    df_encuesta = pd.read_excel(ruta_encuesta)
    print("✅ df_encuesta cargado exitosamente. Shape:", df_encuesta.shape)
except Exception as e:
    print(f"❌ Error al cargar df_encuesta: {e}")
    df_encuesta = pd.DataFrame()

try:
    df_inscripcion = pd.read_excel(ruta_inscripcion)
    print("✅ df_inscripcion cargado exitosamente. Shape:", df_inscripcion.shape)
except Exception as e:
    print(f"❌ Error al cargar df_inscripcion: {e}")
    df_inscripcion = pd.DataFrame()


@app.get("/encuestas")
def get_encuestas():
    if df_encuesta.empty:
        return {"error": "Datos de encuesta no disponibles."}
    try:
        df_encuesta_copy = df_encuesta.copy()
        for col in df_encuesta_copy.select_dtypes(include=["datetime64[ns]", "timedelta64[ns]", "datetimetz"]).columns:
            df_encuesta_copy[col] = df_encuesta_copy[col].astype(str)
        df_encuesta_copy = df_encuesta_copy.fillna("")
        return df_encuesta_copy.to_dict(orient="records")
    except Exception as e:
        print(f"❌ Error al procesar encuestas: {e}")
        return {"error": "Error al procesar los datos de encuesta."}


@app.get("/inscripciones")
def get_inscripciones():
    if df_inscripcion.empty:
        return {"error": "Datos de inscripción no disponibles."}
    try:
        df_inscripcion_copy = df_inscripcion.copy()
        for col in df_inscripcion_copy.select_dtypes(include=["datetime64[ns]", "timedelta64[ns]", "datetimetz"]).columns:
            df_inscripcion_copy[col] = df_inscripcion_copy[col].astype(str)
        df_inscripcion_copy = df_inscripcion_copy.fillna("")
        return df_inscripcion_copy.to_dict(orient="records")
    except Exception as e:
        return {"error": f"Error al procesar inscripciones: {e}"}

@app.get("/encuestas/columnas")
def columnas_encuesta():
    return list(df_encuesta.columns)

@app.get("/inscripciones/columnas")
def columnas_inscripcion():
    return list(df_inscripcion.columns)
