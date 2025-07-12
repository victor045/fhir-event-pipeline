# 📦 Logistics AI Project

Este proyecto demuestra una solución integral de Inteligencia Artificial aplicada a la logística y transporte. Incluye predicción de demanda, optimización de rutas y cálculo de KPIs logísticos usando Python, Prophet, OR-Tools, Apache Airflow y Streamlit.

---

## 🔧 Requisitos

- Python 3.10+
- pip
- Apache Airflow
- Docker (opcional para despliegue)

---

## 🚀 Instalación Local Paso a Paso

```bash
# 1. Actualiza pip e instala dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 2. Configura Airflow
export AIRFLOW_HOME=$(pwd)
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="sqlite:///$AIRFLOW_HOME/airflow.db"
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/dags

# 3. Inicializa la base de datos de Airflow y crea un usuario admin
airflow db init
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

# 4. Ejecuta el script de preparación de datos
bash setup.sh

# 5. Lanza Airflow en segundo plano
airflow scheduler & airflow webserver
```

---

## 📊 Visualización del Dashboard

Abre otro terminal y corre:

```bash
streamlit run app/dashboard.py
```

Esto abre el dashboard interactivo en `http://localhost:8501`

---

## 🐳 Despliegue con Docker

```bash
docker build -t logistics-ai .
docker run -p 8501:8501 logistics-ai
```

---

## 🧠 Estructura del Proyecto

- `src/`: Lógica de procesamiento, predicción, ruteo y KPIs.
- `dags/`: Pipeline automatizado con Apache Airflow.
- `data/`: Archivos de entrada y salida (CSV).
- `app/`: Interfaz visual en Streamlit.
- `setup.sh`: Carga datos de ejemplo.

---

## 📅 Automatización con Airflow

Desde el navegador, entra a:

```
http://localhost:8080
Usuario: admin
Contraseña: admin
```

Busca el DAG `daily_logistics_pipeline` y ejecútalo manualmente para correr el pipeline completo de IA.

---

## ✨ Créditos

Creado como demostración para aplicar a posiciones de Desarrollador Senior de IA en logística y transporte.
