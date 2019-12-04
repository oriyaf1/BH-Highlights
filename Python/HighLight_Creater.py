from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.video.compositing.concatenate
import Score_Reader
from moviepy.editor import VideoFileClip, concatenate_videoclips

import cv2
import Score_Reader
import os
import glob
import conector


class HighLightEditor:

    def __init__(self, videoSrc="Videos/test_video1.mp4", dest="_HighLight.mp4"):
        self.videosrc = videoSrc
        self.cap = cv2.VideoCapture(videoSrc)
        self.speedFPS = self.cap.get(cv2.CAP_PROP_FPS)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.maker = Score_Reader.MakerHighLight(videoSrc)
        self.game_play_by_play = None
        self.frame_size = {'w': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  # set w, h  of the frame
                           'h': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}
        self.out = None
        # if dest =="_HighLight.mp4":
        #   self.dest = videoSrc.replace('.mp4', dest)
        # else:
        #    self.dest = dest
        # self.out = cv2.VideoWriter(dst, self.fourcc, self.speedFPS, (self.frame_size['w'], self.frame_size['h']))

    def createSimpleHighLight_ffmpeg(self):
        self.game_play_by_play = self.maker.makeSimpleHighLight(to_read_all_frame=False)
        count = 1
        for frame, score in self.game_play_by_play.items():
            time = (HighLightEditor.frameNumberToTime(frame, int(self.speedFPS)))
            ffmpeg_extract_subclip(self.videosrc, time - 9, time,
                                   self.videosrc.replace('.mp4', '') + "/subClip_{}_{}.mp4".format(
                                       str(score[0]) + str(score[1]), count))
            print("subClip_{}_{}.mp4 created!".format(score, count))
            count += 1
        conector.connecter_mp4subClip()

    def createSimpleHighLight(self):

        self.game_play_by_play = self.maker.makeSimpleHighLight(to_read_all_frame=False)
        time_list = []
        for frame_number, score in self.game_play_by_play.items():
            time = score[1]/1000 # bc it is  ms
            time_list.append([time-7,time-1])

            # בודק שאין חופפים
        for i in range(len(time_list)-1):
            if i+1 == (len(time_list)): #bc i del item in the iteration
                break
            last_time = time_list[i][1]
            new_time = time_list[i+1][0]
            if (new_time - last_time) < 3:
                time_list[i][1] = new_time = time_list[i+1][1]
                del time_list[i+1]

        full_video = VideoFileClip(self.videosrc)
        sub_clips = []
        for time in time_list:
            sub_clips.append(full_video.subclip(time[0],time[1]))
        final_clip = concatenate_videoclips(sub_clips)
        final_clip.write_videofile(self.videosrc.replace('.mp4', '_HighLight.mp4'), self.speedFPS)

    @staticmethod
    def frameNumberToTime(frame_number, fps):
        if frame_number:
            return float(frame_number / fps)
        return 0

    def connecter_mp4subClip(self):
        pass


######################################################################################################
################ end of HighLightEditor object! ######################################################
######################################################################################################

# ____________ Test To HighLightEditor: _________________
if __name__ == "__main__":
    new_highlight = HighLightEditor("Videos/game1.mp4")
    # new_highlight.connecter_mp4subClip()
    new_highlight.createSimpleHighLight()

    # video = VideoFileClip("Videos/game1.mp4").subclip(50,60)
    # video.write_videofile("myHolidays_edited.mp4", fps=30)  # Many options...

    # Make the text. Many more options are available.
    # txt_clip = (TextClip("My Holidays 2013", fontsize=70, color='white')
    #            .set_position('center')
    #           .set_duration(10))
    # result = CompositeVideoClip([video, txt_clip])  # Overlay text on video    pass
