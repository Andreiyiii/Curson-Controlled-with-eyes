import math

ear_history = []  # smoothing pentru EAR

def get_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def detect_blink(landmarks, threshold=0.2, ear_window=5):
    if not landmarks:
        return False

    #MediaPipe Face Mesh
    p_stanga = (landmarks[33].x, landmarks[33].y)
    p_dreapta = (landmarks[133].x, landmarks[133].y)

    p_sus_1 = (landmarks[160].x, landmarks[160].y)
    p_jos_1 = (landmarks[144].x, landmarks[144].y)

    p_sus_2 = (landmarks[158].x, landmarks[158].y)
    p_jos_2 = (landmarks[153].x, landmarks[153].y)

    dist_vert_1 = get_distance(p_sus_1, p_jos_1)
    dist_vert_2 = get_distance(p_sus_2, p_jos_2)
    dist_oriz = get_distance(p_stanga, p_dreapta)

    if dist_oriz == 0:
        return False

    # eye aspect ratio
    ear = (dist_vert_1 + dist_vert_2) / (2.0 * dist_oriz)

    # average of ear
    global ear_history
    ear_history.append(ear)
    if len(ear_history) > ear_window:
        ear_history.pop(0)
    
    smooth_ear = sum(ear_history) / len(ear_history)

    # blinking logic on smooth_ear
    return smooth_ear < threshold

def get_eye_coordinates(landmarks, frame_shape, gain_x=1.0, gain_y=1.0):
    if not landmarks or len(landmarks) <= 477:
        return None, None

    iris_indices = [474, 475, 476, 477]
    iris_x = sum(landmarks[idx].x for idx in iris_indices) / len(iris_indices)
    iris_y = sum(landmarks[idx].y for idx in iris_indices) / len(iris_indices)

    # we get eye coordinates then multiply with screen resolution
    screen_w, screen_h = 1920, 1080
    
    raw_x = int(iris_x * screen_w)
    raw_y = int(iris_y * screen_h)

    #faster movements
    center_x = screen_w // 2
    center_y = screen_h // 2
    raw_x = int(center_x + (raw_x - center_x) * gain_x)
    raw_y = int(center_y + (raw_y - center_y) * gain_y)

    raw_x = max(0, min(screen_w - 1, raw_x))
    raw_y = max(0, min(screen_h - 1, raw_y))

    return raw_x, raw_y