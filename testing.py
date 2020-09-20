from keras.models import load_model
from keras.preprocessing import image
import numpy as np
# from result_screen import ResultScreen
# from StartScreen import MainWindow




def check(path):
    # prediction
    model = load_model('diseaseClassification1.h5')

    img_rows, img_cols = 224, 224

    class_labels = [
        'eczema',
        'normal',
        'psoriasis'
    ]
    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x.astype('float32') / 255
    pred = np.argmax(model.predict(x))

    if class_labels[pred]=='psoriasis':
        global text
        text = "It's a psoriasis"
        # print('Its a psoriasis')

    else:
        if class_labels[pred]=='eczema':
            text="Its an eczema"
            # print('Its a eczema')
        else:
            text = "The skin is neither affected by eczema nor psoriasis"
            # print('The skin is neither affected by eczema nor psoriasis')

    print("It's a {}.".format(class_labels[pred]))
    print(class_labels[pred])
    # MainWindow.startResultWindow(text)



# check('data/psoriasis1.jpg')