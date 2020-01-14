from axel import Event


class VideoCreatorBase:
    video_created_event = Event()
    num_of_frames_for_trigger = 0

    def set_video_frames_to_trigger_event(self,num_of_frames):
        self.num_of_frames_for_trigger = num_of_frames