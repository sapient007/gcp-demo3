# Predict if a sentence was written natively in English, professionally translated 
# or machine translated. 

import sys
import re

from google.api_core.client_options import ClientOptions
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2


if __name__ == '__main__':

  file_path  = '2b_translated.txt'
  model_name = "projects/261855689705/locations/us-central1/models/TCN7361261134285897728"

  options = ClientOptions(api_endpoint='automl.googleapis.com')
  prediction_client = automl_v1beta1.PredictionServiceClient(client_options=options)
  params = {}

  with open(file_path) as fp:

    content = fp.readline()

    print("native,transl,machine,sentence text")

    while content:
      content=content.strip('\n')

      response = prediction_client.predict(model_name, {'text_snippet': {'content': content, 'mime_type': 'text/plain'} }, params)

      for result in response.payload:
        if re.search('machine',    result.display_name):
	  machine_score=result.classification.score * 100
        if re.search('native',     result.display_name):
	  native_score=result.classification.score * 100
        if re.search('translated', result.display_name):
	  transl_score=result.classification.score * 100

      print("%4.1f,%4.1f,%4.1f,%s" % (native_score,transl_score,machine_score,content) )

      content = fp.readline()


    

       

