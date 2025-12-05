from keras.models import load_model
from PIL import Image
import numpy
import matplotlib.pyplot as plt


def load_images(filename, target_size):
    images = []

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

    arr = numpy.array(images[0]) / 255.0
    return arr


def detect_anomaly(img, model, threshold=0.01):
    # 배치 차원 추가
    img_batch = numpy.expand_dims(img, axis=0)

    # 모델 복원 결과
    reconstructed = model.predict(img_batch)

    # MSE 계산
    mse = numpy.mean(numpy.square(img_batch - reconstructed))

    # threshold 기준으로 anomaly 여부 판단
    return mse > threshold, mse


def show_anomaly_result(img, model):
    # 입력 이미지 준비
    img_batch = numpy.expand_dims(img, axis=0)

    # 복원 이미지
    reconstructed = model.predict(img_batch)[0]

    # 오차 맵 (원본 - 복원)
    error_map = numpy.abs(img - reconstructed)

    # 시각화
    plt.figure(figsize=(12, 4))

    # 원본
    plt.subplot(1, 3, 1)
    plt.title("Original")
    plt.imshow(img)
    plt.axis("off")

    # 복원
    plt.subplot(1, 3, 2)
    plt.title("Reconstructed")
    plt.imshow(reconstructed)
    plt.axis("off")

    # 오차 맵
    plt.subplot(1, 3, 3)
    plt.title("Error Map")
    plt.imshow(error_map, cmap="hot")
    plt.axis("off")

    plt.show()


autoencoder = load_model("F:\\Python\\model.keras")
test_img = load_images("path", (256, 256))
is_anomaly, score = detect_anomaly(test_img, autoencoder, threshold=0.01)
print("Anomaly:", is_anomaly, "Score:", score)
show_anomaly_result(test_img, autoencoder)
