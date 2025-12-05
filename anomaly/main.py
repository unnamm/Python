from PIL import Image
import os
import keras
import numpy


def load_images(folder, target_size):
    images = []
    files = os.listdir(folder)
    for filename in files:
        filename = os.path.join(folder, filename)
        img = Image.open(filename)
        if img.height > img.width:
            img = img.rotate(270, expand=True)

        half = img.crop((0, 0, img.width // 2, img.height))

        tile_width = half.width // 3

        for i in range(3):
            x0 = i * tile_width
            x1 = (i + 1) * tile_width
            crop = half.crop((x0, 0, x1, img.height))

            crop = crop.resize(target_size)
            images.append(crop)

        print(f"loading... {len(images)//3} / {len(files)}")

    return numpy.array(images)


normal_images = load_images("image folder", (256, 256))

input_img = keras.Input(shape=(256, 256, 3))

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
autoencoder.fit(normal_images, normal_images, epochs=5, batch_size=32)
autoencoder.save("model.keras")
