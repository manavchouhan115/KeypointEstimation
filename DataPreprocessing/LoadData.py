import numpy as np
import cv2
import pandas as pd

def load_data(excel_path, image_dir):
    df = pd.read_excel(excel_path)
    images = []
    labels = []
    classification_labels = []
    coordinates_labels = []

    for _, row in df.iterrows():
        img_path = f"{image_dir}/{row['image_name']}"
        image = cv2.imread(img_path)
        image = cv2.resize(image, (224, 224))  # Resize for MobileNetV2

        # Append images and corresponding stick coordinates (or None if missing)
        #images.append(image)
        #label = [row['small_start_x'], row['small_start_y'], row['small_end_x'], row['small_end_y'],
        #         row['big_start_x'], row['big_start_y'], row['big_end_x'], row['big_end_y']]
        #labels.append(label)
        images.append(image)

        # Determine classification label
        small_stick_present = not pd.isnull(row['small_start_x'])
        big_stick_present = not pd.isnull(row['big_start_x'])

        classification_labels.append([int(small_stick_present), int(big_stick_present)])

        #Normalizing the coordinates
        coordinates = [
            (row['small_start_x'] * 224) / 1920 if not pd.isnull(row['small_start_x']) else 0,
            (row['small_start_y']* 224) / 1080 if not pd.isnull(row['small_start_y']) else 0,
            (row['small_end_x']* 224) / 1920 if not pd.isnull(row['small_end_x']) else 0,
            (row['small_end_y']* 224) / 1080 if not pd.isnull(row['small_end_y']) else 0,
            (row['big_start_x']* 224) / 1920 if not pd.isnull(row['big_start_x']) else 0,
            (row['big_start_y']* 224) / 1080 if not pd.isnull(row['big_start_y']) else 0,
            (row['big_end_x']* 224) / 1920 if not pd.isnull(row['big_end_x']) else 0,
            (row['big_end_y']* 224) / 1080 if not pd.isnull(row['big_end_y']) else 0
        ]
        coordinates_labels.append(coordinates)

    return np.array(images), np.array(classification_labels), np.array(coordinates_labels)

images, classification_labels, coordinates_labels = load_data('/content/drive/My Drive/imageAndLabels.xlsx', '/content/drive/My Drive/filtered_images')

# Normalize images and handle missing labels (replace missing values with 0 or other logic)
images = images / 255.0