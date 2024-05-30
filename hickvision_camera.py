import cv2
import time
import os




def setup_video_capture(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Could not open video stream")
        exit()
    return cap

def setup_output_path(usb_drive_path):
    if not os.path.exists(usb_drive_path):
        print("Error: USB drive path does not exist.")
        return None
    if not os.access(usb_drive_path, os.W_OK):
        print("Error: USB drive is not writable.")
        return None
    return usb_drive_path

def get_video_writer_gstreamer(output_file, fps, frame_width, frame_height):
    gst_pipeline = (
        f'appsrc ! videoconvert ! omxh264enc ! matroskamux ! filesink location={output_file}'
    )
    return cv2.VideoWriter(gst_pipeline, cv2.CAP_GSTREAMER, 0, fps, (frame_width, frame_height))

def add_timestamp_to_frame(frame, frame_width, frame_height):
    raw_timestamp = int(time.time())
    cv2.putText(frame, str(raw_timestamp), (frame_width - 200, frame_height - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    return frame

def main():
    # Configuration
    rtsp_url = "rtsp://admin:IskCamera315_1@192.168.1.64:554/Streaming/Channels/101"
    usb_drive_path = '/media/user/USB'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    screen_width, screen_height = 1366, 768  # Monitor dimensions
    duration = 60  # Duration of each video segment in seconds

    # Setup
    cap = setup_video_capture(rtsp_url)
    output_path = setup_output_path(usb_drive_path)
    if not output_path:
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 FPS if not available

    while True:
        filename_timestamp = time.strftime("%Y-%m-%d")
        output_file = os.path.join(output_path, f'output_{filename_timestamp}.avi')
        out = get_video_writer_gstreamer(output_file, fps, frame_width, frame_height)

        start_time = time.time()

        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame = add_timestamp_to_frame(frame, frame_width, frame_height)
            out.write(frame)

            resized_frame = cv2.resize(frame, (screen_width, screen_height))
            cv2.imshow('Hikvision Live Stream', resized_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        out.release()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
