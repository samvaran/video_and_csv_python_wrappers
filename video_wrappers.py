import cv2 #we will use OpenCV version 3.3 here
import numpy as np #and numpy of course

# The VideoReader class gives us some simple tools to open a video file from disk and step through
# it's contents frame by frame until we reach the end. It also has tools to extract metadata info
# from the video and preview the video file before opening it
class VideoReader:
    # This class method can be called without instantiating an instance of the VideoReader class
    # With it you can preview the video - it will play in a little window and then close itself
    def preview_video_file(name):
        video = cv2.VideoCapture(name) #open the video file
        video_num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) #get the total number of frames
        for i in range(video_num_frames):
            ret, frame = video.read() #read the next frame
            cv2.imshow('frame', frame) #show the frame quickly
            cv2.waitKey(10)
        video.release()
        cv2.destroyAllWindows() #close out the window

    def __init__(self):
        self.i = None #we'll use this to keep track of what frame we're on
        self.current_frame = None #this variable will store the current, most recent frame we read
        self.previous_frames_size = 5 #we will also keep a queue of the previous n frames
        self.previous_frames = [None] * self.previous_frames_size #this queue will be helpful if your use case needs previous frames
        self.video = None
        self.video_length = None
        self.video_height = None
        self.video_width = None
        self.video_fps = None
        self.video_num_frames = None

    # This method tells us if we can grab the next frame or if we've reached the end of the video
    # This will make looping once over all frames very easy when using this class, since you can use
    # this method in a while loop (see example code)
    def can_step(self):
        if self.video != None and self.i < self.video_num_frames:
            return True
        return False

    # Given filename, open the video file that exists on disk and extract all relevant metadata
    def open_video(self, name):
        if self.video != None:
            print('Video is already open!')
            return
        self.name = name
        self.video = cv2.VideoCapture(self.name) #uses opencv to open a video stream from the file
        self.video_num_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)) #extract metadata
        self.video_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_fps = self.video.get(cv2.CAP_PROP_FPS)
        self.video_length = self.video_num_frames / float(self.video_fps)
        self.i = 1
        print(str(self.video_width) + 'x' + str(self.video_height) + ' @ ' + str(self.video_fps) + ' for ' + str(self.video_num_frames) + ' frames or ' + str(self.video_length) + ' seconds')

    # Close Video file once done and reset the VideoWriter class instance for use on the next task
    def close_video(self):
        if self.video == None:
            print('No video currently open!')
        else:
            self.video.release()
            self.__init__()
            print('Video closed')

    # Call this method to step forward and read a new frame from the video file
    # It will take the previous 'current frame' and push it in the queue, while popping out the
    # oldest frame from the queue. It will then take the newest frame and put it in 'current_frame'
    def step(self):
        if self.video == None:
            print('No video currently open!')
            return
        if self.can_step == False:
            print('Reached end of video!')
            return
        self.previous_frames.pop(0) #pop oldest frame from end of queue
        self.previous_frames.append(self.current_frame) #append the 'current frame' to the queue
        ret, self.current_frame = self.video.read() #read latest frame from video file and store it
        self.i = self.i + 1 #and keep track of how many frames we've seen
        return self.current_frame #finally, return the frame you just read from disk for use in your code

    # Quick little helper method to export a dictionary of the video's metadata
    def get_video_info(self):
        info = { 'name': self.name,
                 'length': self.video_length,
                 'width': self.video_width,
                 'height': self.video_height,
                 'num_frames': self.video_num_frames,
                 'fps': self.video_fps }
        return info

# Class VideoWriter helps you take a bunch of images (of the same size of course) and save them
# as an AVI video to disk, using OpenCV
class VideoWriter:
    def __init__(self):
        self.name = None
        self.video_width = None
        self.video_height = None
        self.video_fps = None
        self.video = None
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # Get ready to open a new video file on disk with the given name
    # You can specify an FPS or use the default 29.97fps
    # Note: we don't ACTUALLY create a new video file on disk yet, since we need the pixel dimensions
    # and we don't have them yet. To improve usability, we'll grab the dimensions and use them to
    # initialize the video file once the class receives it's first image frame
    def open_video(self, name, fps=float(29.97)):
        if self.name != None:
            print('Video is already open!')
            return
        if name[-4:] != '.avi': #if the desired filename doesn't end in '.avi', add it to the name
            name = name + '.avi'
        self.name = name
        self.video_fps = fps

    # Every time you want to add a new frame to the video, you can call this method
    def add_frame(self, frame):
        if self.name == None:
            print('No video currently open!')
            return
        if self.video == None: #here is where we will check to see if we've made a new video file or not
            dims = np.shape(frame) #if not, we'll automatically grab pixel dimensions based on first input image
            self.video_height = dims[0]
            self.video_width = dims[1]
            self.video = cv2.VideoWriter(self.name, self.fourcc, self.video_fps, (self.video_width, self.video_height))
        self.video.write(frame) #and then create a new video on disk using OpenCV's VideoWriter class and necessary metadata

    # Close Video file once done and reset the VideoWriter class instance for use on the next task
    def close_video(self):
        if self.name == None:
            print('No video currently open!!')
            return
        self.video.release() #close video file on disk
        self.__init__()
        print('Video closed')
