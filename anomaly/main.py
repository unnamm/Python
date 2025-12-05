from PIL import Image
import os
import keras
import numpy
import tensorflow


def load_images(folder, target_size):
    images = []
    files = os.listdir(folder)
    for filename in files:
        filename = os.path.join(folder, filename)
        img = Image.open(filename).convert("RGB")
        if img.height > img.width:
            img = img.rotate(270, expand=True)

        half = img.crop((0, 0, img.width // 2, img.height))
        half = half.resize(target_size)
        half = numpy.array(half) / 255.0
        images.append(half)

        print(f"loading... {len(images)} / {len(files)}")

    return numpy.array(images)

def ssim_loss(y_true, y_pred):
    return 1 - tensorflow.reduce_mean(tensorflow.image.ssim(y_true, y_pred, max_val=1.0))


normal_images = load_images("train folder", (1024, 256))

input_img = keras.Input(shape=(256, 1024, 3))

# Encoder
x = keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same")(input_img)
x = keras.layers.MaxPooling2D((2, 2), padding="same")(x)
x = keras.layers.Conv2D(16, (3, 3), activation="relu", padding="same")(x)
encoded = keras.layers.MaxPooling2D((2, 2), padding="same")(x)

# Decoder
x = keras.layers.Conv2DTranspose(16, (3, 3), strides=2, activation="relu", padding="same")(encoded)
x = keras.layers.Conv2DTranspose(32, (3, 3), strides=2, activation="relu", padding="same")(x)
decoded = keras.layers.Conv2D(3, (3, 3), activation="sigmoid", padding="same")(x)

autoencoder = keras.Model(input_img, decoded)
autoencoder.compile(optimizer="adam", loss="mse")
autoencoder.fit(normal_images, normal_images, epochs=20, batch_size=32)
autoencoder.save("model.keras")
