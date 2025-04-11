from utils.globals import os, logging


def setup_logger(name):
    logs_dir = os.path.join("outputs", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita adicionar múltiplos handlers em execuções sucessivas
    if not logger.handlers:
        fh = logging.FileHandler(os.path.join(logs_dir, f"{name}.log"), encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


# Example usage:
# from utils.logger import get_logger
# logger = get_logger()

# logger.info("Análise iniciada")
# logger.error("Erro ao processar JSON")
