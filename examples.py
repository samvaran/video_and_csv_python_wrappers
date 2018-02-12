from csv_wrappers import * #we can use this line to import each class in the csv_wrappers file
from video_wrappers import * #and same for the video_wrappers file
import numpy as np #and of course our friends numpy
import cv2 #and opencv

### EXAMPLE 1 - Read a video filename from a CSV file, open it up and read the frames,
# apply a simple set of transformations to the image, and write our new images to disk as
# a modified video. Additionally, write a CSV file with some simple information about each frame
# of the video.

# Grab video filename from the 1st cell of 2D list created from CSV and preview it
sample_video_name = CsvReader.csv_to_list('example1.csv')[0][0]
print(sample_video_name)
VideoReader.preview_video_file(sample_video_name)

# Initialize instances of VideoReader, VideoWriter, and CsvWriter
vr = VideoReader()
vw = VideoWriter()
cw = CsvWriter()

# Open the video file we're reading from, and open the new video and CSV files we're creating on disk
vr.open_video(sample_video_name)
print(vr.get_video_info())
vw.open_video(sample_video_name[0:-4]+'_triple') #we'll make the video name be the same as the original, plus '_triple'
cw.open_csv(sample_video_name[0:-4]+'_triple', ['frame_avg', 'gray_avg', 'binary_avg']) #write the header row for the CSV

# Here is where the can_step method is useful - we don't have to worry about reading past the end
# of the number of frames that exist in the source video here - the method does that for us
while(vr.can_step()):
    frame = vr.step() #step forward once and grab the next frame from the video

    # RGB images like the frame variable are 3D arrays, of size Length x Width x 3 (one for each color channel)
    # Grayscale images are only 2D arrays, or Length x Width x 1, but to concatenate the arrays,
    # we'll need to project the grayscale image into the RGB space (ie. duplicate the color information across each channel)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert to grayscale
    gray = np.stack([gray]*3, -1) #cast the grayscale as a 3D array
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) #let's also get a binary threshold black and white image

    # Let's concatenate the images so they're all side by side and then add a new frame to the video we're writing
    new_frame = np.concatenate((frame, gray, binary), axis=1)
    vw.add_frame(new_frame)

    # We'll also get the mean value of each image (RGB, grayscale, and black/white) and write it as a row to our CSV
    frame_avg = np.mean(frame)
    gray_avg = np.mean(gray)
    binary_avg = np.mean(binary)
    cw.add_row([frame_avg, gray_avg, binary_avg])

# Once we're done, close the video we're reading from, and the two files we're writing
vr.close_video()
vw.close_video()
cw.close_csv()

# Now you can check your directory for the new '..._triple' video and CSV files and review the results!
