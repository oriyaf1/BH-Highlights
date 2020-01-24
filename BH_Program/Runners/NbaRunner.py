import sys

sys.path.append("..")
from BH_Program.DataCreators.VideoRecorders.VideoRecorderBase import \
    VideoRecorderBase as Recorder  # should import NbaRecorder
from BH_Program.Analyzers.VideoAnalayzers.VideoAnalyzerBase import \
    VideoAnalyzerBase as Analyzer  # should import NbaVideoAnalyzer
from BH_Program.Repositories.RepositoryBase import RepositoryBase as Repository  # should be you now the drill
from BH_Program.VideoCreators.VideoCreatorBase import VideoCreatorBase as VideoCreator  # should be you now the drill
from BH_Program.Uploaders import UploaderBase as Uploader  # should be you now the drill
from BH_Program.WebScrappers import WebScrapperBase as Scrapper  # should be you now the drill


class NbaRunner:
    # Should get next game time
    # sleeps until it starts
    # record - analyze - save to db - create game

    def run(self):
        while (True):
            self.__sleep_until_next_game_day()  # sleep until 30 minutes before the first game
            gamesThreads = []
            games = self.__get_tonight_games()  # the needed metadata foreach game
            # starting threads
            for game in games:
                gameThread = self.__create_game_thread(game)
                gameThread.start()
                gamesThreads.append(gameThread)
            # waiting for games analyze to finish
            for thread in gamesThreads:
                thread.join()

    def __sleep_until_next_game_day(self):
        pass

    def __get_tonight_games(self):
        pass

    def __create_game_thread(self, game: object) -> object:
        # just in general
        # create controllers
        recorder = Recorder()
        analyzer = Analyzer()
        repo = Repository()
        creator = VideoCreator()
        uploader = Uploader
        # register to events
        recorder.video_recorded_event += analyzer.analyze_video
        analyzer.video_analyzed_event += repo.save_analyzed_video
        repo.new_repo_data_event += creator.use_if_suited
        creator.video_created_event += uploader.upload_video

        recorder.start_recording()
        pass
