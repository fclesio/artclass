#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import logging
import json
from tqdm import tqdm
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    filename='met_data_metadata.log',
    filemode='w',
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
)

logger = logging.getLogger('met_data_metadata')

PROJECT_DIR = os.getcwd()


def load_local_json_file(json_local_record):
    with open(json_local_record, encoding='utf-8') as json_file:
        return json.load(json_file)


def main():
    start_time = datetime.now()

    json_extracted_files \
        = os.listdir(PROJECT_DIR + '/data')

    logger.info(f'[ARTWORK-METADATA-EXTRACTION] - Total Files in data folder: {len(json_extracted_files)}')

    json_valid_records \
        = [file for file in json_extracted_files if "json" in file]

    logger.info(f'[ARTWORK-METADATA-EXTRACTION] - Total valid records: {len(json_valid_records)}')

    list_met_metadata_values = []

    for record in tqdm(json_valid_records):
        json_local_record \
            = PROJECT_DIR + '/data/' + record

        json_data \
            = load_local_json_file(json_local_record)

        try:
            objectID = json_data.get("objectID")
            isHighlight = json_data.get("isHighlight")
            accessionNumber = json_data.get("accessionNumber")
            accessionYear = json_data.get("accessionYear")
            isPublicDomain = json_data.get("isPublicDomain")
            primaryImage = json_data.get("primaryImage")
            primaryImageSmall = json_data.get("primaryImageSmall")
            department = json_data.get("department")
            objectName = json_data.get("objectName")
            title = json_data.get("title")
            culture = json_data.get("culture")
            period = json_data.get("period")
            dynasty = json_data.get("dynasty")
            reign = json_data.get("reign")
            portfolio = json_data.get("portfolio")
            artistRole = json_data.get("artistRole")
            artistPrefix = json_data.get("artistPrefix")
            artistDisplayName = json_data.get("artistDisplayName")
            artistDisplayBio = json_data.get("artistDisplayBio")
            artistSuffix = json_data.get("artistSuffix")
            artistAlphaSort = json_data.get("artistAlphaSort")
            artistNationality = json_data.get("artistNationality")
            artistBeginDate = json_data.get("artistBeginDate")
            artistEndDate = json_data.get("artistEndDate")
            artistGender = json_data.get("artistGender")
            artistWikidata_URL = json_data.get("artistWikidata_URL")
            artistULAN_URL = json_data.get("artistULAN_URL")
            objectDate = json_data.get("objectDate")
            objectBeginDate = json_data.get("objectBeginDate")
            objectEndDate = json_data.get("objectEndDate")
            medium = json_data.get("medium")
            dimensions = json_data.get("dimensions")
            creditLine = json_data.get("creditLine")
            geographyType = json_data.get("geographyType")
            city = json_data.get("city")
            state = json_data.get("state")
            county = json_data.get("county")
            country = json_data.get("country")
            region = json_data.get("region")
            subregion = json_data.get("subregion")
            locale = json_data.get("locale")
            locus = json_data.get("locus")
            excavation = json_data.get("excavation")
            river = json_data.get("river")
            classification = json_data.get("classification")
            rightsAndReproduction = json_data.get("rightsAndReproduction")
            linkResource = json_data.get("linkResource")
            metadataDate = json_data.get("metadataDate")
            repository = json_data.get("repository")
            objectURL = json_data.get("objectURL")
            tags = json_data.get("tags")
            objectWikidata_URL = json_data.get("objectWikidata_URL")
            isTimelineWork = json_data.get("isTimelineWork")
            GalleryNumber = json_data.get("GalleryNumber")

            constituents_constituentID = None
            constituents_role = None
            constituents_name = None
            constituents_constituentULAN_URL = None
            constituents_constituentWikidata_URL = None
            constituents_gender = None
            measurements_elementName = None
            measurements_elementDescription = None
            measurements_elementDescription_elementMeasurements_Height = None
            measurements_elementDescription_elementMeasurements_Width = None

            try:
                constituents_constituentID \
                    = json_data["constituents"][0]["constituentID"]
            except:
                pass

            try:
                constituents_role \
                    = json_data["constituents"][0]["role"]
            except:
                pass

            try:
                constituents_name \
                    = json_data["constituents"][0]["name"]
            except:
                pass

            try:
                constituents_constituentULAN_URL \
                    = json_data["constituents"][0]["constituentULAN_URL"]
            except:
                pass

            try:
                constituents_constituentWikidata_URL \
                    = json_data["constituents"][0]["constituentWikidata_URL"]
            except:
                pass

            try:
                constituents_gender \
                    = json_data["constituents"][0]["gender"]
            except:
                pass

            try:
                measurements_elementName \
                    = json_data["measurements"][0]["elementName"]
            except:
                pass

            try:
                measurements_elementDescription \
                    = json_data["measurements"][0]["elementDescription"]
            except:
                pass

            try:
                measurements_elementDescription_elementMeasurements_Height \
                    = json_data["measurements"][0]["elementMeasurements"]["Height"]
            except:
                pass

            try:
                measurements_elementDescription_elementMeasurements_Width \
                    = json_data["measurements"][0]["elementMeasurements"]["Width"]
            except:
                pass

            list_met_metadata_values.append((
                objectID,
                isHighlight,
                accessionNumber,
                accessionYear,
                isPublicDomain,
                primaryImage,
                primaryImageSmall,
                department,
                objectName,
                title,
                culture,
                period,
                dynasty,
                reign,
                portfolio,
                artistRole,
                artistPrefix,
                artistDisplayName,
                artistDisplayBio,
                artistSuffix,
                artistAlphaSort,
                artistNationality,
                artistBeginDate,
                artistEndDate,
                artistGender,
                artistWikidata_URL,
                artistULAN_URL,
                objectDate,
                objectBeginDate,
                objectEndDate,
                medium,
                dimensions,
                creditLine,
                geographyType,
                city,
                state,
                county,
                country,
                region,
                subregion,
                locale,
                locus,
                excavation,
                river,
                classification,
                rightsAndReproduction,
                linkResource,
                metadataDate,
                repository,
                objectURL,
                tags,
                objectWikidata_URL,
                isTimelineWork,
                GalleryNumber,
                constituents_constituentID,
                constituents_role,
                constituents_name,
                constituents_constituentULAN_URL,
                constituents_constituentWikidata_URL,
                constituents_gender,
                measurements_elementName,
                measurements_elementDescription,
                measurements_elementDescription_elementMeasurements_Height,
                measurements_elementDescription_elementMeasurements_Width
            ))



        except Exception as e:
            logger.info(f'[ARTWORK-METADATA-EXTRACTION] - {e} - Record: {record} skipped.')

    time_elapsed = datetime.now() - start_time
    logger.info(f'[ARTWORK-METADATA-EXTRACTION] - Time elapsed (hh:mm:ss.ms) {time_elapsed}')

    columns = [
        'objectID',
        'isHighlight',
        'accessionNumber',
        'accessionYear',
        'isPublicDomain',
        'primaryImage',
        'primaryImageSmall',
        'department',
        'objectName',
        'title',
        'culture',
        'period',
        'dynasty',
        'reign',
        'portfolio',
        'artistRole',
        'artistPrefix',
        'artistDisplayName',
        'artistDisplayBio',
        'artistSuffix',
        'artistAlphaSort',
        'artistNationality',
        'artistBeginDate',
        'artistEndDate',
        'artistGender',
        'artistWikidata_URL',
        'artistULAN_URL',
        'objectDate',
        'objectBeginDate',
        'objectEndDate',
        'medium',
        'dimensions',
        'creditLine',
        'geographyType',
        'city',
        'state',
        'county',
        'country',
        'region',
        'subregion',
        'locale',
        'locus',
        'excavation',
        'river',
        'classification',
        'rightsAndReproduction',
        'linkResource',
        'metadataDate',
        'repository',
        'objectURL',
        'tags',
        'objectWikidata_URL',
        'isTimelineWork',
        'GalleryNumber',
        'constituents_constituentID',
        'constituents_role',
        'constituents_name',
        'constituents_constituentULAN_URL',
        'constituents_constituentWikidata_URL',
        'constituents_gender',
        'measurements_elementName',
        'measurements_elementDescription',
        'measurements_elementDescription_elementMeasurements_Height',
        'measurements_elementDescription_elementMeasurements_Width'
    ]

    df_met_metadata_values \
        = pd.DataFrame(list_met_metadata_values, columns=columns)

    df_met_metadata_values.to_csv(PROJECT_DIR + '/metadata/' + 'df_met_metadata_values.txt', sep="|")
    logger.info(f'[ARTWORK-METADATA-EXTRACTION] - Metadata extracted and persisted in disk')


if __name__ == '__main__':
    main()
