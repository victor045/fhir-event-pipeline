# FHIR Event Pipeline

Un sistema de microservicios en Python para manejar eventos clínicos basados en el estándar HL7 FHIR. Utiliza Kafka para la comunicación asíncrona entre productores y consumidores, y almacena los eventos en una base de datos PostgreSQL.

---

## Tecnologías Usadas

- Python 3.10+
- FastAPI
- PostgreSQL + SQLAlchemy (asyncpg)
- Apache Kafka + aiokafka
- Docker & Docker Compose
- HL7 FHIR (modelo simplificado)
- Pytest

---

## Estructura del Proyecto

```
app/
├── models/           # Modelos FHIR y DB
├── services/         # Kafka Producer & Consumer
├── utils/            # Logging
├── config.py         # Configuración global
├── db.py             # Conexión a la base de datos
├── init_db.py        # Crea tablas
├── test_publish.py   # Script de prueba para enviar eventos
└── main.py           # Entrypoint API (opcional)
```

---

## Requisitos

- Docker y Docker Compose
- Make (opcional)
- Python 3.10 (para desarrollo local)

---

## Desarrollo Local

```bash
# 1. Clonar el proyecto
git clone https://github.com/victor045/fhir-event-pipeline.git
cd fhir-event-pipeline

# 2. Crear archivo de entorno
cp .env.example .env

# 3. Levantar servicios
docker compose up --build

# 4. Inicializar base de datos
docker compose exec app python -m app.init_db

# 5. Ejecutar consumidor
docker compose exec app python -m app.services.kafka_consumer
```

---

## Enviar un Evento FHIR (ejemplo)

```bash
docker compose exec app python -m app.scripts.test_publish
```

O con un script real:

```bash
docker compose exec app python -m app.scripts.send_real_event
```

---

## Consumir eventos y guardar en DB

Ejecuta el consumidor (si no está corriendo):

```bash
docker compose exec app python -m app.services.kafka_consumer
```

---

## Testing

```bash
pytest tests/
```

---

## Licencia

MIT License. © 2025 Victor045
