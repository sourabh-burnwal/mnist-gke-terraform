import os

import aiofiles
import uvicorn
from fastapi import FastAPI, File, UploadFile

from config import project_config
from core.model import Classification

app = FastAPI(title=project_config["PROJECT_NAME"])

api_config = project_config["API"]
os.makedirs(api_config["static_dir"], exist_ok=True)

classification_model = Classification()
classification_model.load_pt_model(model_path=project_config["MODEL"]['pt_model_path'])


def api_response(status_code: int = 200, message: str = "", data=None):
    return {"status": status_code, "message": message, "data": data}


@app.post("/predict")
async def get_mnist_classification(
        image: UploadFile = File(...)
):
    try:
        # Saving the image into local directory
        image_path = f"{api_config['static_dir']}/{image.filename}"
        async with aiofiles.open(image_path, 'wb') as out_file:
            content = await image.read()
            await out_file.write(content)

        # Call the model inference
        prediction = classification_model.predict(image_path=image_path)

        # Remove the files which has been saved
        os.remove(image_path)
        return api_response(200, "Success", prediction)
    except Exception as ex:
        print("Exception occurred: ", ex)
        return api_response(500, "Error in API", str(ex))


if __name__ == '__main__':
    uvicorn.run("main:app", host=api_config['host'], port=api_config['port'], reload=api_config['reload'])
