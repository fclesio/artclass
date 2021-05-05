#!/usr/bin/env python
# coding: utf-8

import requests
import logging
import json
import glob
from tqdm import tqdm
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    filename='met_data_extraction.log',
    filemode='w',
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
)

logger = logging.getLogger('met_extraction')


def get_all_objects():
    base_url_all_objects = 'https://collectionapi.metmuseum.org/public/collection/v1/objects'
    response_all_objects = requests.get(f'{base_url_all_objects}')
    response_all_objects_json = response_all_objects.json()
    total_artworks = response_all_objects_json['total']
    logger.info(f'[OBJECTS-IDS-EXTRACTION] - Qty of extracted Artworks: {total_artworks}')
    return response_all_objects_json['objectIDs']


def resume_extraction():
    saved_records = []

    for filepath in glob.glob('data/**', recursive=True):
        try:
            artwork_id = int(filepath.split("_")[3].replace(".json", ""))
            saved_records.append(artwork_id)
        except:
            pass

    return set(saved_records)


def get_artwork(artwork_seacrh_id):
    base_url_artwork_search = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/'

    try:
        response_artwork_search = requests.get(f'{base_url_artwork_search}{str(artwork_seacrh_id)}')
        if response_artwork_search.status_code == 200:
            logger.info(f'[ARTWORK-PAYLOAD-EXTRACTION] - Extraction with success for artwork_id: {artwork_seacrh_id}')
        return response_artwork_search.json()
    except Exception as e:
        logger.error(f'[ARTWORK-PAYLOAD-EXTRACTION] - Extraction failure for artwork_id: {artwork_seacrh_id}',
                     exc_info=True)


def save_file(fileobject, artwork_search_id):
    with open(f'data/extraction_met_info_{artwork_search_id}.json', 'w', encoding='utf-8') as f:
        json.dump(fileobject, f, ensure_ascii=False, indent=4)
        logger.info(f'[ARTWORK-EXTRACTION-SAVING] - Saving: data/extraction_met_info_{artwork_search_id}.json')


def main():
    start_time = datetime.now()

    artworks_ids_all = set(get_all_objects())
    previously_saved_files = resume_extraction()
    artworks_to_download = artworks_ids_all - previously_saved_files

    logger.info(f'[ARTWORK-PAYLOAD-EXTRACTION] - Resume previously extraction...')
    logger.info(f'[ARTWORK-PAYLOAD-EXTRACTION] - Qty files in MET: {len(artworks_ids_all)}')
    logger.info(f'[ARTWORK-PAYLOAD-EXTRACTION] - Qty previously saved files: {len(previously_saved_files)}')
    logger.info(f'[ARTWORK-PAYLOAD-EXTRACTION] - Qty remaining files to save: {len(artworks_to_download)}')

    for artwork_id in tqdm(artworks_to_download):
        artwork_payload = get_artwork(artwork_id)

        if artwork_payload is not None:
            save_file(artwork_payload, artwork_id)

    time_elapsed = datetime.now() - start_time
    logger.info(f'[ARTWORK-PAYLOAD-EXTRACTION] - Time elapsed (hh:mm:ss.ms) {time_elapsed}')


if __name__ == '__main__':
    main()
