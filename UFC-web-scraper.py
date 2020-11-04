# Updated the webdriver

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import re
import xlsxwriter


bout_count = 136
number_events = 0
bout_count_copy = bout_count

# event_amt = 11

file1 = open("MMApredictionsheet.txt","w")
file1.write("")
file1.close()

workbook = xlsxwriter.Workbook('MMA.xlsx')
worksheet = workbook.add_worksheet()

file2 = open("MMApredictionsheet.txt","a")

webdriver = webdriver.Chrome(ChromeDriverManager().install())

webdriver.get('https://www.tapology.com/search?term=ufc&mainSearchFilter=events')



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
    worksheet.write(str(letter[14])+str(counter), results[2])

    # /html/body/div[3]/div[2]/div[2]/table/tbody/tr[285]/td[1]/a
    # /html/body/div[3]/div[2]/div[2]/table/tbody/tr[284]/td[1]/a
    # /html/body/div[3]/div[2]/div[2]/table/tbody/tr[2]/td[1]/a
    # /html/body/div[3]/div[2]/div[2]/table/tbody/tr[18]/td[1]/a



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

    round_Num = getRound(resultText)


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
    result.append(round_Num)

    return result

def getRound(description):
    # description_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/h4')
    #
    # description = description_path.text

    round = "Round"

    print ("The string is: " + description)

    try:

        round_number = description.partition(round)[2]

        print("String after the substring occurrence : " + round_number)

        if ("Decision" not in round_number):

            round_number = int(round_number)
        else:
            round_number = 0
    except:
        round_number = 0

    return round_number



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
                decPath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[10]/div/div[2]/div[2]/div[2]/div[1]/div[3]')
                decPerc1 = decPath1.get_attribute("title")
            except:
                try:
                    decPath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[11]/div/div[2]/div[2]/div[2]/div[1]/div[3]')
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


# def Rules(array1):
#     if (array1[0] > array1[1] and array1[0] > array1[2]):
#         file2.write("Method of victory: KO/TKO " + str(array1[0]) + "%\n")
#     if (array1[1] > array1[0] and array1[1] > array1[2]):
#         file2.write("Method of victory: Submission " + str(array1[1]) + "%\n")
#     if (array1[2] > array1[0] and array1[2] > array1[1]):
#         file2.write("Method of victory: Decision " + str(array1[2]) + "%\n")
#
# def Hedging(array1):
#     if (array1[0] > array1[1] and array1[0] > array1[2]):
#         if (array1[1]> hedgeFactor):
#             file2.write("Consider Hedging With Submission: " + str(array1[1]) + "%\n")
#         if (array1[2]> hedgeFactor):
#             file2.write("Consider Hedging With Decision: " + str(array1[2]) + "%\n")
#     if (array1[1] > array1[0] and array1[1] > array1[2]):
#         if (array1[0]> hedgeFactor):
#             file2.write("Consider Hedging With TKO: " + str(array1[0]) + "%\n")
#         if (array1[2]> hedgeFactor):
#             file2.write("Consider Hedging With Decision: " + str(array1[2]) + "%\n")
#     if (array1[2] > array1[0] and array1[2] > array1[1]):
#         if (array1[0]> hedgeFactor):
#             file2.write("Consider Hedging With TKO: " + str(array1[0]) + "%\n")
#         if (array1[1]> hedgeFactor):
#             file2.write("Consider Hedging With Submission: " + str(array1[1]) + "%\n")
#
# def HedgingOpponent(array, percentage, name):
#     if (percentage > 9):
#         if array[0]> opponentHedge:
#             file2.write("Consider Hedging: " + name + " via TKO " + str(array[0]) + "%\n")
#         if array[1]> opponentHedge:
#             file2.write("Consider Hedging: " + name + " via Submission " + str(array[1]) + "%\n")
#         if array[2]> opponentHedge:
#             file2.write("Consider Hedging: " + name + " via Decision " + str(array[2]) + "%\n")

def wasClick(event_count):
    # iterate through array of xpaths then check element to see if it was clicked. if not continue
    print("checking if the link was clicked")
    was_clicked= 0
    arrayTicker = 0
    xpathArray = ['/html/body/div[4]/div[2]/ul/li['+str(event_count)+']/div/div[5]/table/tbody/tr/td/span/a','/html/body/div[3]/div[2]/ul/li['+str(event_count)+']/div/div[5]/table/tbody/tr/td/span/a','//*[@id="content"]/ul/li['+str(event_count)+']/div/div[5]/table/tbody/tr/td/span/a','//*[@id="content"]/ul/li['+str(event_count)+']/div/div[4]/table/tbody/tr/td/span/a']
    while(was_clicked == 0):
        print("beginning of while loop")
        try:
            print("first try catch")
            clickEvent = webdriver.find_element_by_xpath(xpathArray[arrayTicker])
            clickText = clickEvent.text


            print("Checking to see if prelim, main or event in this string:" + clickText)

            if ("PRELIM" in clickText or "MAIN" in clickText or "EVENT" in clickText):
                print("clicked event")
                clickEvent.click()
                sleep(1)
                clickEvent.click()
                sleep(1)
                clickEvent.click()
                break
            else:
                arrayTicker+=1
                if(arrayTicker > 3):
                    print("string is not contained in any of the paths")
                    break
                else:
                    continue

        except:
                arrayTicker+=1
                if(arrayTicker > 3):
                    print("gone through all xpaths for event. breaking while loop")
                    break
                else:
                    continue




def GetMoneyLine(name):

    try:
        moneyLinepath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[5]/div/table/tbody/tr[4]/td[1]')
        moneyLine = moneyLinepath.text
    except:
        try:
            moneyLinepath = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[6]/div/table/tbody/tr[3]/td[1]')
            moneyLine = moneyLinepath.text
        except:
            try:
                moneyLinepath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[5]/div/table/tbody/tr[4]/td[1]')
                moneyLine = moneyLinepath.text
            except:
                moneyLinepath = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]/div/table/tbody/tr[3]/td[1]')
                moneyLine = moneyLinepath.text

    moneyLine = re.sub('[aeiouqwrtypsdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM+()]', '', moneyLine)
    moneyLine = int(moneyLine)

    print ("MoneyLine: " + str(moneyLine))

    try:
        moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[5]/div/table/tbody/tr[4]/td[5]')
        moneyLine1 = moneyLinepath1.text
    except:
        try:
            moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[5]/div/table/tbody/tr[4]/td[5]')
            moneyLine1 = moneyLinepath1.text
        except:
            try:
                moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[6]/div/table/tbody/tr[3]/td[5]')
                moneyLine1 = moneyLinepath1.text
            except:
                moneyLinepath1 = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]/div/table/tbody/tr[3]/td[5]')
                moneyLine1 = moneyLinepath1.text

    moneyLine1 = re.sub('[aeiouqwrtypsdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM+()]', '', moneyLine1)
    moneyLine1 = int(moneyLine1)

    print ("MoneyLine: " + str(moneyLine1))

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

    if (array[0] < tooBadOfOdds):
        file2.write("The odds are bad here: " + str(array[0]) + ". Consider not taking the money line\n")
    if (array[1] < tooBadOfOdds):
        file2.write("The odds are bad here: " + str(array[1]) + ". Consider not taking the money line\n")
    if (array[0] > 0 and probArray[0]> 50):
        file2.write("Consideration Alert! Chance for an upset here. Underdog odds: " + str(array[0]) + " Tapology win percentage: " + str(probArray[0]) + "\n")
    if (array[1] > 0 and probArray[1]> 50):
        file2.write("Consideration Alert! Chance for an upset here. Underdog odds: " + str(array[1]) + " Tapology win percentage: " + str(probArray[1]) + "\n")
    if (array[0] < -120 and array[0] > -150 and probArray[0] > 70):
        file2.write("Opportunity Alert! Almost even in the odds (" + str(array[0]) + "), while skewed in Tapology (" + str(probArray[0]) + ")\n")
    if (array[1] < -120 and array[1] > -150 and probArray[1] > 70):
        file2.write("Opportunity Alert! Almost even in the odds (" + str(array[1]) + "), while skewed in Tapology (" + str(probArray[1]) + ")\n")
    if (array[0] < -150 and array[0] > -200 and probArray[0] > 75):
        file2.write("Opportunity Alert! Almost even in the odds (" + str(array[0]) + "), while skewed in Tapology (" + str(probArray[0]) + ")\n")
    if (array[1] < -150 and array[1] > -200 and probArray[1] > 75):
        file2.write("Opportunity Alert! Almost even in the odds (" + str(array[1]) + "), while skewed in Tapology (" + str(probArray[1]) + ")\n")
    if (array[0] < -100 and array[0] > -120 and probArray[0] > 75):
        file2.write("Opportunity Alert! Almost even in the odds (" + str(array[0]) + "), while skewed in Tapology (" + str(probArray[0]) + ")\n")
    if (array[1] < -100 and array[1] > -120 and probArray[1] > 75):
        file2.write("Opportunity Alert! Almost even in the odds (" + str(array[1]) + "), while skewed in Tapology (" + str(probArray[1]) + ")\n")

# while(bout_count <= bout_count_copy + number_events):
print("Original Bout count: "+ str(bout_count_copy))
print("Original Bout count: " + str(bout_count))
print("Should end at: " + str(bout_count_copy + number_events))
try:
    amount_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/table/tbody/tr['+str(bout_count)+']/td[7]')
    amount = amount_path.text
except:
    amount_path = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/table/tbody/tr['+str(bout_count)+']/td[7]')
    amount = amount_path.text

print(amount)

amount = int(amount)

if (amount > 0):
    try:
        event_path = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/table/tbody/tr['+str(bout_count)+']/td[1]/a')
        event_path.click()
    except:
        try:
            event_path = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/table/tbody/tr['+str(bout_count)+']/td[1]/a')
            event_path.click()
        except:
            print("Something went wrong in this event")



    xl_counter = 1
    event_count = 1

    while event_count <= amount:

        # try:

        wasClick(event_count)

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

        results = getResults(firstName, secondName)

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
            print ("The winner will be: " + firstName)
            file2.write("\nThe winner between " + firstName + " and " + secondName + " will be: " + firstName + " " + str(first_win_percentage) + "%\n")
            file2.write("The win percentages are " + str(fighter1) + "\n")
            # Rules(fighter1)
            # Hedging(fighter1)
            # HedgingOpponent(fighter2, second_win_percentage, secondName)
            # AnalyzeOdds(moneyLineArray , probArray)
        else:
            print ("The winner will be: " + secondName)
            file2.write("\nThe winner between " + firstName + " and " + secondName + " will be: " + secondName + " " + str(second_win_percentage) + "%\n")
            file2.write("The win percentages are " + str(fighter2) + "\n")
            # Rules(fighter2)
            # Hedging(fighter2)
            # HedgingOpponent(fighter1, first_win_percentage, firstName)
            # AnalyzeOdds(moneyLineArray , probArray)
        print ("Clicking back button for fight between " + firstName + " and " + secondName)
        backbutton = webdriver.find_element_by_xpath('//*[@id="content"]/div[1]/ul/li[3]/a')
        backbutton.click()
        sleep(2)
        event_count += 1

        writeExcel(worksheet,firstName, secondName, first_win_percentage, second_win_percentage, moneyLineArray, fighter1, fighter2, xl_counter, results)
        xl_counter+=1

        # except:
        #     print("Something went wrong with this bout")
        #     print ("Clicking back button for fight between " + firstName + " and " + secondName)
        #     webdriver.back()
        #     sleep(2)
        #     event_count += 1

    # back button
    # print("Trying to click the back button")
    # webdriver.get('https://www.tapology.com/search?term=ufc&mainSearchFilter=events')
    # sleep(2)
    # print("incrementing one for the next event")
    # bout_count += 1


webdriver.close()
workbook.close()
