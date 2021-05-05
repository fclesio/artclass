#!/usr/bin/env python
# coding: utf-8

import os
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import requests
import logging
import numpy as np
import shutil
import uuid

logging.basicConfig(
    level=logging.INFO,
    filename='met_save_image_files.log',
    filemode='w',
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
)

logger = logging.getLogger('met_data_metadata')

start_time = datetime.now()
logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Start - Start time: {start_time}')

PROJECT_DIR = os.getcwd()

images_data_folder = PROJECT_DIR + '/images_data'


def get_class_report(df, column):
    df_group \
        = pd.DataFrame(df.groupby(column).size()).reset_index()

    df_group.columns = ["column", 'qty']

    return df_group.sort_values(by=['qty'], ascending=False)


def generate_art_class_column(df, old_desc, new_desc, column='medium'):
    df['art_class'] \
        = np.where(
        df[column] == old_desc,
        new_desc,
        df['art_class'])
    return df


def delete_folder(path):
    shutil.rmtree(path)
    os.mkdir(path)


def save_image_in_folder(image_url, file_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

    response = requests.get(image_url, stream=True, headers=headers)
    if response.status_code == 200:
        response.raw.decode_content = True
        with open(file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
    else:
        print(f'ImageURL: {file_path} not retrieved')


def main():
    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Load metadata file...')
    df_met_metadata_values \
        = pd.read_csv(PROJECT_DIR + '/metadata/' + 'df_met_metadata_values.txt',
                      sep="|",
                      index_col=0,
                      )

    df_met_metadata_values.fillna('', inplace=True)

    df_met_metadata_values['art_class'] = 'misc'

    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Save list of class distribution for medium...')
    df_medium_class_report = get_class_report(df_met_metadata_values, "medium")
    df_medium_class_report.to_csv('reports/medium_class_report.csv', sep='|', index=None)

    list_mapping = [
        ('Graphite on wove paper with gilt edges, bound in a leather', 'graphite_on_wove_paper'),
        ('Terracotta', 'terracotta'),
        ('Commercial color lithograph', 'commercial_color_lithograph'),
        ('Etching', 'etching'),
        ('', 'misc'),
        (' ', 'misc'),
        ('Engraving', 'engraving'),
        ('Gelatin silver print', 'gelatin_silver'),
        ('Albumen photograph', 'albumen'),
        ('Silk', 'silk'),
        ('Brown and black ink and graphite on dark off-white-tan', 'brown_and_black_ink'),
        ('Black ink wash, gray gouache, and black chalk on off-white', 'black_ink_wash'),
        ('Brown and black ink and pink gouache on dark off-white-tan', 'brown_and_black_ink'),
        ('Bronze', 'bronze'),
        ('Rosewood, rosewood-grained walnut, marquetry of various', 'rosewood'),
        ('Glass', 'glass'),
        ('Lithograph', 'lithograph'),
        ('48 leaves with drawings and sketches in graphite and in ink', 'drawings_and_sketches'),
        ('Mahogany, gilt gesso, eglomise tablets, white pine, tulip', 'mahogany'),
        ('Film negative', 'film_negative'),
        ('Albumen silver print from glass negative', 'albumen'),
        ('Faience', 'faience'),
        ('Silver', 'silver'),
        ('silk', 'silk'),
        ('Black and colored crayon on brown wove paper laid down to', 'black_and_colored_crayon'),
        ('Colored wax pencil and graphite on brown wove paper', 'colored_wax'),
        ('Woodcut', 'wood'),
        ('Cotton and wool; Doublecloth, woven on a hand-loom with a', 'cotton'),
        ('Mahogany and mahogany veneer', 'mahogany'),
        ('Quarter-sawn oak, oak veneer, cedar, mahogany, brass,', 'mahogany'),
        ('Graphite and colored wax pencil on brown wove paper', 'colored_wax'),
        ('Gold', 'gold'),
        ('Commercial color photolithograph', 'photolithograph'),
        ('Watercolor, gouache, and charcoal on off-white wove paper', 'watercolor_gouache'),
        ('Linen embroidered with wool and silk threads; decorated', 'silk'),
        ('Oil on canvas', 'on_canvas'),
        ('Commercial photolithograph', 'photolithograph'),
        ('Etching and engraving', 'etching'),
        ('Cotton', 'cotton'),
        ('Albumen silver print', 'albumen'),
        ('Wood', 'wood'),
        ('Graphite on light tan wove paper (recto);', 'graphite_on_light'),
        ('Hard-paste porcelain', 'porcelain'),
        ('cotton', 'cotton'),
        ('Woodblock print; ink and color on paper', 'wood'),
        ('Porcelain', 'porcelain'),
        ('Wood engraving', 'wood'),
        ('Indurated limestone', 'limestone'),
        ('Ceramic', 'ceramic'),
        ('Watercolor, gum arabic, and iron gall ink on off-white laid', 'watercolor'),
        ('wool', 'wool'),
        ('Bobbin lace', 'bobbin_lace'),
        ('Limestone', 'limestone'),
        ('Steel', 'steel'),
        ('Iron', 'iron'),
        ('Ivory', 'ivory'),
        ('[no medium available]', 'misc'),
        ('Hand-colored etching', 'etching'),
        ('Soft-paste porcelain', 'porcelain'),
        ('Limestone, ink', 'limestone'),
        ('Linen', 'linen'),
        ('Pottery', 'pottery'),
        ('Earthenware', 'earthenware'),
        ('Commercial lithograph', 'lithograph'),
        ('Pottery and ink, paint', 'pottery'),
        ('Color lithograph', 'lithograph'),
        ('Graphite', 'graphite'),
        ('Salted paper print from paper negative', 'salted_paper'),
        ('Silk / Compound weave', 'silk'),
        ('Silk and metal thread', 'silk'),
        ('Chromogenic print', 'chromogenic'),
        ('Brass', 'brass'),
        ('leather', 'leather'),
        ('Marble', 'marble'),
        ('Gilt bronze', 'bronze'),
        ('Copper alloy', 'copper'),
        ('Platinum print', 'print'),
        ('Photomechanical print', 'print'),
        ('Hand-colored lithograph', 'lithograph'),
        ('Photolithograph', 'photolithograph'),
        ('Ink on paper', 'ink'),
        ('Copper', 'copper'),
        ('Tin-glazed earthenware', 'earthenware'),
        ('Clay', 'clay'),
        ('Drypoint', 'drypoint'),
        ('Commercial Color Lithograph', 'commercial_color_lithograph'),
        ('Illustrations: wood engraving', 'wood'),
        ('Wool, linen; plain weave, tapestry weave', 'wool'),
        ('Wool', 'wool'),
        ('Graphite on paper', 'graphite'),
        ('Pen and black ink, watercolor and gouache with gum arabic', 'watercolor'),
        ('Watercolor on ivory', 'watercolor'),
        ('Illustrations: engraving', 'engraving'),
        ('Ink, opaque watercolor, and gold on paper', 'gold'),
        ('linen', 'linen'),
        ('Instant internal dye diffusion transfer print (Polaroid SX-70)', 'print'),
        ('Albumen silver prints', 'albumen'),
        ('Etching; only state', 'etching'),
        ('Lithograph; second state of two (Delteil)', 'lithograph'),
        ('Graphite on off-white wove paper', 'graphite'),
        ('Etching; second state of two', 'etching'),
        ('Glass, ceramic', 'glass'),
        ('Illustrations: lithography', 'lithograph'),
        ('Watercolor', 'watercolor'),
        ('Etching and aquatint', 'etching'),
        ('Relief print (wood or metal)', 'print'),
        ('Woodblock print (surimono); ink and color on paper', 'wood'),
        ('wool, silk', 'wool'),
        ('Engraving and etching', 'etching'),
        ('Limestone, paint', 'limestone'),
        ('Clay (unfired)', 'clay'),
        ('Pen and brown ink', 'ink'),
        ('Silver gilt', 'silver'),
        ('Silk on linen', 'linen'),
        ('Ceramic, pigment', 'ceramic'),
        ('Salted paper print', 'print'),
        ('Polychrome woodblock print; ink and color on paper', 'print'),
        ('Pen and black ink, watercolor and gouache', 'watercolor'),
        ('silk, metal', 'silk'),
        ('Etching; first state of two', 'etching'),
        ('Leather', 'leather'),
        ('Lithograph; second state of two (Armelhault & Bocher)', 'lithograph'),
        ('Blue faience', 'faience'),
        ('Hanging scroll; ink and color on paper', 'ink'),
        ('Hanging scroll; ink and color on silk', 'silk'),
        ('Maiolica (tin-glazed earthenware)', 'earthenware'),
        ('Bronze or copper alloy', 'bronze'),
        ('silk, cotton', 'cotton'),
        ('Pottery fragment with ink inscription', 'pottery'),
        ('Lithography', 'lithograph'),
        ('Watercolor on paper', 'watercolor'),
        ('Albumen silver print from paper negative', 'albumen'),
        ('Pressed glass', 'glass'),
        ('Lithograph on newsprint; second state of two (Delteil)', 'lithograph'),
        ('Pen and black ink', 'ink'),
        ('Hanging scroll; ink on paper', 'ink'),
        ('Illustrations: etching and engraving', 'engraving'),
        ('Etching and drypoint', 'etching'),
        ('Steel, gold', 'gold'),
        ('Faience (tin-glazed earthenware)', 'faience'),
        ('Pottery, ink', 'pottery'),
        ('Mahogany, gilt gesso, eglomise tablet, tulip poplar, white', 'mahogany'),
        ('Earthenware; glazed', 'earthenware'),
        ('Triptych of woodblock prints; ink and color on paper', 'wood'),
        ('Iron, copper', 'iron'),
        ('Screenprint', 'print'),
        ('Etching; first state of two (Lieure)', 'etching'),
        ('Gelatin silver prints', 'gelatin_silver'),
        ('Engraving; first state of two', 'engraving'),
        ('Lead-glazed earthenware', 'earthenware'),
        ('Ink and opaque watercolor on paper', 'watercolor'),
        ('Etching with drypoint', 'etching'),
        ('Copper-gold alloy (shakud≈ç), gold', 'gold'),
        ('Inkjet print', 'print'),
        ('Linen, wool', 'wool'),
        ('Watercolor over graphite', 'watercolor'),
        ('Limestone, paint (mostly modern)', 'limestone'),
        ('Commercial color lithograph with metal trim', 'commercial_color_lithograph'),
        ('Lacy pressed glass', 'glass'),
        ('Etching; second state of three', 'etching'),
        ('Woodblock print (nishiki-e); ink and color on paper', 'wood'),
        ('Pen and ink', 'ink'),
        ('Steel, wood', 'wood'),
        ('cotton, silk', 'silk'),
        ('Limestone; carved in relief', 'limestone'),
        ('Stipple engraving', 'engraving'),
        ('Parian porcelain', 'porcelain'),
        ('Printed book with woodcut illustrations', 'print'),
        ('Un-baked clay', 'clay'),
        ('Etching; first state of two (Pr√©aud)', 'etching'),
        ('Silver on base metal', 'silver'),
        ('Paper, silk', 'silk'),
        ('Mosaic glass', 'glass'),
        ('Pen and india ink on paper', 'ink'),
        ('Watercolor and gouache on off-white wove paper laid down on', 'watercolor'),
        ('Lithograph with tint stone', 'lithograph'),
        ('Silk, printed', 'print'),
        ('Earthenware, transfer-printed', 'earthenware'),
        ('Glazed earthenware', 'earthenware'),
        ('Dye transfer print', 'print'),
        ('Photomechanical prints', 'print'),
        ('Gouache over Graphite', 'graphite'),
        ('Linen, wool; tapestry weave', 'wool'),
        ('Commercial color lithography reproducing drawings', 'commercial_color_lithograph'),
        ('Engraving; second state of two', 'engraving'),
        ('Graphite on wove paper', 'graphite_on_wove_paper'),
        ('Porcelain painted in overglaze polychrome enamels', 'porcelain'),
        ('Printed felt', 'print'),
        ('leather, metal', 'leather'),
        ('etching', 'etching'),
        ('Illustrations: color lithography', 'lithograph'),
        ('Mahogany', 'mahogany'),
        ('Machine roll-printed', 'print'),
        ('Stained glass', 'glass'),
        ('Platinum-palladium print', 'print'),
        ('Watercolor and pencil on paper', 'watercolor'),
        ('Lithograph; second state of three (Armelhault & Bocher)', 'lithograph'),
        ('Silver (hammered), gilt', 'silver'),
        ('Engraving; second state of three', 'engraving'),
        ('Tempera on wood, gold ground', 'wood'),
        ('Steel, leather', 'steel'),
        ('Gold, enamel', 'gold'),
        ('Salted paper print from glass negative', 'glass'),
        ('Gelatin silver print from glass negative', 'gelatin_silver'),
        ('Blown glass', 'glass'),
        ('Camelid hair, cotton', 'cotton'),
        ('Porcelain painted in underglaze blue', 'porcelain'),
        ('Silver dye bleach print', 'print'),
        ('Etching and Engraving', 'etching'),
        ('Dark brown ink, black chalk, and incised lines', 'ink'),
        ('Wool, linen; tapestry weave', 'wool'),
        ('silk, leather', 'leather'),
        ('Engraving; first state', 'engraving'),
        ('charcoal, gouache and gold paint', 'gold'),
        ('Wrought iron', 'iron'),
        ('Engraving; first state of two (New Hollstein)', 'engraving'),
        ('Woodblock', 'wood'),
        ('Etching; second state', 'etching'),
        ('Papyrus and ink', 'ink'),
        ('Part of an album of woodblock prints (surimono); ink and color on paper', 'print'),
        ('Earthenware; incised decoration through white slip and coloring under transparent glaze', 'earthenware'),
        ('Gilt bronze, struck', 'bronze'),
        ('Ink, wash, on paper', 'ink'),
        ('Salt-glazed stoneware', 'stone'),
        ('Albumen silver print from glass negative with applied color', 'albumen'),
        ('Lithograph; third state of three (Delteil)', 'lithograph'),
        ('Pottery, paint', 'pottery'),
        ('Ink and graphite on paper', 'graphite'),
        ('Engraving and blackwork', 'engraving'),
        ('Copper-silver alloy (shibuichi), gold', 'gold'),
        ('Etching, printed in brown ink', 'etching'),
        ('Colorless glass', 'glass'),
        ('Sandstone', 'stone'),
        ('Iron alloy', 'iron'),
        ('Pen and brown ink, brush and brown wash', 'ink'),
        ('Color Lithograph', 'lithograph'),
        ('Watercolor and graphite on paper', 'watercolor'),
        ('plates: hand colored engraving', 'engraving'),
        ('Wool, silk', 'wool'),
        ('Album leaf; ink and color on silk', 'silk'),
        ('Printed book with engraved illustrations', 'print'),
        ('Etching; first state of three', 'etching'),
        ('silk, glass', 'glass'),
        ('Bobbin lace, point d\'Angleterre', 'bobbin_lace'),
        ('wood', 'wood'),
        ('Copper (hammered), gilt', 'copper'),
        ('Stone', 'stone'),
        ('Pot metal glass', 'glass'),
        ('Pen and black ink, watercolor and gouache with gum arabic and metallic ink', 'watercolor'),
        ('Black ink, gray wash', 'ink'),
        ('Lithograph; third state of three (Armelhault & Bocher)', 'lithograph'),
        ('Hand-colored albumen photograph', 'albumen'),
        ('leather, silk', 'silk'),
        ('Stonepaste; glazed', 'stonepaste'),
        ('Woodblock-printed book', 'wood'),
        ('Watercolor and graphite on off-white wove paper', 'watercolor'),
        ('Ink and wash', 'ink'),
        ('glass', 'glass'),
        ('plates: engraving', 'engraving'),
        ('Watercolor and ink', 'watercolor'),
        ('Woodcuts', 'wood'),
        ('metal, glass', 'glass'),
        ('Copper-gold alloy (shakud≈ç), gold, silver', 'gold'),
        ('wool, cotton', 'cotton'),
        ('Copper, gold, enamel', 'gold'),
        ('Steel engraving', 'engraving'),
        ('Gelatin silver print with applied color', 'gelatin_silver'),
        ('Ceramic, paint', 'ceramic'),
        ('silk, wool', 'wool'),
        ('Stonepaste; painted under transparent glaze', 'stonepaste'),
        ('Color lithography', 'lithograph'),
        ('Etching on zinc', 'etching'),
        ('Etching on chine coll√©', 'etching'),
        ('Etching, only state', 'etching'),
        ('Bronze, struck', 'bronze'),
        ('Woodblock printed book; ink and color on paper', 'wood'),
        ('Iron, gold, copper', 'gold'),
        ('Engraving; second state', 'engraving'),
        ('Engraving on zinc', 'engraving'),
        ('Steel, silver', 'silver'),
        ('Iron, gold', 'gold'),
        ('wool, leather', 'wool'),
        ('Copper (cast)', 'copper'),
        ('Favrile glass', 'glass'),
        ('linen, cotton', 'cotton'),
        ('Silk on cotton', 'cotton'),
        ('Etching and engraving; third state of three (Bocher)', 'etching'),
        ('Ceramic, slip, pigment', 'ceramic'),
        ('Etching and engraving; first state of two (New Hollstein)', 'etching'),
        ('Gilded copper', 'copper'),
        ('Etching and engraving; first state of two (Lieure)', 'etching'),
        ('Painted terracotta', 'terracotta'),
        ('Stonepaste; polychrome painted under transparent glaze', 'stonepaste'),
        ('Papyrus, ink', 'ink'),
        ('Pressed purple marble glass', 'glass'),
        ('Pen and black ink with watercolor, gouache, metallic ink and gum arabic', 'watercolor_gouache'),
        ('Graphite, watercolor, and crayon on paper', 'watercolor'),
        ('Wood; carved', 'wood'),
        ('Earthenware; unglazed', 'earthenware'),
        ('Engraving; second state of two (New Hollstein)', 'engraving'),
        ('Commercial lithographs with half-tone photograph', 'lithograph'),
        ('Free-blown glass', 'glass'),
        ('Pressed yellow glass', 'glass'),
        ('Graphite on wove paper with perforated linen tape adhered to left edge for binding.',
         'graphite_on_wove_paper'),
        ('Engraving; first state of three', 'engraving'),
        ('Etching, Aquatint', 'etching'),
        ('Illustrations: woodcut', 'wood'),
        ('Ink and watercolor', 'watercolor'),
        ('Albumen photograph, cabinet card', 'albumen'),
        ('Acrylic on canvas', 'on_canvas'),
        ('Handscroll; ink and color on silk', 'silk'),
        ('Engraving; first state of three (New Hollstein)', 'engraving'),
        ('Glass negative', 'glass'),
        ('Stonepaste; underglaze painted', 'stonepaste'),
        ('Wood, various materials', 'wood'),
        ('Cast iron', 'iron'),
        ('Wool (warp, weft and pile); symmetrically knotted pile', 'wool'),
        ('Pen and black and gray ink, graphite, black chalk', 'graphite'),
        ('silk, linen', 'linen'),
        ('Oil on paper, laid down on canvas', 'on_canvas'),
        ('Illustrations: engravings', 'engraving'),
        ('Graphite on tracing paper', 'graphite'),
        ('Painted enamel on copper, partly gilt', 'copper'),
        ('Copper, gilt', 'copper'),
        ('Lithograph on wove paper', 'lithograph'),
        ('Stainless steel', 'steel'),
        ('Stoneware', 'stone'),
        ('Earthenware; molded', 'earthenware'),
        ('Graphite and watercolor', 'watercolor'),
        ('Carbon print', 'print'),
        ('Wood engraving; proof', 'wood'),
        ('Linen and silk', 'silk'),
        ('Ink, watercolor and wash', 'watercolor'),
        ('Steel, brass', 'steel'),
        ('Cotton, camelid hair', 'cotton'),
        ('Lithograph on newsprint; third state of three (Delteil)', 'lithograph'),
        ('Stained Glass', 'glass'),
        ('Gelatin silver glass negative', 'gelatin_silver'),
        ('Printed illustration in color; proof', 'print'),
        ('Gum bichromate print', 'print'),
        ('Lithographic print with dark grey ink', 'lithograph'),
        ('Etching, hand-colored', 'etching'),
        ('Copper-silver alloy (shibuichi), gold, copper-gold alloy (shakud≈ç)', 'gold'),
        ('Silk and cotton', 'silk'),
        ('Black ink, on off-white wove paper', 'ink'),
        ('Enamel on copper', 'copper'),
        ('Cotton, silk', 'silk'),
        ('Folding fan mounted as an album leaf; ink and color on alum paper', 'ink'),
        ('Etching; first state of four', 'etching'),
        ('Etching; first state of two (Hollstein)', 'etching'),
        ('Clay, glazed', 'clay'),
        ('Engraving; third state of three', 'engraving'),
        ('Green faience', 'faience'),
        ('Etching; second state of four', 'etching'),
        ('gold', 'gold'),
        ('Tempera, ink, and metal leaf on parchment', 'ink'),
        ('Enameled copper', 'copper'),
        ('Tempera and gold on wood', 'gold'),
        ('leather, wood', 'wood'),
        ('Tempera on wood', 'wood'),
    ]

    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Start database mapping...')
    for folder_mapping in tqdm(list_mapping):
        df_met_metadata_values \
            = generate_art_class_column(df_met_metadata_values, folder_mapping[0], folder_mapping[1])
    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - End database mapping')

    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Save list of art_class distribution...')
    df_art_class_report = get_class_report(df_met_metadata_values, "art_class")
    df_art_class_report.to_csv('reports/art_class_report.csv', sep='|', index=None)

    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Flagging records based on image_url len...')
    df_met_metadata_values['len_image_url'] \
        = df_met_metadata_values['primaryImage'].str.len()

    df_met_metadata_images \
        = df_met_metadata_values[df_met_metadata_values['len_image_url'] > 0]

    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Qty images with URL: {df_met_metadata_images.shape[0]}')

    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Filter data')
    categories = ['misc', 'graphite_on_wove_paper', 'etching', 'terracotta', 'silk',
                  'albumen', 'commercial_color_lithograph', 'brown_and_black_ink',
                  'wood', 'mahogany', 'engraving', 'lithograph', 'cotton',
                  'gelatin_silver', 'glass', 'bronze', 'colored_wax',
                  'black_ink_wash', 'photolithograph', 'porcelain', 'rosewood',
                  'drawings_and_sketches', 'print', 'watercolor', 'film_negative',
                  'gold', 'faience', 'silver', 'wool', 'black_and_colored_crayon',
                  'ink', 'earthenware', 'limestone', 'on_canvas',
                  'watercolor_gouache', 'pottery', 'graphite', 'stone',
                  'graphite_on_light', 'copper', 'ceramic', 'linen', 'iron', 'steel',
                  'bobbin_lace', 'leather', 'ivory', 'clay', 'salted_paper',
                  'chromogenic', 'brass', 'marble', 'drypoint', 'stonepaste']

    df_limited_extraction = pd.DataFrame()
    df_met_metadata_images = df_met_metadata_images[['objectID', 'primaryImage', 'art_class']].drop_duplicates()

    for category in categories:
        df_limited_records = df_met_metadata_images[df_met_metadata_images['art_class'] == category].head(5000)
        df_limited_extraction = df_limited_extraction.append(df_limited_records)

    df_met_metadata_images = df_limited_extraction

    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Qty data to be extracted: {df_met_metadata_images.shape[0]}')

    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Recreate data folder')
    delete_folder(images_data_folder)

    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Create mapping folders...')
    for folder_mapping in tqdm(list_mapping):
        try:
            os.mkdir(images_data_folder + '/' + folder_mapping[1])
            logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Art Medium {folder_mapping[1]} created')
        except:
            pass

    qty_records = df_met_metadata_images.shape[0]
    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Total Images to be extracted {qty_records}')

    for index, row in df_met_metadata_images.iterrows():
        object_id = row.objectID
        image_url = row.primaryImage
        data_folder = row.art_class
        extention = image_url.split('.')[-1]
        unique_id = uuid.uuid4().hex
        file_path = PROJECT_DIR + '/images_data/' + data_folder + '/' + str(object_id) + f'_{unique_id}_.' + extention

        if (image_url != None) and (len(image_url) != 0):
            try:
                save_image_in_folder(image_url, file_path)
                logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Image from {image_url} - Saved at {file_path}')
            except Exception as e:
                logger.error(f'[ARTWORK-IMAGE-EXTRACTION] - Image {e} - Error. ')

        qty_records = qty_records - 1

        if qty_records % 1000 == 0:
            logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Remaining Images to be extracted {qty_records}')

    time_elapsed = datetime.now() - start_time
    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - End time: {datetime.now()}')
    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - Time elapsed (hh:mm:ss.ms) {time_elapsed}')
    logger.info(f'[ARTWORK-IMAGE-EXTRACTION] - End.')


if __name__ == '__main__':
    main()
