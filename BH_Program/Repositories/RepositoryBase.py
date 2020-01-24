from axel import Event


class RepositoryBase:
    new_repo_data_event = Event()

    def save_analyzed_video(self, analyzed_video):
        data = None
        self.new_repo_data_event(data)
        pass
