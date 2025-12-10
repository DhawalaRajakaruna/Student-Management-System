#!/usr/bin/python
from configparser import ConfigParser
from pathlib import Path

def config(filename='database.ini', section='postgresql'):
    # Get the directory where this file is located
    current_dir = Path(__file__).resolve().parent
    config_path = current_dir / filename
    
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(str(config_path))

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, str(config_path)))

    return db