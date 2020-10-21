# -*- coding: utf-8 -*-

import argparse
import json
import logging
import os
import pickle
import numpy as np
from methods.train_classifier import TrainClassifier


def main():
    home_folder = os.getcwd()
    dataset_folder = 'output/dataset'
    model_output_folder = '../src/hub/model'

    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p',
                        level=logging.DEBUG)

    # TRAIN MODEL

    logging.info('Calling TrainClassifier')

    X = np.load(os.path.join(home_folder, dataset_folder, 'dataset.npy'))
    y = np.load(os.path.join(home_folder, dataset_folder, 'labels.npy'))

    train_classifier = TrainClassifier(X, y)
    performance, parameters, best_estimator = train_classifier.train()

    # SAVE

    logging.info('Saving model...')

    # Save performances
    with open(os.path.join(model_output_folder, 'performance.json'), 'w') as fp:
        json.dump(performance, fp)

    # Save parameters
    with open(os.path.join(model_output_folder, 'parameters.json'), 'w') as fp:
        json.dump(parameters, fp)

    # Save model
    with open(os.path.join(model_output_folder, 'model.pkl'), 'wb') as fp:
        pickle.dump(best_estimator, fp)


if __name__ == '__main__':
    main()
