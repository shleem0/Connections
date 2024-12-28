import copy
import random
import pygame
from guizero import App, Text, TextBox

class Square:
    def __init__(self, rect, text, textObj, x, y, colour):
        self.rect = rect
        self.text = text
        self.textObj = textObj
        self.x = x
        self.y = y
        self.colour = colour
        self.selected = False

def GetWords():
    file = open("words.txt", "r")

    categories = [""] * 4
    words = ["" * 4] * 4


    for i in range(4):

        categories[i] = file.readline()
        currentWords = file.readline().split()

        words[i] = currentWords

    file.close()
    return categories, words


def RandomiseWords(words):

    index = 0
    shuffledWords = [""] * 16

    for c in words:
        for w in c:

            shuffledWords[index] = w
            index += 1

    random.shuffle(shuffledWords) #shuffles the categories
    return shuffledWords


def SelectWord(current, screen, numSelected, selected):

    selectedRect = pygame.Rect.copy(current.rect)
    current.selected = True
    pygame.draw.rect(screen, "black", selectedRect)
    screen.blit(current.textObj, (current.x + 50, current.y + 30))

    selected[selected.index("")] = current.text
    numSelected += 1

    return numSelected

def DeSelectWord(current, screen, numSelected, selected):
    selectedRect = pygame.Rect.copy(current.rect)
    current.selected = False
    pygame.draw.rect(screen, current.colour, selectedRect)
    screen.blit(current.textObj, (current.x + 50, current.y + 30))

    numSelected -= 1
    selected[selected.index(current.text)] = ""

    return numSelected



def SubmitReady(submit, screen):
    submitRect = pygame.Rect.copy(submit.rect)
    pygame.draw.rect(screen, "mediumorchid", submitRect)
    screen.blit(submit.textObj, (submit.x + 50, submit.y + 35))

    submit.selected = True

def SubmitUnready(submit, screen):

    submitRect = pygame.Rect.copy(submit.rect)
    pygame.draw.rect(screen, "grey", submitRect)
    screen.blit(submit.textObj, (submit.x + 50, submit.y + 35))

    submit.selected = False


def checkSelection(selected, words, lives, rects, screen, numSelected, submit):

    score = 0
    correct = False
    oneAway = False

    for c in range(len(words)):

        score = 0

        for w in selected:
            if w in words[c]:
                score += 1

                if score == 4:
                    category = str(categories[c])
                    print(category)
                    correct = True

                elif score == 3:
                    oneAway = True


    messageWindow = App(width = 240, height = 180)

    if correct:
        message = "Correct!\n" + "Category: " + category + "\n" + str(selected[0]) + ", " +  str(selected[1]) + ", " + str(selected[2]) + ", " + str(selected[3])

        text = Text(messageWindow, text= message)
        removed = 0

        size = len(rects)

        for i in range(size):
            squ = rects[i-removed]
            if squ.text in selected:
                    
                    pygame.draw.rect(screen, "lavender", (pygame.Rect(squ.x, squ.y, 180, 90)))
                    rects.remove(squ)
                    del squ
                    print(len(rects))
                    removed += 1

        selected = [""] * 4
        SubmitUnready(submit, screen)
        numSelected = 0

        
    elif oneAway:
        message = "One away!\n" + str(lives-1) + " tries remaining"
        lives -= 1
        text = Text(messageWindow, text= message)
        messageWindow.display()

    else:
        message = "Wrong!\n" + str(lives-1) + " tries remaining"
        text = Text(messageWindow, text = message)
        lives -= 1


    messageWindow.display()
    return numSelected, lives, selected




def EndGame(win, categories, words, running):

    endMessage = ""

    if win:
        title = "Well done!"
    else:
        title = "Better luck next time!"

    endScreen = App(title = title, height = 350)
    wordCounter = 0

    for c in categories:
        endMessage = endMessage + str(c) + "\n" + words[wordCounter][0] + ", " + words[wordCounter][1] + ", " + words[wordCounter][2] + ", " + words[wordCounter][3] + "\n\n"
        wordCounter += 1

    endMessage = endMessage + "\n" + "Thanks for playing!"

    endText = Text(endScreen, text = endMessage)
    endScreen.display()

    running = False
    return running


#--------------------------------------------------------    

def game(categories, words, randomisedWords):

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 32)

    screen.fill("lavender")
    
    rects = [Square] * 16
    gridIndex = 0
    numSelected = 0
    lives = 4
    selected = [""] * 4
    win = False

    for i in range(0,4):
        for j in range(0,4):

            x = (i % 4 + 1) * 200 + 50
            y = (j % 4 + 1) * 100 + 60
            rects[gridIndex] = Square((pygame.Rect(x, y, 180, 90)), "", None,  x, y, "mediumorchid")
            pygame.draw.rect(screen, rects[gridIndex].colour, rects[gridIndex])

            rects[gridIndex].text = randomisedWords[gridIndex]
            rects[gridIndex].textObj = font.render(randomisedWords[gridIndex], True, "white", None)

            screen.blit(rects[gridIndex].textObj, ((x + 50), (y + 30)))
            gridIndex += 1


    submit = Square((pygame.Rect(550, 570, 180, 90)), "Submit", (font.render("Submit", True, "white", None)), 550, 570, "grey")
    pygame.draw.rect(screen, submit.colour, submit)

    screen.blit(submit.textObj, (submit.x+50, submit.y+35))



    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #quit event
                running = False


            if event.type == pygame.MOUSEBUTTONDOWN: #click event

                for i in range(len(rects)): #selecting words

                    mousePos = pygame.mouse.get_pos()

                    if rects[i].rect.collidepoint(mousePos) and rects[i].selected == False and numSelected < 4:
                        numSelected = SelectWord(rects[i], screen, numSelected, selected)


                    elif rects[i].rect.collidepoint(mousePos) and rects[i].selected == True and numSelected > 0:
                        numSelected = DeSelectWord(rects[i], screen, numSelected, selected)


                    if numSelected == 4:
                            SubmitReady(submit, screen)
                    else:
                            SubmitUnready(submit, screen)


                if submit.rect.collidepoint(mousePos) and submit.selected:

                    numSelected, lives, selected = checkSelection(selected, words, lives, rects, screen, numSelected, submit)

                if len(rects) == 0:

                    win = True
                    running = EndGame(win, categories, words, running)

                elif lives == 0:
        
                    running = EndGame(win, categories, words, running)


        pygame.display.flip()



#---------------------------------------------------------

categories, words = GetWords()
randomisedWords = RandomiseWords(words)

game(categories, words, randomisedWords)