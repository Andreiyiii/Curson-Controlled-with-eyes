import cv2
import time
import eye_tracker     
import mouse_control    
import utils           
import config         

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("no camera found")
        return

    print("Press ESC to cancel")
    last_click_time = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        landmarks = eye_tracker.get_landmarks(frame)

        if landmarks:
            # find where you look
            x, y = utils.get_eye_coordinates(
                landmarks,
                frame.shape,
                gain_x=config.CURSOR_GAIN_X,
                gain_y=config.CURSOR_GAIN_Y,
            )
            
            #move mouse
            if x is not None and y is not None:
                mouse_control.move(x, y)

            #blinking click
            if utils.detect_blink(landmarks, threshold=config.EAR_THRESHOLD, ear_window=config.EAR_SMOOTHING_WINDOW):
                now = time.monotonic()
                if now - last_click_time >= config.CLICK_COOLDOWN_SECONDS:
                    mouse_control.click()
                    last_click_time = now

            eye_tracker.draw_landmarks(frame, landmarks)

        cv2.imshow("Eye Tracker", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()