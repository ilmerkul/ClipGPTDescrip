from src.utils.keyframe import KFPropose, KFCluster
import time

if __name__ == '__main__':
    kf_propose = KFPropose()
    frames = kf_propose.propose_frames('IMG_6971.mp4')
    kd_cluster = KFCluster()
    frames = kd_cluster.select_best_frames(frames)
    kf_propose.imshow_frames(frames)
