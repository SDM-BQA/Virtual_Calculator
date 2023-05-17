import cv2
from cvzone.HandTrackingModule import HandDetector


# class button
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        # main frame
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)

        # border
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)

        # text
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True
        else:
            return False


# webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1024)
cap.set(4, 768)
# Set the desired size for the video frame
width, height = 1024, 768

# creating button
# Buttons
buttonListValues = [['7', '8', '9', '*', 'C'],
                    ['4', '5', '6', '-', 'x'],
                    ['1', '2', '3', '+', '%'],
                    ['0', '/', '.', '=', 'VC'],
                    ]
buttonList = []
for x in range(5):
    for y in range(4):
        xpos = x * 100 + 200
        ypos = y * 100 + 120
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

# Variables
myEquation = ''
delayCounter = 0

# detect hand init
detector = HandDetector(detectionCon=.5, maxHands=1)  # detectionCon -> if it 80% sure it's a hand then it will show

# loop
while True:
    # get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Resize the frame to the desired size
    resized_frame = cv2.resize(img, (width, height))

    # hand detection
    hands, img = detector.findHands(resized_frame, flipType=False)

    # Draw All
    cv2.rectangle(resized_frame, (200, 50), (200 + 500, 70 + 100),
                  (225, 225, 225), cv2.FILLED)

    cv2.rectangle(resized_frame, (200, 50), (200 + 500, 70 + 100),
                  (50, 50, 50), 3)

    # display the result
    cv2.putText(img, myEquation, (210, 100), cv2.FONT_HERSHEY_PLAIN,
                3, (50, 50, 50), 3)

    for button in buttonList:
        button.draw(resized_frame)

    # check hand
    if hands:
        # Find distance between fingers
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], resized_frame)
        # print(length)
        x, y, _ = lmList[8]

        if length < 30 and delayCounter == 0:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y):
                    myValue = buttonListValues[int(i % 4)][int(i / 4)]  # get correct number
                    print(buttonListValues[int(i % 4)])
                    if myValue == '=':
                        if myEquation:
                            try:
                                if len(str(eval(myEquation))) > 16:
                                    myEquation = "Answer overflow"
                                else:
                                    myEquation = str(eval(myEquation))
                                    pass
                            except (SyntaxError, NameError, ZeroDivisionError, ValueError):
                                myEquation = "Invalid equation"
                        else:
                            pass
# extra function
                    elif myValue == 'C':
                        myEquation = ''
                        delayCounter = 1
                    elif myValue == 'x':
                        myEquation = str(myEquation[:-1])
                        delayCounter = 1
                    elif myValue == "VC":
                        pass
                    else:
                        myEquation += myValue
                        delayCounter = 1

    # to avoid multiple clicks
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Write the Final answer
    # cv2.putText(resized_frame, myEquation, (810, 130), cv2.FONT_HERSHEY_PLAIN,
    #             3, (0, 0, 0), 3)

    # Display
    cv2.imshow("Image", resized_frame)
    # cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''
