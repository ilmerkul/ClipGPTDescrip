import cv2
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt


class Configs:
    USE_LOCAL_MAXIMA = True

    len_window = 10

    max_frames_in_chunk = 2500
    window_type = "hanning"


class KFPropose:
    def __init__(self):
        self.USE_LOCAL_MAXIMA = Configs.USE_LOCAL_MAXIMA
        self.len_window = Configs.len_window
        self.max_frames_in_chunk = Configs.max_frames_in_chunk

    def __calculate_frame_difference(self, curr_frame, prev_frame):
        if curr_frame is not None and prev_frame is not None:
            diff = cv2.absdiff(curr_frame, prev_frame)
            count = np.sum(diff)

            return count
        return None

    def __process_frame(self, frame, prev_frame, frame_diffs, frames):
        curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        frame_diff = self.__calculate_frame_difference(curr_frame, prev_frame)

        if frame_diff is not None:
            frame_diffs.append(frame_diff)
            frames.append(frame)

        return curr_frame

    def __extract_all_frames_from_video__(self, path):
        cap = cv2.VideoCapture(str(path))

        while True:
            prev_frame = None

            frame_diffs = []
            frames = []
            ret, frame = cap.read()
            for _ in range(0, self.max_frames_in_chunk):
                if not ret:
                    yield frames, frame_diffs
                    cap.release()
                    return
                prev_frame = self.__process_frame(frame, prev_frame, frame_diffs, frames)
                ret, frame = cap.read()

            yield frames, frame_diffs

        cap.release()

    def __get_frames_in_local_maxima__(self, frames, frame_diffs):
        diff_array = np.array(frame_diffs)
        # Normalizing the frame differences based on windows parameters
        sm_diff_array = self.__smooth__(diff_array, self.len_window)

        # sm_diff_array = diff_array
        # Get the indexes of those frames which have maximum differences
        frame_indexes = np.asarray(argrelextrema(sm_diff_array, np.greater))[0]

        return [frames[idx - 1] for idx in frame_indexes]

    def __smooth__(self, x, window_len, window=Configs.window_type):
        if x.ndim != 1:
            raise (ValueError, "smooth only accepts 1 dimension arrays.")

        if x.size < window_len:
            raise (ValueError, "Input vector needs to be bigger than window size.")

        if window_len < 3:
            return x

        if not window in ["flat", "hanning", "hamming", "bartlett", "blackman"]:
            raise (
                ValueError,
                "Smoothing Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'",
            )

            # Doing row-wise merging of frame differences wrt window length. frame difference
            # by factor of two and subtracting the frame differences from index == window length in reverse direction
        s = np.r_[2 * x[0] - x[window_len:1:-1], x, 2 * x[-1] - x[-1:-window_len:-1]]

        if window == "flat":
            w = np.ones(window_len, "d")
        else:
            w = getattr(np, window)(window_len)
        y = np.convolve(w / w.sum(), s, mode="same")
        return y[window_len - 1: -window_len + 1]

    def propose_frames(self, path):
        extracted_candidate_key_frames = []

        frame_extractor_from_video_generator = self.__extract_all_frames_from_video__(path)

        for frames, frame_diffs in frame_extractor_from_video_generator:
            if self.USE_LOCAL_MAXIMA:
                extracted_candidate_key_frames_chunk = self.__get_frames_in_local_maxima__(frames, frame_diffs)
                extracted_candidate_key_frames.extend(extracted_candidate_key_frames_chunk)

        return extracted_candidate_key_frames

    def imshow_frames(self, frames):
        for frame in frames:
            plt.imshow(frame)
            plt.show()
            # cv2.imshow('frames', frame)

    def save_frames(self, frames):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

        for frame in frames:
            out.write(frame)

        out.release()
