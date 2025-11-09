import fileinput
import sys
import configparser
import os

def get_config():
    config = configparser.ConfigParser()
    config.read('config.properties')
    return config

def setup_config():
    if not os.path.exists('config.properties'):
        generate_default_config()

    if not os.path.exists('./out'):
        os.makedirs('./out')

    config = get_config()
    return config['BOT']['TOKEN'], config['BOT']['SDXL_SOURCE']

def generate_default_config():
    print("[ERROR] No config file: Please rename 'config.properties.example' to 'config.properties' and restart.")

def replace_all(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def change_checkpoint_cfg(checkpoint_name):
    current_ckpt_name = get_config().get('CHECKPOINT', 'CHECKPOINT_NAME')

    replace_all('config.properties', current_ckpt_name, checkpoint_name)

def change_lora_cfg(lora_name):
    current_lora_name = get_config().get('LORA', 'LORA_NAME')
    replace_all('config.properties', current_lora_name, lora_name)

def get_models(type):
    arr = []
    dir = get_config().get('LOCAL', 'COMFY_DIR') + r'\models' + '\\' + type
    for file in os.listdir(dir):
        if file.endswith(".safetensors"):
            arr.append(os.path.join(file))
    return arr