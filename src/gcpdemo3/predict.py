import re
import numpy as np
import pandas as pd

from google.api_core.client_options import ClientOptions
from google.cloud import automl_v1beta1


class Predictor(object):
    """
    Predictor object for model predictions
    """

    def __init__(self, credentials, model_name):
        """
        Create predictor object
        :param credentials: credential object for AutoML
        :param model_name: deployed model name in GCP
        """

        self.model_name = model_name
        self.options = ClientOptions(api_endpoint='automl.googleapis.com')
        self.prediction_client = automl_v1beta1.PredictionServiceClient(
            credentials=credentials,
            client_options=self.options
        )

    def predict(self, text_df):
        """
        Predict text using deployed model
        :param text_df: DataFrame containing lines of text and labels
        :return: DataFrame with predictions
        """

        rows = []
        for row in text_df.itertuples():
            line = row.line
            label = row.label

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
                'label': label,
                'native_score': native_score,
                'translated_score': transl_score,
                'machine_score': machine_score,
                'line': line
            })

        return pd.DataFrame(rows)
