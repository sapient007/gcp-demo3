import re
import numpy as np
import pandas as pd

from google.api_core.client_options import ClientOptions
from google.cloud import automl_v1beta1


class Predictor(object):
    """
    TODO: description
    """

    def __init__(self, credentials, model_name):
        """
        TODO: description
        :param credentials:
        :param model_name:
        """

        self.model_name = model_name
        self.options = ClientOptions(api_endpoint='automl.googleapis.com')
        self.prediction_client = automl_v1beta1.PredictionServiceClient(
            credentials=credentials,
            client_options=self.options
        )

    def predict(self, text):
        """
        TODO: description
        :param text:
        :return:
        """

        rows = []
        for line in text:
            line = line.strip('\n')

            response = self.prediction_client.predict(
                self.model_name,
                {'text_snippet': {
                    'content': line,
                    'mime_type': 'text/plain'
                }},
                {})

            machine_score = np.nan
            native_score = np.nan
            transl_score = np.nan
            for result in response.payload:
                if re.search('machine', result.display_name):
                    machine_score = result.classification.score * 100
                if re.search('native', result.display_name):
                    native_score = result.classification.score * 100
                if re.search('translated', result.display_name):
                    transl_score = result.classification.score * 100

            rows.append({
                'native_score': native_score,
                'translated_score': transl_score,
                'machine_score': machine_score,
                'line': line
            })

        return pd.DataFrame(rows)
