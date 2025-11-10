import fileinput
import sys
import configparser
import os
import time

config = configparser.ConfigParser()

def read_config():
    config.read('config.properties')
    return config

def setup_config():
    if not os.path.exists('config.properties'):
        generate_default_config()

    if not os.path.exists('./out'):
        os.makedirs('./out')

    config = read_config()
    return config['BOT']['TOKEN'], config['BOT']['SDXL_SOURCE']

def generate_default_config():
    print("[ERROR] No config file: Please rename 'config.properties.example' to 'config.properties' and restart.")

def replace_all(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def set_size(width, height):
    current_width = read_config().get('TEXT2IMG', 'WIDTH')
    current_height = read_config().get('TEXT2IMG', 'HEIGHT')
    replace_all('config.properties', 'WIDTH='+str(current_width), 'WIDTH='+str(width))
    replace_all('config.properties', 'HEIGHT='+str(current_height), 'HEIGHT='+str(height))

def set_checkpoint(checkpoint_name):
    current_ckpt_name = read_config().get('CHECKPOINT', 'CHECKPOINT_NAME')
    replace_all('config.properties', 'CHECKPOINT_NAME='+current_ckpt_name, 'CHECKPOINT_NAME='+checkpoint_name)

def set_lora(lora_name):
    current_lora_name = read_config().get('LORA', 'LORA_NAME')
    replace_all('config.properties', 'LORA_NAME='+current_lora_name, 'LORA_NAME='+lora_name)

def get_models(type):
    arr = []
    dir = read_config().get('LOCAL', 'COMFY_DIR') + r'\models' + '\\' + type
    for file in os.listdir(dir):
        if file.endswith(".safetensors"):
            arr.append(os.path.join(file))
    return arr