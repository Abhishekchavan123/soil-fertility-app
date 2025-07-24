import os
import numpy as np
from flask import Flask, request, render_template
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load your model
model = load_model(r"C:\Users\Admin\Downloads\soil_fertility_model.h5")

# Class labels
labels = sorted({
    'high': 0,
    'medium': 1,
    'low': 2,
}, key={
    'high': 0,
    'medium': 1,
    'low': 2,
}.get)

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(180, 180))
    img_array = image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    image_url = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Preprocess and predict
            img_tensor = preprocess_image(filepath)
            preds = model.predict(img_tensor)
            predicted_index = np.argmax(preds)
            prediction = labels[predicted_index]
            image_url = filepath

    return render_template('index.html', prediction=prediction, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
