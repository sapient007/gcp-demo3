# python predict.py IMG_20190115_185820_02_03.jpg glassy-groove-229013 ICN18736000583343382
#
# pip install google-cloud-automl google-auth google-auth-httplib2 google-api-python-client
# payload {
#  classification {
#    score: 0.997835338116
#  }
#  display_name: "partcarbon"
# }

import sys
import os
import time
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = '/Users/mikeevanoff/CarbonParts/glassy-groove-229013-76a499e48937.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

project_id = "glassy-groove-229013"
model_id = "ICN18736000583343382"

def get_prediction(content, project_id, model_id):
  prediction_client = automl_v1beta1.PredictionServiceClient(credentials=creds)

  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': content }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned

if __name__ == '__main__':

  path = '.'
  outfile=open('BatchOutput.txt','w')

  files = os.listdir(path)

  for image in files:

    print(image)
    sys.stdout.flush()

    if image.endswith('.jpg'):

      ff=open(image, 'rb')
      content = ff.read()
      pred = get_prediction(content, project_id,  model_id)

      print(pred)
      sys.stdout.flush()
      
      try:
        outfile.write("%s, %f, %s\n" % (image, pred.payload[0].classification.score, str(pred.payload[0].display_name)))
      except:
        print("Error occurred processing ", image)

      time.sleep(1)
