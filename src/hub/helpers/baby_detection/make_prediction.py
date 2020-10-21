"""
Let's make a prediction!
"""

import os
import pickle
import sys
import warnings
from helpers.baby_detection.helpers.majority_voter import MajorityVoter
from helpers.baby_detection.helpers.feature_engineer import FeatureEngineer
from helpers.baby_detection.helpers.baby_cry_predictor import BabyCryPredictor
from helpers.baby_detection.helpers import Reader
from helpers.queues import UPDATED_WAVE_QUEUE
from helpers.logger import LOGGER

EGG_PATH = '{}/../lib/baby_cry_detection-1.1-py2.7.egg'.format(
    os.path.dirname(os.path.abspath(__file__)))
sys.path.append(EGG_PATH)

class Predictomatica:
    """
    Yes!
    """

    def __init__(self):
        self.__home_folder = os.getenv('HOME_DIR')
        self.__model_folder = os.getenv('MODEL_DIR')
        with open(os.path.join(self.__home_folder, self.__model_folder, 'model.pkl'), 'rb') as fp:
            self.model = pickle.load(fp)

    def predict(self):
        """
        SUPPOSEDLY this will run ML model predictions. We shall see...
        """

        LOGGER.info('Starting...')

        try:
            while True:
                file_name = UPDATED_WAVE_QUEUE.get()
                file_reader = Reader(file_name)
                play_list = file_reader.read_audio_file()

                engineer = FeatureEngineer()

                play_list_processed = list()

                for signal in play_list:
                    tmp = engineer.feature_engineer(signal)
                    play_list_processed.append(tmp)

                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=UserWarning)

                predictor = BabyCryPredictor(self.model)

                predictions = list()

                for signal in play_list_processed:
                    tmp = predictor.classify(signal)
                    predictions.append(tmp)

                LOGGER.info(f'Predictions: {predictions}')

                majority_voter = MajorityVoter(predictions)
                majority_vote = majority_voter.vote()

                LOGGER.info(f'Majority Vote: {majority_vote}')
        except Exception as ex:
            LOGGER.exception(ex)
            raise ex
