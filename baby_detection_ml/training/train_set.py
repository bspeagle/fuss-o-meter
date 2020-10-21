# -*- coding: utf-8 -*-

import argparse
import logging
import os
import re
import timeit
import numpy as np
from methods import Reader
from methods.feature_engineer import FeatureEngineer


def main():
    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p',
                        level=logging.INFO)

    home_folder = os.getcwd()

    # if home_folder not like ('baby_detection_nl*'):
    #     logging.exception('Please run from baby_detection_nl directory.')
    #     exit()

    training_data_folder = 'data'
    dataset_output_folder = 'output/dataset'

    # READ FILES IN SUB-FOLDERS of training_data_folder and FEATURE ENGINEERING

    # list training_data_folder sub-folders
    regex = re.compile(r'^[0-9]')
    directory_list = [i for i in os.listdir(
        training_data_folder) if regex.search(i)]

    # initialize empty array for features
    X = np.empty([1, 18])

    # initialise empty array for labels
    y = []

    logging.info('Creating training set...')
    start = timeit.default_timer()

    # iteration on sub-folders
    for directory in directory_list:

        # Instantiate FeatureEngineer
        feature_engineer = FeatureEngineer(label=directory)

        file_list = os.listdir(os.path.join(
            home_folder, training_data_folder, directory))

        logging.info(f'File List: {file_list}')

        # iteration on audio files in each sub-folder
        for audio_file in file_list:
            logging.info(f'Audio File: {audio_file}')

            file_reader = Reader(os.path.join(
                training_data_folder, directory, audio_file))

            logging.info(f'File Reader: {file_reader.file_name}')

            data, sample_rate = file_reader.read_audio_file()
            avg_features, label = feature_engineer.feature_engineer(
                audio_data=data)

            X = np.concatenate((X, avg_features), axis=0)
            y.append(label)

    # X.shape is (401, 18) as I'm not using indexing. First line is made of zeros and is to be removed
    X = X[1:, :]

    stop = timeit.default_timer()
    logging.info(
        'Time taken for reading files and feature engineering: {0}'.format(stop - start))

    # Save to numpy binary format
    logging.info('Saving training set...')
    np.save(os.path.join(dataset_output_folder, 'dataset.npy'), X)
    np.save(os.path.join(dataset_output_folder, 'labels.npy'), y)

    logging.info('Saved! {0}'.format(
        os.path.join(dataset_output_folder, 'dataset.npy')))
    logging.info('Saved! {0}'.format(
        os.path.join(dataset_output_folder, 'labels.npy')))


if __name__ == '__main__':
    main()
