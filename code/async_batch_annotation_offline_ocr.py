import io
import os

from google.cloud import vision_v1

from os import listdir
import proto
from google.cloud import storage
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/Users/example/Documents/Project/ServiceAccountTolken.json"

def loadImages(path):
    # return array of bytes

    imagesList = listdir(path)
    loadedImages = []

    for image in imagesList:
        with io.open(path+image, 'rb') as image:
            content = image.read()
        loadedImages.append(content)

    return loadedImages

path = "/Users/joshvirnarula/snapwrite/testing_dataset/snapwrite_testdataset/Sentence Testing"

# your images in an array
contents = loadImages(path)

def batch_annotate(
    contents = contents,
):
    """Perform async batch image annotation."""
    client = vision_v1.ImageAnnotatorClient()

    bucket_name = "image_data"
    destination_blob_name = "response.json"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    requests = []

    for content in contents:
        image = {"content": content}
        features = [
            {"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION},
        ]
        requests.append({"image": image, "features": features})

    response = client.batch_annotate_images(requests=requests,)
    to_text = proto.Message.to_json(response) # convert object to text

    # uncomment if you want to save the response to your local directory
    f = open('response.json', 'w')
    for data in to_text:
        f.write(data)
    f.close()

    file_obj = io.StringIO(to_text)
    file_obj.seek(0)
    blob.upload_from_file(file_obj)

batch_annotate()
