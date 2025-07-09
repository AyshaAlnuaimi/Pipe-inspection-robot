from picamera2 import Picamera2
import time

# Initialize the camera
picam2 = Picamera2()

# Set max resolution (12MP)
config = picam2.create_still_configuration(main={"size": (4608, 2592)})
picam2.configure(config)

# Start camera
picam2.start()
time.sleep(2)  # Allow warm-up

# Capture 3 high-res images
for i in range(1, 4):
    filename = f"photo_{i}.jpg"
    picam2.capture_file(filename)
    print(f"✅ Saved: {filename}")
    time.sleep(1)

picam2.close()
