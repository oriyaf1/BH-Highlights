from axel import Event


class VideoCreatorBase:
    video_created_event = Event()
    num_of_frames_for_trigger = 0

    def use_if_suited(self,data):
        pass