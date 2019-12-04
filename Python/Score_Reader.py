import cv2
import numpy as np
import importlib
import My_OCR
import pickle


# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  #cd to tesseract

# this objec must get the ROI of the score boxs
class MakerHighLight:
    allScoreBoxROI = [530, 650, 800, 1200]
    homeTeamScoreBoxROI = [580, 605, 930, 983]
    guestTeamScoreBoxROI = [580, 605, 1075, 1125]
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    def __init__(self, full_game, dst='dst.mp4'):
        self.full_game_src = full_game  # set the game video src variable
        self.cap = cv2.VideoCapture(full_game)  # cap the gmae
        self.speedFPS = float(self.cap.get(cv2.CAP_PROP_FPS))  # set the FPS of the video
        self.frame_size = {'w': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  # set w, h  of the frame
                           'h': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}
        # self.dst = dst  # set the highlight dst variable
        # self.out = cv2.VideoWriter(dst, self.fourcc, self.speedFPS, (self.frame_size['w'], self.frame_size['h']))
        self.allScoreFrameArr = None
        self.star_frame = 0
        print("\n Created ToHighlight object success! \n\n")

    def goToStartGame(self):
        if not (self.cap.isOpened()):
            print("ERROR, unable to capture the file..")
        # end if

        corrnt_frame = 6350
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, corrnt_frame)
        print('Searching for the game start frame... please wait!')
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            team1scorebox = frame[self.homeTeamScoreBoxROI[0]:self.homeTeamScoreBoxROI[1],
                            self.homeTeamScoreBoxROI[2]:self.homeTeamScoreBoxROI[3]]
            team2scorebox = frame[self.guestTeamScoreBoxROI[0]:self.guestTeamScoreBoxROI[1],
                            self.guestTeamScoreBoxROI[2]:self.guestTeamScoreBoxROI[3]]

            corrnt_frame += 1
            if self.readScore(team1scorebox) == 0:
                if self.readScore(team2scorebox) == 0:
                    break
        print('Tha first game frame is number ' + str(corrnt_frame))
        cv2.destroyAllWindows()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, corrnt_frame)  # set cap to start of the game!!!!
        self.star_frame = corrnt_frame
        return corrnt_frame

    def frameToTime(self, ferame_number):
        if ferame_number:
            return float(ferame_number / self.speedFPS)
        return 0

    def readScore(self, scoreFrameToRede):

        score_text = My_OCR.imageToString(scoreFrameToRede)
        # score_text = pytesseract.image_to_string(scoreFrameToRede)
        if score_text == '':  # Can't read the frame / trash frame
            return -1
        else:
            return int(score_text)

    def isScore(self, teamScoreBoxFrameToCheck, teamCorrntScore):

        new_score_text = My_OCR.imageToString(teamScoreBoxFrameToCheck)
        # ____________________  Test the score: __________________________
        if new_score_text == '':  # Can't read the frame / trash frame
            return -1
        elif int(new_score_text) == teamCorrntScore:  # Didn’t score...
            return 0
        elif int(new_score_text) < (teamCorrntScore + 4):  # Scored 1 / 2 / 3 point's
            return int(new_score_text) - teamCorrntScore
        else:  # Can't read the frame / trash frame
            return -1

    def makeSimpleHighLight(self, to_read_all_frame=False):

        corrnt_frame = self.goToStartGame()
        ret, frame = self.cap.read()
        self.allScoreFrameArr = {corrnt_frame: [(0, 0), self.cap.get(cv2.CAP_PROP_POS_MSEC)]}
        (homeTeamScore, guestTeamScore) = (0, 0)  # score at the start
        run_faster = int(self.speedFPS * 1.0)
        # ______ cap while it not the end of the video: ____
        while self.cap.isOpened():
            corrnt_frame += run_faster
            if  (not to_read_all_frame) and (corrnt_frame > 50000): # to frame 50,000
                break
            if ((self.cap.get(cv2.CAP_PROP_FRAME_COUNT))-(self.speedFPS * run_faster)) > (corrnt_frame + run_faster):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, corrnt_frame + run_faster)  # 0.5 * speedFPS  to run faster!!!!!!
            else:
                break
            # __ read the next frame and ROI the core box: _________
            ret, frame = self.cap.read()
            scoreBoxHomeTeam = frame[self.homeTeamScoreBoxROI[0]:self.homeTeamScoreBoxROI[1],
                               self.homeTeamScoreBoxROI[2]:self.homeTeamScoreBoxROI[3]]
            scoreboxGuestTeam = frame[self.guestTeamScoreBoxROI[0]:self.guestTeamScoreBoxROI[1],
                                self.guestTeamScoreBoxROI[2]:self.guestTeamScoreBoxROI[3]]
            print('Checking score frame, number ' + str(corrnt_frame))
            # _____________ Check if scored: ________________________________________
            new_score_home_team = self.readScore(scoreBoxHomeTeam)
            new_score_guest_team = self.readScore(scoreboxGuestTeam)

            print(str(new_score_home_team) + " vs " + str(new_score_guest_team))

            if (new_score_home_team == (-1)) or (
                    new_score_guest_team == (-1)):  # Problem with the score box frame: can't read..
                new_score_home_team = homeTeamScore
                new_score_guest_team = guestTeamScore

            new_score_home_team -= homeTeamScore
            new_score_guest_team -= guestTeamScore
            if (not new_score_home_team) and (not new_score_guest_team):  # no one score
                pass
            elif (new_score_home_team) and (
                    new_score_guest_team):  # Problem with the score box frame: both team score..
                pass
            elif (new_score_home_team) or (new_score_guest_team):
                homeTeamScore += new_score_home_team
                guestTeamScore += new_score_guest_team
            new_dict = {corrnt_frame: [(homeTeamScore, guestTeamScore), self.cap.get(cv2.CAP_PROP_POS_MSEC)]}
            self.allScoreFrameArr.update(new_dict)
        return self.resultsArrCheckeAndReduce() #return the dict after CheckeAndReduce func

    def resultsArrCheckeAndReduce(self):
        if self.allScoreFrameArr is None:
            print("resultsArrCheckeAndReduce: ERROR with the results...")
            return False

        to_del = []
        home_last_score = 0
        guest_last_score = 0
        for frame, score in self.allScoreFrameArr.items():
            (home_new_score, guest_new_score) = score[0]

            if (home_new_score == -1) or (guest_new_score == -1):
                to_del.append(frame)

            elif (home_new_score == home_last_score) and (guest_new_score == guest_last_score):
                to_del.append(frame)

            elif (home_new_score < home_last_score) or (guest_new_score < guest_last_score):
                print("frameArrCheckeAndReduce: There is a problem! The result in the frame number {} is smaller "
                      "than the result in the previous "
                      "frame..".format(frame))
                to_del.append(frame)

            elif (home_new_score > home_last_score) and (guest_new_score > guest_last_score):
                print("frameArrCheckeAndReduce: There is a problem! The result in the frame number {} Both "
                      "results increased ...".format(frame))
                to_del.append(frame)

            elif (home_new_score > home_last_score) or (guest_new_score > guest_last_score):
                # Someone scored a basket! We'll leave that frame in the arr but update the score
                home_last_score = home_new_score
                guest_last_score = guest_new_score

        # end for frame, score in self.allScoreFrameArr.items()

        to_del.pop(0)
        for frame in to_del:
            del self.allScoreFrameArr[frame]
        return self.allScoreFrameArr


######################################################################################################
################ end of ToHighlight object! ##########################################################
######################################################################################################

# ____________ Test To Highlight: _________________
if __name__ == "__main__":
    x = MakerHighLight('Videos/game1.mp4')
    # file = open('Simple_Highlight.txt', 'a')
    # file.write(json.dumps(x.makeSimpleHighLight()))  # use `json.loads` to do the reverse
    x.makeSimpleHighLight()
    print(x.resultsArrCheckeAndReduce())
