# Updated the webdriver

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import re

hedgeFactor = 26
opponentHedge = 59
tooBadOfOdds = -300
event_amt = 11

file1 = open("MMApredictionsheet.txt","w")
file1.write("")
file1.close()

# workbook = xlsxwriter.Workbook('MMA.xlsx')
# worksheet = workbook.add_worksheet()

file2 = open("MMApredictionsheet.txt","a")

webdriver = webdriver.Chrome(ChromeDriverManager().install())

webdriver.get('https://www.tapology.com/')

UFC_event_button = webdriver.find_element_by_xpath('//*[@id="mainUpcoming"]/ul/li/h1/a')
UFC_event_button.click()

# webdriver.get('https://www.tapology.com/fightcenter/events/71447-ufc-fight-night')

sleep(2)

# try:
#     number_events_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/ul/li[1]/div/div[2]')
# except:
#     number_events_path = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/ul/li[1]/div/div[2]')
#
# numberEvents = number_events_path.text
# numberEvents = int(numberEvents)

# print ("Number of events: " + str(numberEvents))

def writeExcel(worksheet,firstName, secondName, first_win_percentage, second_win_percentage, oddsArray, methodArray1, methodArray2, counter, results):

    letter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    worksheet.write(str(letter[0])+str(counter), firstName)
    worksheet.write(str(letter[1])+str(counter), str(oddsArray[0]))
    worksheet.write(str(letter[2])+str(counter), str(first_win_percentage))
    worksheet.write(str(letter[3])+str(counter), str(methodArray1[0]))
    worksheet.write(str(letter[4])+str(counter), str(methodArray1[1]))
    worksheet.write(str(letter[5])+str(counter), str(methodArray1[2]))
    worksheet.write(str(letter[6])+str(counter), secondName)
    worksheet.write(str(letter[7])+str(counter), str(oddsArray[1]))
    worksheet.write(str(letter[8])+str(counter), str(second_win_percentage))
    worksheet.write(str(letter[9])+str(counter), str(methodArray2[0]))
    worksheet.write(str(letter[10])+str(counter), str(methodArray2[1]))
    worksheet.write(str(letter[11])+str(counter), str(methodArray2[2]))
    worksheet.write(str(letter[12])+str(counter), results[0])
    worksheet.write(str(letter[13])+str(counter), results[1])


def getResults(firstName, secondName):
    result = []
    index1 = -10
    index2 = -10
    draw = -1
    tko = -1
    decision1 = -1
    subz = -1
    winner = ""
    method = ""
    try:
        resultTextpath = webdriver.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/h4')
        resultText = resultTextpath.text
    except:
        try:
            resultTextpath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]/h4')
            resultText = resultTextpath.text
        except:
            try:
                resultTextpath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/h4')
                resultText = resultTextpath.text
            except:
                resultTextpath = webdriver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/h4')
                resultText = resultTextpath.text




    index1 = resultText.index(firstName)
    index2  = resultText.index(secondName)

    draw = resultText.find("Draw")
    tko = resultText.find("TKO")
    subz = resultText.find("Submission")
    decision1 = resultText.find("Decision")

    print("Draw: " + str(draw))

    print(resultText)

    print ("The Index 1: " + str(index1))
    print ("The Index 2: " + str(index2))

    if (draw == -1):
        if (tko != -1):
            method = "TKO"
        if (subz != -1):
            method = "Submission"
        if (decision1 != -1):
            method = "Decision"
        if (index1<index2):
            winner = firstName
        else:
            winner = secondName
    else:
        winner = "Draw"
        method = "Draw"

    print ("Winner: " + winner)
    print ("Method: " + method)

    result.append(winner)
    result.append(method)

    return result


def getMethods():
    fighter1Method = []
    try:
        KOpath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[10]/div/div[2]/div[1]/div[2]/div[1]/div[1]')
        KOperc = KOpath.get_attribute("title")
    except:
        try:
            KOpath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[11]/div/div[2]/div[1]/div[2]/div[1]/div[1]')
            KOperc = KOpath.get_attribute("title")
        except:
            try:
                KOpath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[11]/div/div[2]/div[1]/div[2]/div[1]/div[1]')
                KOperc = KOpath.get_attribute("title")
            except:
                try:
                    KOpath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[10]/div/div[2]/div[1]/div[2]/div[1]/div[1]')
                    KOperc = KOpath.get_attribute("title")
                except:
                    try:
                        KOpath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[12]/div/div[2]/div[1]/div[2]/div[1]/div[1]')
                        KOperc = KOpath.get_attribute("title")
                    except:
                        KOpath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[12]/div/div[2]/div[1]/div[2]/div[1]/div[1]')
                        KOperc = KOpath.get_attribute("title")

    KO = KOperc.strip("% by KO/TKO")
    KO = int(KO)
    fighter1Method.append(KO)

    try:
        SubPath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[10]/div/div[2]/div[1]/div[2]/div[1]/div[2]')
        SubPerc = SubPath.get_attribute("title")
    except:
        try:
            SubPath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[11]/div/div[2]/div[1]/div[2]/div[1]/div[2]')
            SubPerc = SubPath.get_attribute("title")
        except:
            try:
                SubPath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[11]/div/div[2]/div[1]/div[2]/div[1]/div[2]')
                SubPerc = SubPath.get_attribute("title")
            except:
                try:
                    SubPath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[10]/div/div[2]/div[1]/div[2]/div[1]/div[2]')
                    SubPerc = SubPath.get_attribute("title")
                except:
                    try:
                        SubPath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[12]/div/div[2]/div[1]/div[2]/div[1]/div[2]')
                        SubPerc = SubPath.get_attribute("title")
                    except:
                        SubPath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[12]/div/div[2]/div[1]/div[2]/div[1]/div[2]')
                        SubPerc = SubPath.get_attribute("title")

    Sub = SubPerc.strip("% by Submission")
    Sub = int(Sub)
    fighter1Method.append(Sub)

    try:
        decPath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[10]/div/div[2]/div[1]/div[2]/div[1]/div[3]')
        decPerc = decPath.get_attribute("title")
    except:
        try:
            decPath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[11]/div/div[2]/div[1]/div[2]/div[1]/div[3]')
            decPerc = decPath.get_attribute("title")
        except:
            try:
                decPath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[11]/div/div[2]/div[1]/div[2]/div[1]/div[3]')
                decPerc = decPath.get_attribute("title")
            except:
                try:
                    decPath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[10]/div/div[2]/div[1]/div[2]/div[1]/div[3]')
                    decPerc = decPath.get_attribute("title")
                except:
                    try:
                        decPath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[12]/div/div[2]/div[1]/div[2]/div[1]/div[3]')
                        decPerc = decPath.get_attribute("title")
                    except:
                        decPath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[12]/div/div[2]/div[1]/div[2]/div[1]/div[3]')
                        decPerc = decPath.get_attribute("title")


    Dec = decPerc.strip("% by Decision")
    Dec = int(Dec)
    fighter1Method.append(Dec)

    print (fighter1Method)
    return fighter1Method

def getMethods1():
    fighter2Method = []
    try:
        KOpath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[10]/div/div[2]/div[2]/div[2]/div[1]/div[1]')
        KOperc1 = KOpath1.get_attribute("title")
    except:
        try:
            KOpath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[11]/div/div[2]/div[2]/div[2]/div[1]/div[1]')
            KOperc1 = KOpath1.get_attribute("title")
        except:
            try:
                KOpath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[11]/div/div[2]/div[2]/div[2]/div[1]/div[1]')
                KOperc1 = KOpath1.get_attribute("title")
            except:
                try:
                    KOpath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[10]/div/div[2]/div[2]/div[2]/div[1]/div[1]')
                    KOperc1 = KOpath1.get_attribute("title")
                except:
                    try:
                        KOpath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[12]/div/div[2]/div[2]/div[2]/div[1]/div[1]')
                        KOperc1 = KOpath1.get_attribute("title")
                    except:
                        KOpath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[12]/div/div[2]/div[2]/div[2]/div[1]/div[1]')
                        KOperc1 = KOpath1.get_attribute("title")


    KO1 = KOperc1.strip("% by KO/TKO")
    KO1 = int(KO1)
    fighter2Method.append(KO1)

    try:
        SubPath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[10]/div/div[2]/div[2]/div[2]/div[1]/div[2]')
        SubPerc1 = SubPath1.get_attribute("title")
    except:
        try:
            SubPath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[11]/div/div[2]/div[2]/div[2]/div[1]/div[2]')
            SubPerc1 = SubPath1.get_attribute("title")
        except:
            try:
                SubPath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[11]/div/div[2]/div[2]/div[2]/div[1]/div[2]')
                SubPerc1 = SubPath1.get_attribute("title")
            except:
                try:
                    SubPath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[10]/div/div[2]/div[2]/div[2]/div[1]/div[2]')
                    SubPerc1 = SubPath1.get_attribute("title")
                except:
                    try:

                        SubPath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[12]/div/div[2]/div[2]/div[2]/div[1]/div[2]')
                        SubPerc1 = SubPath1.get_attribute("title")
                    except:
                        SubPath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[12]/div/div[2]/div[2]/div[2]/div[1]/div[2]')
                        SubPerc1 = SubPath1.get_attribute("title")


    Sub1 = SubPerc1.strip("% by Submission")
    Sub1 = int(Sub1)
    fighter2Method.append(Sub1)

    try:
        decPath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[10]/div/div[2]/div[2]/div[2]/div[1]/div[3]')
        decPerc1 = decPath1.get_attribute("title")
    except:
        try:
            decPath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[11]/div/div[2]/div[2]/div[2]/div[1]/div[3]')
            decPerc1 = decPath1.get_attribute("title")
        except:
            try:
                decPath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[11]/div/div[2]/div[2]/div[2]/div[1]/div[3]')
                decPerc1 = decPath1.get_attribute("title")
            except:
                try:
                    decPath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[10]/div/div[2]/div[2]/div[2]/div[1]/div[3]')
                    decPerc1 = decPath1.get_attribute("title")
                except:
                    try:
                        decPath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[12]/div/div[2]/div[2]/div[2]/div[1]/div[3]')
                        decPerc1 = decPath1.get_attribute("title")
                    except:
                        decPath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[12]/div/div[2]/div[2]/div[2]/div[1]/div[3]')
                        decPerc1 = decPath1.get_attribute("title")


    Dec1 = decPerc1.strip("% by Decision")
    Dec1 = int(Dec1)
    fighter2Method.append(Dec1)

    print (fighter2Method)
    return fighter2Method


def Rules(array1):
    if (array1[0] > array1[1] and array1[0] > array1[2]):
        file2.write("Method of victory: KO/TKO " + str(array1[0]) + "%\n")
    if (array1[1] > array1[0] and array1[1] > array1[2]):
        file2.write("Method of victory: Submission " + str(array1[1]) + "%\n")
    if (array1[2] > array1[0] and array1[2] > array1[1]):
        file2.write("Method of victory: Decision " + str(array1[2]) + "%\n")

def methodOpportunity(array, winpercent):
    if (winpercent>63.5 and array[0] > 69.5):
        file2.write("Take this TKO bet. Make sure odds are positive (+120 at least) 37% correct \n")
    if (winpercent>56.5 and array[1] > 59.5):
        file2.write("Take this submission bet. Make sure odds are positive (+100 at least) 52% correct \n")
    if (winpercent>69.5 and array[2] > 50.5):
        file2.write("Take this points bet. Make sure odds are positive (+100 at least) 47% correct \n")

def Hedging(array1):
    if (array1[0] > array1[1] and array1[0] > array1[2]):
        if (array1[1]> hedgeFactor):
            file2.write("Consider Hedging With Submission: " + str(array1[1]) + "%\n")
        if (array1[2]> hedgeFactor):
            file2.write("Consider Hedging With Decision: " + str(array1[2]) + "%\n")
    if (array1[1] > array1[0] and array1[1] > array1[2]):
        if (array1[0]> hedgeFactor):
            file2.write("Consider Hedging With TKO: " + str(array1[0]) + "%\n")
        if (array1[2]> hedgeFactor):
            file2.write("Consider Hedging With Decision: " + str(array1[2]) + "%\n")
    if (array1[2] > array1[0] and array1[2] > array1[1]):
        if (array1[0]> hedgeFactor):
            file2.write("Consider Hedging With TKO: " + str(array1[0]) + "%\n")
        if (array1[1]> hedgeFactor):
            file2.write("Consider Hedging With Submission: " + str(array1[1]) + "%\n")

def Opponent(array, percentage, name):
    if (percentage > 9):
        if array[0]> opponentHedge:
            file2.write("Consider Hedging: " + name + " via TKO " + str(array[0]) + "%\n")
        if array[1]> opponentHedge:
            file2.write("Consider Hedging: " + name + " via Submission " + str(array[1]) + "%\n")
        if array[2]> opponentHedge:
            file2.write("Consider Hedging: " + name + " via Decision " + str(array[2]) + "%\n")

def GetMoneyLine(name):

    try:
        moneyLinepath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[5]/div/table/tbody/tr[4]/td[1]')
        moneyLine = moneyLinepath.text
        print("found")
    except:
        try:
            moneyLinepath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[6]/div/table/tbody/tr[3]/td[1]')
            moneyLine = moneyLinepath.text
            print("found 1")
        except:
            try:
                moneyLinepath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[5]/div/table/tbody/tr[4]/td[1]')
                moneyLine = moneyLinepath.text
                print("found 2")
            except:
                try:
                    moneyLinepath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]/div/table/tbody/tr[3]/td[1]')
                    moneyLine = moneyLinepath.text
                    print("found 3")
                except:
                    moneyLinepath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[5]/div/table/tbody/tr[3]/td[5]')
                    moneyLine = moneyLinepath.text
                    print("found 4")



    print ("MoneyLine 0 : " + str(moneyLine))

    moneyLine = re.sub('[aeiouqwrtypsdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM+()]', '', moneyLine)
    moneyLine = int(moneyLine)

    try:
        moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[5]/div/table/tbody/tr[4]/td[5]')
        moneyLine1 = moneyLinepath1.text
        print("x")

    except:
        try:
            moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[5]/div/table/tbody/tr[4]/td[5]')
            moneyLine1 = moneyLinepath1.text
            print("xx")
        except:
            try:
                moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[6]/div/table/tbody/tr[3]/td[5]')
                moneyLine1 = moneyLinepath1.text

                print("xxx")

            except:
                try:

                    moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]/div/table/tbody/tr[3]/td[5]')
                    moneyLine1 = moneyLinepath1.text
                    print("xxxx")
                except:
                    try:
                        moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[5]/div/table/tbody/tr[3]/td[1]')
                        moneyLine1 = moneyLinepath1.text
                        print("xxxxx")
                    except:
                        moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[5]/div/table/tbody/tr[3]/td[5]')
                        moneyLine1 = moneyLinepath1.text

                        print("xxxxxxx")



    print("moneyLine1: "+ moneyLine1)

    moneyLine1 = re.sub('[aeiouqwrtypsdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM+()]', '', moneyLine1)
    moneyLine1 = int(moneyLine1)


    try:
        getNamePath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[5]/p[1]/span[1]/a')
        getName = getNamePath.text
    except:
        try:
            getNamePath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[4]/p[1]/span[1]/a')
            getName = getNamePath.text
        except:
            try:
                getNamePath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[4]/p[1]/span[1]/a')
                getName = getNamePath.text
            except:
                getNamePath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[5]/p[1]/span[1]/a')
                getName = getNamePath.text


    last_chars1 = firstName[-3:]
    last_chars2 = getName[-3:]

    print ("These should match: " + last_chars1 + " and " + last_chars2)

    if (last_chars1 == last_chars2):
        moneyLineArray = []
        moneyLineArray.append(moneyLine)
        moneyLineArray.append(moneyLine1)
    else:
        moneyLineArray = []
        moneyLineArray.append(moneyLine1)
        moneyLineArray.append(moneyLine)

    return moneyLineArray

def AnalyzeOdds(array, probArray):

    print ("here are fighter 1 odds + tap " + str(array[0]) + " " + str(probArray[0]))
    print ("here are fighter 2 odds + tap " + str(array[1]) + " " + str(probArray[1]))

    # if (array[0] < tooBadOfOdds):
    #     file2.write("The odds are bad here: " + str(array[0]) + ". Consider not taking the money line\n")
    # if (array[1] < tooBadOfOdds):
    #     file2.write("The odds are bad here: " + str(array[1]) + ". Consider not taking the money line\n")
    # if (array[0] > 0 and probArray[0]> 50):
    #     file2.write("Consideration Alert! Chance for an upset here. Underdog odds: " + str(array[0]) + " Tapology win percentage: " + str(probArray[0]) + "\n")
    # if (array[1] > 0 and probArray[1]> 50):
    #     file2.write("Consideration Alert! Chance for an upset here. Underdog odds: " + str(array[1]) + " Tapology win percentage: " + str(probArray[1]) + "\n")
    if (array[0] < -100 and array[0] > -130 and probArray[0] > 67.5):
        file2.write("Opportunity Alert! Almost even in the odds Take this bet if odds are between -100 & -130 (66% win)\n")
    if (array[1] < -130 and array[1] > -150 and probArray[1] > 20):
        file2.write(" You usually want to take bets in the -130 & -150 odds range. Profitable in the long run (63%)\n")
    if (array[0] < -150 and array[0] > -180 and probArray[0] > 71):
        file2.write(" You can take this bet if you want. History shows long run youll break about even if odds between -150 & -180 (62% win)\n")
    if (array[1] < -180 and array[1] > -210 and probArray[1] > 77):
        file2.write("Opportunity Alert! Take this bet. Will be profitable in the long run if odds are between -180 & -210 (81% win)\n")
    if (array[0] < -210 and array[0] > -230 and probArray[0] > 84):
        file2.write(" Consider doing less amt or not making this bet if odds are between -210 and -230. Slightly profitable in long run (71% win)\n")
    if (array[1] < -230 and array[1] > -260 and probArray[1] > 0):
        file2.write("Opportunity Alert! Consider making this bet. Profitable in the long run if odds between -230 & -260 (79% win)\n")
    if (array[1] < -260 and array[1] > -320 and probArray[1] > 86):
        file2.write("Dont bet on the money line on this round if odds are between -260 & -320 \n")
    if (array[1] < -320 and array[1] > -400 and probArray[1] > 87):
        file2.write("You can take this bet if you want, slightly profitable in the long run -260 & -320\n")
    if (array[1] < -400 and array[1] > -1000 and probArray[1] > 0):
        file2.write("Take this bet. I know the odds are high (-400 & -1000) but long run is profitable. Think about a higher bet\n")
#
    if (array[1] < -100 and array[1] > -130 and probArray[1] > 67.5):
        file2.write("Opportunity Alert! Almost even in the odds Take this bet if odds are between -100 & -130 (66% win)\n")
    if (array[0] < -130 and array[0] > -150 and probArray[0] > 20):
        file2.write(" You usually want to take bets in the -130 & -150 odds range. Profitable in the long run (63%)\n")
    if (array[1] < -150 and array[1] > -180 and probArray[1] > 71):
        file2.write(" You can take this bet if you want. History shows long run youll break about even if odds between -150 & -180 (62% win)\n")
    if (array[0] < -180 and array[0] > -210 and probArray[0] > 77):
        file2.write("Opportunity Alert! Take this bet. Will be profitable in the long run if odds are between -180 & -210 (81% win)\n")
    if (array[1] < -210 and array[1] > -230 and probArray[1] > 84):
        file2.write(" Consider doing less amt or not making this bet if odds are between -210 and -230. Slightly profitable in long run (71% win)\n")
    if (array[0] < -230 and array[0] > -260 and probArray[0] > 0):
        file2.write("Opportunity Alert! Consider making this bet. Profitable in the long run if odds between -230 & -260 (79% win)\n")
    if (array[0] < -260 and array[0] > -320 and probArray[0] > 86):
        file2.write("Dont bet on the money line on this round if odds are between -260 & -320 \n")
    if (array[0] < -320 and array[0] > -400 and probArray[0] > 87):
        file2.write("You can take this bet if you want, slightly profitable in the long run -260 & -320\n")
    if (array[0] < -400 and array[0] > -1000 and probArray[0] > 0):
        file2.write("Take this bet. I know the odds are high (-400 & -1000) but long run is profitable. Think about a higher bet\n")


# xl_counter = 1
event_count = 1
while event_count <= event_amt:
    print("trying to click on event " + str(event_count))
    sleep(2)
    try:
        event = webdriver.find_element_by_xpath('//*[@id="content"]/ul/li['+str(event_count)+']/div/div[4]/table/tbody/tr/td/span/a')
        sleep(1)
        event.click()
    except:
        event = webdriver.find_element_by_xpath('//*[@id="content"]/ul/li['+str(event_count)+']/div/div[5]/table/tbody/tr/td/span/a')
        sleep(1)
        event.click()

    try:
        sleep(2)
        event = webdriver.find_element_by_xpath('//*[@id="content"]/ul/li['+str(event_count)+']/div/div[4]/table/tbody/tr/td/span/a')
        event.click()
    except:
        print ("Event already clicked")

    print("succesfully clicked on event")

    sleep(2)

    webdriver.execute_script("window.scrollTo(0, 2500)")

    sleep(2)
    try:
        print("Finding Name")
        first_name_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[10]/div/div[2]/div[1]/div[1]')
        firstName = first_name_path.text
    except:
        try:
            print("Finding Name again")
            first_name_path = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[10]/div/div[2]/div[1]/div[1]')
            firstName = first_name_path.text
        except:
            try:
                print("Finding Name again *2")
                first_name_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[11]/div/div[2]/div[1]/div[1]')
                firstName = first_name_path.text
            except:
                try:
                    print("Finding Name again *3")
                    first_name_path = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[11]/div/div[2]/div[1]/div[1]')
                    firstName = first_name_path.text
                except:
                    try:
                        print("Finding Name again *4")
                        first_name_path = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[12]/div/div[2]/div[1]/div[1]')
                        firstName = first_name_path.text
                    except:
                        print("Finding Name again *5")
                        first_name_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[12]/div/div[2]/div[1]/div[1]')
                        firstName = first_name_path.text

    moneyLineArray = GetMoneyLine(firstName)

    try:
        print("Finding Name #2")
        second_name_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[10]/div/div[2]/div[2]/div[1]')
        secondName = second_name_path.text
    except:
        try:
            print("Finding Name #2 again")
            second_name_path = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[10]/div/div[2]/div[2]/div[1]')
            secondName = second_name_path.text
        except:
            try:
                print("Finding Name #2 again *2")
                second_name_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[11]/div/div[2]/div[2]/div[1]')
                secondName = second_name_path.text
            except:
                try:
                    print("Finding Name #2 again *3")
                    second_name_path = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[11]/div/div[2]/div[2]/div[1]')
                    secondName = second_name_path.text
                except:
                    try:
                        print("Finding Name #2 again *2")
                        second_name_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[12]/div/div[2]/div[2]/div[1]')
                        secondName = second_name_path.text
                    except:
                        print("Finding Name #2 again *2")
                        second_name_path = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[12]/div/div[2]/div[2]/div[1]')
                        secondName = second_name_path.text

    # results = getResults(firstName, secondName)

    try:
        print("Finding win percentage")
        first_win_percentage_path = webdriver.find_element_by_xpath('//*[@id="content"]/div[10]/div/div[2]/div[1]/div[2]/div[2]')
        first_win_percentage = first_win_percentage_path.text
        first_win_percentage = first_win_percentage.strip("%")
    except:
        try:
            print("Finding win percentage again")
            first_win_percentage_path = webdriver.find_element_by_xpath('//*[@id="content"]/div[11]/div/div[2]/div[1]/div[2]/div[2]')
            first_win_percentage = first_win_percentage_path.text
            first_win_percentage = first_win_percentage.strip("%")
        except:
            print("Finding win percentage again")
            first_win_percentage_path = webdriver.find_element_by_xpath('//*[@id="content"]/div[12]/div/div[2]/div[1]/div[2]/div[2]')
            first_win_percentage = first_win_percentage_path.text
            first_win_percentage = first_win_percentage.strip("%")

    fighter1 = getMethods()

    try:
        print("Finding second win percentage")
        second_win_percentage_path = webdriver.find_element_by_xpath('//*[@id="content"]/div[10]/div/div[2]/div[2]/div[2]/div[2]')
        second_win_percentage = second_win_percentage_path.text
        second_win_percentage = second_win_percentage.strip("%")
    except:
        try:
            print("Finding second win percentage again")
            second_win_percentage_path = webdriver.find_element_by_xpath('//*[@id="content"]/div[11]/div/div[2]/div[2]/div[2]/div[2]')
            second_win_percentage = second_win_percentage_path.text
            second_win_percentage = second_win_percentage.strip("%")
        except:
            print("Finding second win percentage again")
            second_win_percentage_path = webdriver.find_element_by_xpath('//*[@id="content"]/div[12]/div/div[2]/div[2]/div[2]/div[2]')
            second_win_percentage = second_win_percentage_path.text
            second_win_percentage = second_win_percentage.strip("%")

    fighter2 = getMethods1()

    print (firstName + " win percentage is: " + first_win_percentage)
    print (secondName + " win percentage is: " + second_win_percentage)

    first_win_percentage = int(first_win_percentage)
    second_win_percentage = int(second_win_percentage)

    probArray = []
    probArray.append(first_win_percentage)
    probArray.append(second_win_percentage)

    if first_win_percentage>second_win_percentage:
        print ("Tapology Projects " + firstName)
        file2.write("\nTapology Projects " + firstName + " and " + secondName + " will be: " + firstName + " " + str(first_win_percentage) + "%\n")
        file2.write("The method percentages are " + str(fighter1) + "\n")
        Rules(fighter1)
        methodOpportunity(fighter1, first_win_percentage)
        # Hedging(fighter1)
        # HedgingOpponent(fighter2, second_win_percentage, secondName)
        AnalyzeOdds(moneyLineArray , probArray)
    else:
        print ("The winner will be: " + secondName)
        file2.write("\nTapology projects " + firstName + " and " + secondName + " will be: " + secondName + " " + str(second_win_percentage) + "%\n")
        file2.write("The method percentages are " + str(fighter2) + "\n")
        Rules(fighter2)
        methodOpportunity(fighter2, second_win_percentage)
        # Hedging(fighter2)
        # HedgingOpponent(fighter1, first_win_percentage, firstName)
        AnalyzeOdds(moneyLineArray , probArray)

    backbutton = webdriver.find_element_by_xpath('//*[@id="content"]/div[1]/ul/li[3]/a')
    backbutton.click()
    sleep(2)
    event_count += 1

    # writeExcel(worksheet,firstName, secondName, first_win_percentage, second_win_percentage, moneyLineArray, fighter1, fighter2, xl_counter, results)
    # xl_counter+=1

webdriver.close()
# workbook.close()
