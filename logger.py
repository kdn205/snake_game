# logger.py
import logging

# Configure logging
logging.basicConfig(filename='snake_game.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log(message):
    logging.info(message)