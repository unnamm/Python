from keras.models import load_model
from PIL import Image
import numpy
import matplotlib.pyplot as plt
import keras
import tensorflow

@keras.saving.register_keras_serializable()
def ssim_loss(y_true, y_pred):
    return 1 - tensorflow.reduce_mean(tensorflow.image.ssim(y_true, y_pred, max_val=1.0))


def load_images(filename, target_size):
    img = Image.open(filename).convert("RGB")
    if img.height > img.width:
        img = img.rotate(270, expand=True)

    half = img.crop((0, 0, img.width // 2, img.height))
    half = half.resize(target_size)

    arr = numpy.array(half) / 255.0
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


def visualize_anomaly(img, model):

    # 입력 이미지 준비
    img_batch = numpy.expand_dims(img, axis=0)

    # 복원 이미지
    reconstructed = model.predict(img_batch)[0]

    # 차이 계산 (픽셀 단위)
    diff = numpy.abs(img - reconstructed)

    # 채널 평균 → 단일 값으로 변환
    diff_map = numpy.mean(diff, axis=-1)

    # 시각화: 원본 이미지 + 히트맵 오버레이
    plt.figure(figsize=(8, 6))
    plt.imshow(img.astype(numpy.uint8))  # 원본 이미지
    plt.imshow(diff_map, cmap="jet", alpha=0.5)  # 히트맵 겹치기
    plt.colorbar(label="Anomaly intensity")
    plt.axis("off")
    plt.show()


autoencoder = load_model("F:\\Python\\model.keras")
test_img = load_images("test image file.jpg", (1024, 256))

img_batch = numpy.expand_dims(test_img, axis=0)
reconstructed = autoencoder.predict(img_batch)
mse = numpy.mean(numpy.square(img_batch - reconstructed))

print("Score", mse)

visualize_anomaly(test_img, autoencoder)
