import logging
import yaml

def setup_logging():
    with open('config/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    logging.basicConfig(
        level=config['logging']['level'],
        format=config['logging']['format']
    )



    return logging.getLogger(__name__)

logger = setup_logging()