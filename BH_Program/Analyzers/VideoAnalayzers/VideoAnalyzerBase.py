import sys

sys.path.append("..")
from axel import Event
from BH_Program.Analyzers.VideoAnalayzers.AnalyzerUtils import *


class VideoAnalyzerBase:
    video_analyzed_event = Event()

    def analyze_video(self, video):
        analyzed = None
        self.video_analyzed_event(analyzed)
        pass
