from keras.models import load_model
import numpy as np
import tensorflow as tf


disease_config = {
    "brain_tumor" : {
        "model_path" : "",
        "classes" : [
            "notumor",       
            "meningioma",   
            "pituitary",     
            "glioma"
        ]
    },
    "bone_class" : {
        "model_path" : "",
        "classess" : [
            "fractured",
            "not fractured"
        ]
    },
    "lung_disease" : {
        "model_path" : "",
        "classes" : [
            "Bacterial Pneumonia",   
            "Corona Virus Disease"   
            "Normal",      
            "Tuberculosis",   
            "Viral Pneumonia"
        ]
    },
    "oral_disease" : {
        "model_path" : "",
        "classess" : [
            "Calculus",
            "Data caries",
            "Gingivitis",
            "Mouth Ulcer",
            "Tooth Discoloration",
            "hypodontia"
        ]
    },
    "skin_disease" : {
        "model_path" : "",
        "classess" : [
            "Eczema",
            "Melanoma",
            "Atopic Dermatitis",
            "Basal Cell Carcinoma",
            "Melanocytic Nevi (Moles)",
            "Benign Skin Tumors",
            "Psoriasis",
            "Seborrheic Keratosis",
            "Tinea (Ringworm)",
            "Warts and Molluscum Contagiosum"
        ]
    }
}

# for bytes
def prepare_image(image, image_size):
    image = tf.image.decode_jpeg(image, channels=3)

    image = tf.cast(image, tf.float32)
    image /= 255.0
    image = tf.image.resize(image, [image_size, image_size])

    image = np.expand_dims(image, axis=0)

    return image

def classify_using_bytes(image_bytes, disease_type, image_size):
    model_path = disease_config[disease_type]['model_path']
    class_labels = disease_config[disease_type]['classess']

    model = load_model(model_path, compile=False)
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    prediction = model.predict(prepare_image(image_bytes, image_size))
    index = np.argmax(prediction, axis=1)[0]

    class_name = class_labels[index]
    confidence_score = prediction[0][index]

    return {
        'class' : class_name,
        'score' : f'{confidence_score*100:02.2f}%'
    }
