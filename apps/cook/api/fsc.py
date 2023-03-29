from PIL import Image
import base64
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import os
from apps.cook.models import (
    FSCCatalogue,
    FSCCatalogueImage
)

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\venky\OneDrive\Desktop\Quytech\Cangurhu\Cangurhu\cangurhu_python\fsc.json"


def predict_image_object_detection_sample(
        project: str,
        endpoint_id: str,
        filename: str,
        object_id: str,
        id: str,
        location: str = "us-central1",
        api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    # client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    # client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # with open(filename, "rb") as f:
    #     file_content = f.read()
    #
    # # The format of each instance should conform to the deployed model's prediction input schema.
    # encoded_content = base64.b64encode(file_content).decode("utf-8")
    # instance = predict.instance.ImageObjectDetectionPredictionInstance(
    #     content=encoded_content,
    # ).to_value()
    # instances = [instance]
    # # See gs://google-cloud-aiplatform/schema/predict/params/image_object_detection_1.0.0.yaml for the format of the parameters.
    # parameters = predict.params.ImageObjectDetectionPredictionParams(
    #     confidence_threshold=0.5, max_predictions=5,
    # ).to_value()
    # endpoint = client.endpoint_path(
    #     project=project, location=location, endpoint=endpoint_id
    # )
    # response = client.predict(
    #     endpoint=endpoint, instances=instances, parameters=parameters
    # )
    # print("response")
    # print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_object_detection_1.0.0.yaml for the format of the predictions.
    # predictions = response.predictions
    predictions = {'displayNames': ['dirty_microwave_oven'], 'confidences': [0.832795203],
                   'ids': ['8177088316735225856'], 'bboxes': [[0.203493953, 0.862704039, 0.239147604, 0.638348758]]}

    # for prediction in predictions:
    #     print(" prediction:", dict(prediction))
    object_names = FSCCatalogue.objects.filter(id=object_id)
    print(predictions['displayNames'][0])
    for object_name in object_names:
        print(object_name.name)
        if predictions['displayNames'][0] == object_name.name:
            # FSCCatalogueImage.objects.update(status="Pass")
            print("pass")
            FSCCatalogueImage.objects.filter(id=id).update(status="Pass")
        else:
            print("fail")
            FSCCatalogueImage.objects.filter(id=id).update(status="Fail")

    # return predictions['displayNames']
    # print(object_names,object_name)
    return object_name
