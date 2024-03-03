from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import numpy as np
# from keras.preprocessing.image import load_img
# from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from keras.models import load_model

# Create your views here.

model = load_model(
    'C:/PBL5/SmartTrash/ai/model/fine_tunning_resnet50_model_custom_data.h5')
# Create your views here.


def index(request):
    return render(request, 'index.html')


def predict(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image_file')
        img = Image.open(image_file)
        img = img.resize((384, 384))
        img_array = np.array(img)
        test_img = np.expand_dims(img_array, axis=0)

        prediction = None
        percent_predict = None

        prediction_prob = model.predict(test_img)
        print(prediction_prob)
        if prediction_prob.any():
            if (prediction_prob[0][0] * 100) >= 80:
                prediction = "Glass"
                percent_predict = prediction_prob[0][0] * 100
            elif (prediction_prob[0][1] * 100) >= 80:
                prediction = "Metal"
                percent_predict = prediction_prob[0][1] * 100
            elif (prediction_prob[0][2] * 100) >= 80:
                prediction = "Plastic"
                percent_predict = prediction_prob[0][2] * 100
        print(prediction)
        print(percent_predict)
        return render(request, 'index.html', {'prediction': prediction, 'percent_predict': percent_predict})
    return HttpResponse("Lỗi rồi !!!!")
