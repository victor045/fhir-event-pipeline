
import logging
import sys

# Formato estructurado y legible
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] ▶ %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configuración global del logger
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Logger de la aplicación
logger = logging.getLogger("fhir-pipeline")

