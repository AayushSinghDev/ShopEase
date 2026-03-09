"""
face_utils.py — ShopEase Facial Recognition Utilities
Uses OpenCV LBPH Face Recognizer for face registration and login.

Functions:
  - capture_face_images(user_id, role)  → captures 30 webcam images & saves them
  - train_face_model(role)              → trains LBPH model on all registered faces
  - recognize_face(role)               → detects & predicts face from webcam
"""

import os
import cv2
import pickle
import numpy as np
from django.conf import settings


# ─── Paths ──────────────────────────────────────────────────────────────────

def get_face_data_dir():
    """Return and create base dir for face image datasets."""
    path = os.path.join(settings.MEDIA_ROOT, 'face_data')
    os.makedirs(path, exist_ok=True)
    return path


def get_face_models_dir():
    """Return and create base dir for trained face models."""
    path = os.path.join(settings.MEDIA_ROOT, 'face_models')
    os.makedirs(path, exist_ok=True)
    return path


def get_haar_cascade():
    """Return OpenCV Haar Cascade classifier for frontal face detection."""
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        raise RuntimeError(
            "Haar Cascade XML not found. Ensure opencv-python is installed correctly."
        )
    return cascade


# ─── Function 1: Capture Face Images ────────────────────────────────────────

def capture_face_images(user_id, role, num_images=30):
    """
    Open webcam, detect face, capture `num_images` grayscale face images,
    and save them to media/face_data/{role}_{user_id}/ folder.

    Returns:
        str: Relative folder path (stored in model's face_data field)

    Raises:
        RuntimeError: If webcam cannot be opened or face not detected consistently
    """
    cascade = get_haar_cascade()

    # Create save directory
    folder_name = f"{role}_{user_id}"
    save_dir = os.path.join(get_face_data_dir(), folder_name)
    os.makedirs(save_dir, exist_ok=True)

    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError(
            "Webcam could not be opened. "
            "Please ensure a camera is connected and not in use by another application."
        )

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    captured = 0
    max_attempts = 300  # Avoid infinite loop if face is never detected

    try:
        while captured < num_images and max_attempts > 0:
            ret, frame = cap.read()
            if not ret:
                max_attempts -= 1
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(80, 80)
            )

            if len(faces) == 0:
                max_attempts -= 1
                continue

            # Use the largest detected face
            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (200, 200))

            img_path = os.path.join(save_dir, f"{captured:03d}.jpg")
            cv2.imwrite(img_path, face_roi)
            captured += 1
            max_attempts -= 1

    finally:
        cap.release()

    if captured < num_images:
        raise RuntimeError(
            f"Only {captured}/{num_images} face images captured. "
            "Please ensure your face is clearly visible and well-lit, then try again."
        )

    # Return relative path for storage in model
    relative_path = os.path.join('face_data', folder_name)
    return relative_path


# ─── Function 2: Train Face Model ───────────────────────────────────────────

def train_face_model(role):
    """
    Read all registered face images for the given role,
    train an LBPH Face Recognizer, and save:
      - media/face_models/{role}_model.yml
      - media/face_models/{role}_labels.pkl  (maps label int → user_id)

    Returns:
        dict: {'trained': int (number of users), 'model_path': str}

    Raises:
        RuntimeError: If no face images are found for this role
    """
    face_data_dir = get_face_data_dir()
    models_dir = get_face_models_dir()

    faces = []
    labels = []
    label_map = {}  # label_int → user_id
    label_counter = 0

    # Scan all subfolders matching pattern: {role}_{user_id}
    prefix = f"{role}_"
    if not os.path.isdir(face_data_dir):
        raise RuntimeError(f"Face data directory not found: {face_data_dir}")

    for folder in sorted(os.listdir(face_data_dir)):
        if not folder.startswith(prefix):
            continue

        try:
            user_id = int(folder[len(prefix):])
        except ValueError:
            continue

        folder_path = os.path.join(face_data_dir, folder)
        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]

        if not image_files:
            continue

        label_map[label_counter] = user_id

        for img_file in image_files:
            img_path = os.path.join(folder_path, img_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, (200, 200))
            faces.append(img)
            labels.append(label_counter)

        label_counter += 1

    if not faces:
        raise RuntimeError(
            f"No face images found for role '{role}'. "
            "Please ensure at least one user has registered their face."
        )

    # Train LBPH recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))

    # Save model
    model_path = os.path.join(models_dir, f"{role}_model.yml")
    recognizer.save(model_path)

    # Save label map
    labels_path = os.path.join(models_dir, f"{role}_labels.pkl")
    with open(labels_path, 'wb') as f:
        pickle.dump(label_map, f)

    return {
        'trained': label_counter,
        'model_path': model_path,
    }


# ─── Function 3: Recognize Face ─────────────────────────────────────────────

def recognize_face(role, confidence_threshold=80):
    """
    Open webcam, capture one frame, detect face, and predict user_id
    using the trained LBPH model for the given role.

    Args:
        role (str): 'customer' or 'seller'
        confidence_threshold (int): Lower = stricter match. Default 80.

    Returns:
        int or None: user_id if recognized with confidence < threshold, else None

    Raises:
        RuntimeError: If model not found, webcam unavailable, or face not detected
    """
    models_dir = get_face_models_dir()
    model_path = os.path.join(models_dir, f"{role}_model.yml")
    labels_path = os.path.join(models_dir, f"{role}_labels.pkl")

    # Check if model exists
    if not os.path.exists(model_path):
        raise RuntimeError(
            f"No trained face model found for role '{role}'. "
            "Please register at least one face before using face login."
        )

    if not os.path.exists(labels_path):
        raise RuntimeError(
            f"Label map not found for role '{role}'. "
            "Please re-train the face model."
        )

    # Load model and label map
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)

    with open(labels_path, 'rb') as f:
        label_map = pickle.load(f)

    cascade = get_haar_cascade()

    # Open webcam and try to detect a face
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError(
            "Webcam could not be opened. "
            "Please ensure a camera is connected and not in use."
        )

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detected_user_id = None
    max_attempts = 60  # Try up to 60 frames (~2 seconds at 30fps)

    try:
        while max_attempts > 0:
            ret, frame = cap.read()
            if not ret:
                max_attempts -= 1
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(80, 80)
            )

            if len(faces) == 0:
                max_attempts -= 1
                continue

            # Use the largest detected face
            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (200, 200))

            label, confidence = recognizer.predict(face_roi)

            if confidence < confidence_threshold:
                user_id = label_map.get(label)
                detected_user_id = user_id
            break  # Got a face — either matched or not

    finally:
        cap.release()

    return detected_user_id
