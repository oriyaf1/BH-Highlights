from selenium import webdriver
import time
from axel import Event


class ScoreEvent:
    def __init__(self, player_name, team, pts, pts_number, record_score, assist_player, assist_number):
        self.player_name = player_name
        self.team = team
        self.pts = pts
        self.pts_number = pts_number
        self.record_score = record_score
        self.assist_player = assist_player
        self.assist_number = assist_number

class GameData:
    def __init__(self, home_team, guest_team, url, date, start_time):
        self.Home_team = home_team
        self.guest_team = guest_team
        self.url = url
        self.date = date
        self.start_time = start_time
        self.playbyplay = []

class WebScrapperBase:
    new_data_event = Event()

    def __init__(self):
        self.driver = None
        self.is_open = False

    def close_driver(self):
        self.driver.close()
        self.is_open = False

    def get_today_games(self):

        if self.is_open == False:
            self.driver = webdriver.Chrome("../chromedriver.exe")
            self.is_open = True

        self.driver.get("https://watch.nba.com")

        try:
            self.driver.find_element_by_class_name("cookie-close").click()
            time.sleep(1)
        except:
            pass

        ##------------------------ read data: --------------------------------- ##
        today_upcomig_games = []
        schedule_list = self.driver.find_elements_by_class_name("schedule-item")
        for schedule in schedule_list:
            all_data = schedule.text
            if all_data.find('Watch') != -1:
                continue
            all_data = all_data.split('\n')
            url = "https://watch.nba.com/game/" + schedule.get_attribute('onclick').split('\'')[1]
            both_team_name = schedule.find_elements_by_class_name("team-name")
            today_upcomig_games.append(GameData(home_team=all_data[0],
                                                guest_team=all_data[4],
                                                url=url,
                                                date=all_data[3] + "/2020",
                                                start_time=all_data[2].split()[0]))
        # end for
        return today_upcomig_games

    def get_playbyplay(self, game):

        if self.is_open == False:
            self.driver = webdriver.Chrome("../chromedriver.exe")
            self.is_open = True

        self.driver.get(game.url)

        try:
            self.driver.find_element_by_class_name("cookie-close").click()
            time.sleep(1)
        except:
            pass

        for element in self.driver.find_element_by_class_name("switch-part").find_elements_by_class_name("item"):
            if element.text == 'Play-By-Play':
                element.click()
                break
        time.sleep(3)
        self.driver.find_element_by_class_name("all").click()
        time.sleep(2)
        all_Quarter = self.driver.find_elements_by_class_name("playbyplay-content")

        ##------------------------ read data: --------------------------------- ##

        for quarter in all_Quarter:
            for item in quarter.find_elements_by_class_name("items"):
                score_str = item.find_element_by_class_name("record-score").text.split('-')
                data = item.find_element_by_class_name("desc").text
                if data.find('Made') == -1:
                    continue
                if data.find('3pt') == -1:
                    pts = 2
                else:
                    pts = 3
                if data.find('Assist') == -1:
                    is_assist = False
                else:
                    is_assist = True
                pts_number = int(data.split('(')[1].split()[0])
                data_list = data.split()
                assist_player = None
                assist_number = None
                if is_assist:
                    assist_player = data_list[-3]
                    assist_number = int(data_list[-2].replace('(', ''))

                game.playbyplay.insert(0, ScoreEvent(player_name=data_list[2],
                                                      team=item.find_element_by_class_name("team").text,
                                                      pts=pts,
                                                      pts_number=pts_number,
                                                      record_score=(int(score_str[0]), int(score_str[1])),
                                                      assist_player=assist_player,
                                                      assist_number=assist_number))


##------------------------ test: --------------------------------- ##
##---- required a chromedriver.exe in BH_Program directory ! ------##
if __name__ == "__main__":
    my_web_scraper = WebScrapperBase()

    today_upcomig_games = my_web_scraper.get_today_games()
    print("Today games:")
    for game in today_upcomig_games:
        print(game.Home_team, " VS ",game.guest_team,game.date,game.start_time,game.url)

    print("\nhttps://watch.nba.com/game/20200120/TORATL Play By Play:")
    temp_game = GameData('home','guest','https://watch.nba.com/game/20200120/TORATL','date','time')
    my_web_scraper.get_playbyplay(temp_game)
    for score in temp_game.playbyplay:
        print(score.player_name, score.team, score.pts, score.pts_number, score.record_score, score.assist_player, score.assist_number)

    my_web_scraper.close_driver()
