# main.py

import xml.etree.ElementTree as ET
from typing import Annotated

import logging
import traceback

from fastapi import FastAPI, File
from pydantic import BaseModel

from parser_config import PART_NAME

logger = logging.getLogger('xml_parser')
logger.setLevel(level=logging.DEBUG)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s ln:%(lineno)d %(funcName)s - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

class Configuration(BaseModel):
    path_to_xml: str


def execute_xml_parser(config: Configuration, xml_file: File = None):
    '''
    Function execute_xml_parser process xml file and collect data (product_count - count of collected products, products - list of product names, replace_parts - list of replace part names) 

    Input: path to xml file
    Output: collected data in json file
    '''

    collected_data = {
        'product_count': 0,
        'products': [],
        'replace_parts': {}
    }

    input_vaild = False
    xml_tree = None
    if config:
        logger.info(f'>>> execute_xml_parser local file {config.path_to_xml}')
        try:
            xml_tree = ET.parse(config.path_to_xml)
        except Exception:
            logger.error(f'Exception: {traceback.format_exc()}')
        else:
            input_vaild = True
    if xml_file:
        logger.info(f'>>> execute_xml_parser given file size {len(xml_file)}')
        try:
            xml_tree = ET.fromstring(xml_file)
        except Exception:
            logger.error(f'Exception: {traceback.format_exc()}')
        else:
            input_vaild = True

    if input_vaild and xml_tree:
        for item in xml_tree.find('items').findall('item'):

            if item:
                # collect product names
                collected_data['products'].append(item.get('name'))

                # collect product replase part names
                if item.find('parts'):
                    for part_data in item.find('parts').findall('part'):
                        if part_data.get('name') == PART_NAME:
                            collected_data['replace_parts'][item.get('name')] = []
                            for part_item in part_data.findall('item'):
                                collected_data['replace_parts'][item.get('name')].append(part_item.get('name'))

        # count of collected product items
        collected_data['product_count'] = len(collected_data['products'])
    else:
        collected_data['error_message'] = 'Invalid input data.'

    if config:
        logger.info(f'<<< execute_xml_parser local file {config.path_to_xml}')
    if xml_file:
        logger.info(f'<<< execute_xml_parser given file size {len(xml_file)}')

    return collected_data


app = FastAPI()


@app.post('/process_local_xml/')
async def process_local_xml(config: Configuration):

    logger.info('Process local xml: %s', config.path_to_xml)

    response = {"message": "No file path in configuration json."}
    if config.path_to_xml:
        try:
            response = execute_xml_parser(config)
        except Exception:
            response = {"message": "process_local_xml error occures."}
            logger.error(f'Exception: {traceback.format_exc()}')

    return response

@app.post('/process_xml/')
async def process_xml(xml_file: Annotated[bytes, File()]):

    logger.info('Process xml of size: %s', len(xml_file))

    response = {"message": "Given file is empty."}
    if len(xml_file):
        try:
            response = execute_xml_parser(config=None, xml_file=xml_file)
        except Exception:
            response = {"message": "process_xml error occures."}
            logger.error(f'Exception: {traceback.format_exc()}')

    return response
