import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

refine_landmarks = True

face_mesh_instance = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def get_landmarks(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = face_mesh_instance.process(rgb_frame)
    if results.multi_face_landmarks:
        return results.multi_face_landmarks[0].landmark
    
    return None

def draw_landmarks(frame, landmarks):
    if not landmarks:
        return
    ih, iw, _ = frame.shape

    ochiul_stang_index = 362, 385, 387, 263, 373, 380
    ochiul_drept_index = 33, 160, 158, 133, 153, 144
    
    iris_stang_index = 474, 475, 476, 477
    iris_drept_index = 469, 470, 471, 472

    toate_punctele_interesante = ochiul_stang_index + ochiul_drept_index + iris_stang_index + iris_drept_index

    for idx in toate_punctele_interesante:
        landmark = landmarks[idx]
        x = int(landmark.x * iw)
        y = int(landmark.y * ih)
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)