"""
face_utils.py — ShopEase Facial Recognition Utilities

NOTE: Face recognition sirf local machine pe kaam karta hai jahan
opencv-python aur face-recognition install ho.
Server pe ENABLE_FACE_RECOGNITION=False set karo.
"""
import os
import pickle
from django.conf import settings


def _cv2_available():
    try:
        import cv2
        return True
    except ImportError:
        return False


def get_face_data_dir():
    path = os.path.join(settings.MEDIA_ROOT, 'face_data')
    os.makedirs(path, exist_ok=True)
    return path


def get_face_models_dir():
    path = os.path.join(settings.MEDIA_ROOT, 'face_models')
    os.makedirs(path, exist_ok=True)
    return path


def get_haar_cascade():
    import cv2
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        raise RuntimeError("Haar Cascade XML not found. Reinstall opencv-python.")
    return cascade


def capture_face_images(user_id, role, num_images=30):
    """Webcam se face images capture karo aur save karo."""
    if not _cv2_available():
        raise RuntimeError(
            "opencv-python install nahi hai. "
            "Run: pip install opencv-python"
        )

    import cv2
    import numpy as np

    cascade = get_haar_cascade()
    folder_name = f"{role}_{user_id}"
    save_dir = os.path.join(get_face_data_dir(), folder_name)
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError(
            "Webcam open nahi ho saka. "
            "Camera connected hai aur kisi aur app mein use nahi ho raha?"
        )

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    captured = 0
    max_attempts = 300

    try:
        while captured < num_images and max_attempts > 0:
            ret, frame = cap.read()
            if not ret:
                max_attempts -= 1
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

            if len(faces) == 0:
                max_attempts -= 1
                continue

            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
            face_roi = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            cv2.imwrite(os.path.join(save_dir, f"{captured:03d}.jpg"), face_roi)
            captured += 1
            max_attempts -= 1
    finally:
        cap.release()

    if captured < num_images:
        raise RuntimeError(
            f"Sirf {captured}/{num_images} images capture hui. "
            "Face clearly visible aur light theek honi chahiye."
        )

    return os.path.join('face_data', folder_name)


def train_face_model(role):
    """Registered faces ka LBPH model train karo."""
    if not _cv2_available():
        raise RuntimeError("opencv-python install nahi hai.")

    import cv2
    import numpy as np

    face_data_dir = get_face_data_dir()
    models_dir = get_face_models_dir()

    faces, labels, label_map = [], [], {}
    label_counter = 0
    prefix = f"{role}_"

    if not os.path.isdir(face_data_dir):
        raise RuntimeError(f"Face data directory nahi mili: {face_data_dir}")

    for folder in sorted(os.listdir(face_data_dir)):
        if not folder.startswith(prefix):
            continue
        try:
            user_id = int(folder[len(prefix):])
        except ValueError:
            continue

        folder_path = os.path.join(face_data_dir, folder)
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            continue

        label_map[label_counter] = user_id
        for img_file in image_files:
            img = cv2.imread(os.path.join(folder_path, img_file), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(cv2.resize(img, (200, 200)))
            labels.append(label_counter)
        label_counter += 1

    if not faces:
        raise RuntimeError(f"Role '{role}' ke liye koi face images nahi mili.")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, __import__('numpy').array(labels))
    recognizer.save(os.path.join(models_dir, f"{role}_model.yml"))

    with open(os.path.join(models_dir, f"{role}_labels.pkl"), 'wb') as f:
        pickle.dump(label_map, f)

    return {'trained': label_counter, 'model_path': os.path.join(models_dir, f"{role}_model.yml")}


def recognize_face(role, confidence_threshold=80):
    """Webcam se face detect karo aur user_id return karo."""
    if not _cv2_available():
        raise RuntimeError("opencv-python install nahi hai.")

    import cv2

    models_dir = get_face_models_dir()
    model_path = os.path.join(models_dir, f"{role}_model.yml")
    labels_path = os.path.join(models_dir, f"{role}_labels.pkl")

    if not os.path.exists(model_path):
        raise RuntimeError(f"Role '{role}' ka trained model nahi mila. Pehle face register karo.")
    if not os.path.exists(labels_path):
        raise RuntimeError(f"Role '{role}' ka label map nahi mila. Model dobara train karo.")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)

    with open(labels_path, 'rb') as f:
        label_map = pickle.load(f)

    cascade = get_haar_cascade()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Webcam open nahi ho saka.")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detected_user_id = None
    max_attempts = 60

    try:
        while max_attempts > 0:
            ret, frame = cap.read()
            if not ret:
                max_attempts -= 1
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

            if len(faces) == 0:
                max_attempts -= 1
                continue

            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
            face_roi = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            label, confidence = recognizer.predict(face_roi)

            if confidence < confidence_threshold:
                detected_user_id = label_map.get(label)
            break
    finally:
        cap.release()

    return detected_user_id
