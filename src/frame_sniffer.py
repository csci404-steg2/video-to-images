from moviepy.editor import *

# local imports
from .handshake import HandshakeMeta, HandshakeColors
from.transmission_state_machine import TransmissionStateMachine

import random

class FrameSniffer:
    def __init__(self, clip: VideoFileClip):
        self._clip = clip

    def search_for_handshake(self):
        """search for a handshake in the provided clip
        returns:
            on valid handshake found, a HandshakeMeta dataclass and a list
            of relevant data frames
        raises:
            RuntimeError - no handshakes are found
        """
    
        candidiate_starting_timestamps = self._get_candidate_frame_indexes()

        if len(candidiate_starting_timestamps) < 1:
            raise RuntimeError("No handshakes found.")
        
        handshake_found = False
        for timestamp in candidiate_starting_timestamps:
            handshake_frames = self._check_handshake(timestamp)
            if handshake_frames:
                handshake_found = True
                break

        if not handshake_found
            raise RuntimeError("Handshake candidates tested but none valid.")

        return handshake_frames

    def _frame_number_to_timestamp(self, frame_number):
        """convert a frame index to a timestamp
        params:
            frame_number - index of a frame
        returns:
            string representing the timestamp of the given frame
        raises:
            ValueError - clip fps is leq 0, which shouldn't ever happen
        """
        # string time stamp is in the form hour:minute:second.ms
        clip_fps = self._clip.fps
        if clip_fps <= 0:
            raise ValueError("clip fps is 0, unable to determine a timestamp for the given clip")
        
        # beautiful
        frame_number_carved = frame_number
        hours = int(frame_number_carved / (60 * 60 * fps))
        frame_number_carved -= hours * (60 * 60 * fps)
        minutes = int(frame_number_carved / (60 * fps))
        frame_number_carved -= minutes * (60 * fps)
        seconds = int(frame_number / (fps))
        frame_number_carved -= seconds
        milliseconds = frame_number_carved

        return f"{hours}:{minutes}:{seconds}.{milliseconds}"

    def _get_frame_average_color(self, frame):
        """get the average color of the given frame
        params:
            frame - np array of rbg values
        returns:
            3 member tuple of the average value of the rgb values
        """
        total_colors = (0,0,0)
        total_pixels = self._clip.h * self._clip.w

        for pixel_row in frame:
            for pixel in pixel_row:
                average_colors += pixel

        return (
            int(total_colors[0] / total_pixels), 
            int(total_colors[1] / total_pixels),
            int(total_colors[2] / total_pixels))

    def _color_to_number(self, color):
        return (color[0] << 16) | (color[1] << 8) | (color[2] << 0) 

    def _get_candidate_frame_indexes(self):
        """get candidate starting positions, or more accurately, frame numbers
        of full black frames in the video
        """
        timestamps = []
        skip_frames = 0
        for frame_n, frame in enumerate(self._clip.iter_frames()):
            # genius
            if skip_frames > 0:
                skip_frams -= 1
                continue 

            average_color = self._get_frame_average_color(frame)

            if average_color == HandshakeColors.COLOR_DEAD_TIME:
                timestamps.append(
                    frame_n
                )
                skip_frames = self._clip.fps

        return timestamps

    def _get_frame_at(self, frame_index):
        """get the frame at a given frame index
        params:
            frame_index: index of frame to test
        returns:
            Frame at given index
        """
        return list(self._clip.iter_frames())[frame_index]

    def _handshake_time_to_frames(self, handshake_time):
        """convert a "handshake time," ie. a time passed by the handshake, to
        a number of frames that can be used to offset
        params:
            handshake_time: time from a handshake frame
        returns:
            number of frames that is equivalent
        """
        return int((handshake_time / 1000) * self._clip.fps)

    def _get_value_at_frame(self, frame_index):
        """get the "handshake value" at a given frame index, ie. the color
        making up the frame as a number
        params:
            frame_index: index of frame to test
        returns:
            Value of color
        """
        frame = self._get_frame_average_color(self, self._get_frame_at(frame_index))
        return self._color_to_number(frame)

    def _get_handshake_time_frames_at_frame(self, frame_index):
        """gets the "handshake time" at a given frame index, more or less to auto
        parse the value being passed by the handshake at the given frame as a 
        number of frames
        params:
            frame_index: index of frame to test
        returns:
            Number of frames conveyed by handshake at frame index
        """
        raw_number = self._get_value_at_frame(frame_index)
        return self._handshake_time_to_frames(raw_number)

    def _is_full_frame_color(self, frame_index):
        """check if the frame at the given index is comprised of only a single color
        (within a threashold)
        params:
            frame_index: index of frame to test
        returns:
            True on full frame color, false otherwise
        """
        frame = self._get_frame_at(frame_index)

        random_pixel = frame[random.randint(0, self._clip.h-1)][random.randint(0, self._clip.w-1)]
        threashold = 5 # color values must be within +-5

        for pixel_row in frame:
            for pixel in pixel_row:
                if (abs(pixel[0] - random_pixel[0]) > threashold) or 
                    (abs(pixel[1] - random_pixel[1]) > threashold) or 
                    (abs(pixel[2] - random_pixel[2]):
                    return False

        return True
        

    def _check_handshake(self, timestamp):
        """check if there is a handshake originating at the given frame index
        params:
            timestamp: frame index to start at
        returns:
            if a valid handshake is found, a hand shake and a list of relevant
            data frames is returned, None otherwise
        """
        # things to check for in order:
        # - 1s of full screen black (0x000000) 
        # - 1s of full screen dead time color 
        # - 1s of full screen alive time 
        # - 1s of offset time 
        # - 1s transmission length 
        # - wait offset time 
        # - [capture frame in alive window -> wait dead time]*transmission length 
        # - end capture

        # check for all black frame
        if self._get_frame_average_color(self, self._get_frame_at(timestamp)) != HandshakeColors.COLOR_DEAD_TIME:
            return None

        timestamp += self._clip.fps
        if not self._is_full_frame_color(timestamp):
            return None
        DEAD_TIME = _get_handshake_time_frames_at_frame(timestamp)
        timestamp += self._clip.fps
        if not self._is_full_frame_color(timestamp):
            return None
        ALIVE_TIME = _get_handshake_time_frames_at_frame(timestamp)
        timestamp += self._clip.fps
        if not self._is_full_frame_color(timestamp):
            return None
        OFFSET_TIME = _get_handshake_time_frames_at_frame(timestamp)
        timestamp += self._clip.fps
        if not self._is_full_frame_color(timestamp):
            return None
        TRANSMISSION_LENGTH = self._get_value_at_frame(timestamp)

        handshake = HandshakeMeta(DEAD_TIME, ALIVE_TIME, OFFSET_TIME, TRANSMISSION_LENGTH)

        timestamp += OFFSET_TIME
        frames = []
        for i in range(0, TRANSMISSION_LENGTH):
            frames.append(self._get_frame_at(timestamp))
            timestamp += (ALIVE_TIME + DEAD_TIME)

        return (handshake, frames)