from pypylon import pylon
import cv2
import time
import os

def main():
    # Initialize the camera
    serial_number = "XXXXXXXXXX"  # Replace XXXXXXXXXX with the serial number of your GigE camera
    info = pylon.DeviceInfo()
    info.SetSerialNumber(serial_number)
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))
    camera.Open()
    
    # Set camera parameters
    camera.AcquisitionMode.SetValue("Continuous")
    
    # Set frame rate to 10 fps
    camera.AcquisitionFrameRateEnable.SetValue(True)
    camera.AcquisitionFrameRate.SetValue(10)
    
    camera.PixelFormat.SetValue("BGR8")
    
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    
    # Define video codec and output video file
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    # Specify the USB drive's path
    usb_drive_path = '/media/user/USB'
    if not os.path.exists(usb_drive_path):
        print("Error: USB drive path does not exist.")
        return
    
    # Check if the USB drive is writable
    if not os.access(usb_drive_path, os.W_OK):
        print("Error: USB drive is not writable.")
        return
    
    # Initialize the VideoWriter object for the video file
    output_file = os.path.join(usb_drive_path, 'output.avi')
    out = cv2.VideoWriter(output_file, fourcc, 10, (camera.Width.GetValue(), camera.Height.GetValue()))
    
    # Set up directory for saving images
    image_dir = os.path.join(usb_drive_path, 'images')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    start_time = time.time()
    duration = 60  # Duration of the video in seconds
    frame_count = 0

    while time.time() - start_time < duration:
        # Grab a frame from the camera
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grab_result.GrabSucceeded():
            # Convert the grabbed frame to OpenCV format
            image = grab_result.Array
            
            # Show the live feed
            cv2.imshow('Live Feed', image)
            
            # Write the frame to the output video file
            out.write(image)
            
            # Save the frame as a JPG image
            image_filename = os.path.join(image_dir, f"frame_{frame_count:05d}.jpg")
            cv2.imwrite(image_filename, image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])  # JPEG quality set to 95
            frame_count += 1
            
            # Check for key press to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        grab_result.Release()
    
    # Release the camera and close the output video file
    camera.StopGrabbing()
    camera.Close()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
