from __future__ import print_function

import cv2
import numpy as np
from skimage.filters.rank import entropy
from skimage.morphology import disk
import hdbscan


class KFCluster(object):
    def __init__(self):
        self.min_brightness_value = 20
        self.max_brightness_value = 70

        self.min_entropy_value = 0.5
        self.max_entropy_value = 3

    def __get_brighness_score__(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        _, _, v = cv2.split(hsv)
        sum = np.sum(v, dtype=np.float32)
        num_of_pixels = v.shape[0] * v.shape[1]
        brightness_score = (sum * 100.0) / (num_of_pixels * 255.0)

        return brightness_score

    def __get_entropy_score__(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        entr_img = entropy(gray, disk(5))
        all_sum = np.sum(entr_img)
        num_of_pixels = entr_img.shape[0] * entr_img.shape[1]
        entropy_score = all_sum / num_of_pixels

        return entropy_score

    def __variance_of_laplacian__(self, image):
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(image, cv2.CV_64F).var()

    def __get_general_score__(self, image):
        return self.__variance_of_laplacian__(image)

    def __filter_optimum_brightness_and_contrast_images__(self, frames):
        brightness_score = np.asarray(list(map(self.__get_brighness_score__, frames)))

        entropy_score = np.asarray(list(map(self.__get_entropy_score__, frames)))

        brightness_ok = np.logical_and(
            brightness_score > self.min_brightness_value,
            brightness_score < self.max_brightness_value,
        )
        contrast_ok = np.logical_and(
            entropy_score > self.min_entropy_value,
            entropy_score < self.max_entropy_value,
        )

        return [
            frames[i]
            for i in range(len(frames))
            if brightness_ok[i] and contrast_ok[i]
        ]

    def __prepare_cluster_sets_hdbscan(self, frames):
        all_dct = []
        for frame in frames:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (256, 256), img)
            imf = np.float32(img) / 255.0
            dct = cv2.dct(imf)
            dct = dct[:16, :16]
            dct = dct.reshape((256))
            all_dct.append(dct)

        Hdbascan = hdbscan.HDBSCAN(min_cluster_size=2, metric='euclidean').fit(all_dct)
        labels = np.add(Hdbascan.labels_, 1)
        nb_clusters = len(np.unique(Hdbascan.labels_))

        files_clusters_index_array = []
        for i in np.arange(nb_clusters):
            index_array = np.where(labels == i)
            files_clusters_index_array.append(index_array[0])

        return files_clusters_index_array

    def __get_laplacian_scores(self, frames, n_images):
        variance_laplacians = [self.__get_general_score__(frames[n_images[image_i]])
                               for image_i in n_images]

        return variance_laplacians

    def __get_best_images_index_from_each_cluster__(self, frames, files_clusters_index_array):
        filtered_items = []
        for cluster_i in range(len(files_clusters_index_array)):
            curr_row = files_clusters_index_array[cluster_i]

            n_images = np.arange(len(curr_row))
            variance_laplacians = self.__get_laplacian_scores(frames, n_images)

            if not len(variance_laplacians):
                continue
            selected_frame_of_current_cluster = curr_row[np.argmax(variance_laplacians)]
            filtered_items.append(selected_frame_of_current_cluster)

        return filtered_items

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    def select_best_frames(self, frames):
        filtered_images_list = []

        frames = self.__filter_optimum_brightness_and_contrast_images__(frames)

        if len(frames) < 1:
            return filtered_images_list
        files_clusters_index_array = self.__prepare_cluster_sets_hdbscan(
            frames)
        selected_images_index = self.__get_best_images_index_from_each_cluster__(frames, files_clusters_index_array)
        for index in selected_images_index:
            img = frames[index]
            filtered_images_list.append(img)

        return filtered_images_list
