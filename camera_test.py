import cv2
import signal
import itertools

def get_camera(w=1280, h=720, fps=30):
    pipeline = (
        f"libcamerasrc ! "
        f"video/x-raw,format=NV12,width={w},height={h},framerate={fps}/1 ! "
        "videoconvert ! "
        "appsink drop=1 sync=false"
    )
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        raise RuntimeError("Could not open Pi-camera pipeline")
    return cap

def main():
    cap = get_camera()
    cv2.namedWindow("Pi Cam", cv2.WINDOW_AUTOSIZE)

    print("Live preview — press q to quit")
    for i in itertools.count():
        ok, frame = cap.read()
        if not ok:
            print("⚠️ lost frame"); break
        cv2.imshow("Pi Cam", frame)

        if i % 60 == 0:
            cv2.imwrite(f"/tmp/frame_{i}.jpg", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda *_: exit(0))
    main()
