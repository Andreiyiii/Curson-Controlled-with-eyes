import cv2
import eye_tracker      # Modulul tău pentru MediaPipe
import mouse_control    # Modulul tău pentru PyAutoGUI
import utils            # Modulul tău pentru calcule (EAR)
import config           # Fișierul tău de setări

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("no camera found")
        return

    print("Press ESC to cancel")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        landmarks = eye_tracker.get_landmarks(frame)

        if landmarks:
            # find where you look
            x, y = utils.get_gaze_coordinates(landmarks, frame.shape)
            
            #move mouse
            mouse_control.move(x, y)

            #blinking click
            if utils.detect_blink(landmarks, threshold=config.EAR_THRESHOLD):
                mouse_control.click()
                #sleep maybe

            eye_tracker.draw_landmarks(frame, landmarks)

        cv2.imshow("Eye Tracker", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()