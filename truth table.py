from tkinter import *
def clearResult():
    resultLabl["text"] = ''
page = Tk()
page.title("Таблица истинности")

frame1 = Frame(page)
frame2 = Frame(page)
frame3 = Frame(page)
frame1.pack()
frame2.pack()
frame3.pack()
labl = Label(frame1, text = "Доступные функции переменных:\t \na * b;\na + b;\na E b (E - эквивалентность);\na I b (I - импликация);\na R b (R - обратная импликация);\na S b (S - сума по модулю 2);\n!(a);\na | b (функция Шеффера);\na P b (стрелка Пирса);\n ")
labl2 = Label(frame1, text = "Введите функцию f:")
ent = Entry(frame1, width=100)
labl.pack(side = LEFT)
ent.pack(side = RIGHT)
labl2.pack(side = RIGHT)
submitButton = Button(frame2, text='Вывести таблицу истинности', command = lambda : drawTable(ent.get()))
submitButton.pack(side = BOTTOM)
resultLabl = Label(frame3)
resultLabl.pack(side = BOTTOM)

listOfFunctions = ['*', '+', 'E', 'I', 'R', 'S', 'P', '|']
listOfFunctions.reverse()
metaOfFunctions = [lambda a, b: a*b, lambda a, b: int(a or b), lambda a, b: int(not(not(a) and b or not(b) and a)), lambda a, b: int(not(a) or b), lambda a, b: int(not(b) or a), lambda a, b: int(not(a) and b or not(b) and a), lambda a, b: int(not(a or b)), lambda a, b: int(not(a and b))]
metaOfFunctions.reverse()
constElements = ['1', '0']

def listOfVariables(string, listOfFunc):
    tempString = string.replace('!', '').replace('(', '').replace(')', '')
    for func in listOfFunc:
        tempString = tempString.replace(func, '')
    tempString = tempString.replace(' ', '')
    finalList = []
    for i in list(tempString):
        if not i in finalList and not i in constElements:
            finalList.append(i)
    return finalList

def findRightBracket(string):
    if string.find('(') > string.find(')') or string.find('(') == -1:
        return string.find(')')
    else:
        return findRightBracket(string.replace('(', ' ', 1).replace(')', ' ', 1))

def removeBrackets(string):
    if string.find('(') == -1:
        return string
    else:
        indexOfLeftBracket = string.find('(')
        indexOfRightBracket = findRightBracket(string.replace('(', ' ', 1))
        return removeBrackets(string[:indexOfLeftBracket] + ' ' * (indexOfRightBracket - indexOfLeftBracket + 1) + string[indexOfRightBracket + 1:])
    
def calculateFunc(string, mainString, *arg):
    if string in constElements:
        return int(string)
    for funct in listOfFunctions:
        indexOfStr = removeBrackets(string).find(' '+ funct + ' ')
        if not (indexOfStr == -1):
            ide = listOfFunctions.index(funct)
            return metaOfFunctions[ide](calculateFunc(string[:indexOfStr], mainString, *arg), calculateFunc(string[indexOfStr+3:], mainString, *arg))    

    if not(string.find('(') == -1) and (not(string.find('(') - 1 == string.find('!')) or (string.find('!') == -1)):
        tempFunc = [string[string.find('(') - 2 if (string.find('(') - 2) >= 0 else string.find('(')], string[findRightBracket(string.replace('(', ' ', 1)) + 2 if (findRightBracket(string.replace('(', ' ', 1)) + 2) < len(string) else findRightBracket(string.replace('(', ' ', 1))]]
        tempListOfFunctions = ''.join(listOfFunctions)     
        if tempFunc[0] in listOfFunctions and tempFunc[1] in listOfFunctions and tempListOfFunctions.find(tempFunc[1]) >= tempListOfFunctions.find(tempFunc[0]):
            return metaOfFunctions[listOfFunctions.index(tempFunc[1])](metaOfFunctions[listOfFunctions.index(tempFunc[0])](calculateFunc(string[:string.find('(') - 3], mainString, *arg), calculateFunc(string[string.find('(') + 1: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg)), calculateFunc(string[findRightBracket(string.replace('(', ' ', 1)) + 4:], mainString, *arg))
        if tempFunc[0] in listOfFunctions and tempFunc[1] in listOfFunctions and tempListOfFunctions.find(tempFunc[1]) < tempListOfFunctions.find(tempFunc[0]):
            return metaOfFunctions[listOfFunctions.index(tempFunc[1])](calculateFunc(string[:string.find('(') - 3], mainString, *arg), metaOfFunctions[listOfFunctions.index(tempFunc[0])](calculateFunc(string[string.find('(') + 1: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg), calculateFunc(string[findRightBracket(string.replace('(', ' ', 1)) + 4:], mainString, *arg)))
        elif tempFunc[0] in listOfFunctions:
            return metaOfFunctions[listOfFunctions.index(tempFunc[0])](calculateFunc(string[:string.find('(') - 3], mainString, *arg), calculateFunc(string[string.find('(') + 1: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg))
        elif tempFunc[1] in listOfFunctions:
            return metaOfFunctions[listOfFunctions.index(tempFunc[1])](calculateFunc(string[string.find('(') + 1: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg), calculateFunc(string[findRightBracket(string.replace('(', ' ', 1)) + 4:], mainString, *arg))
        return calculateFunc(string[string.find('(') + 1: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg)

    if string.find('!') < string.find('(') and not (string.find('!') == -1):
        tempFunc = [string[string.find('!') - 2 if (string.find('!') - 2) >= 0 else string.find('!')], string[findRightBracket(string.replace('(', ' ', 1)) + 2 if (findRightBracket(string.replace('(', ' ', 1)) + 2) < len(string) else findRightBracket(string.replace('(', ' ', 1))]]
        tempListOfFunctions = ''.join(listOfFunctions)
        if tempFunc[0] in listOfFunctions and tempFunc[1] in listOfFunctions and tempListOfFunctions.find(tempFunc[1]) >= tempListOfFunctions.find(tempFunc[0]):
            return metaOfFunctions[listOfFunctions.index(tempFunc[1])](metaOfFunctions[listOfFunctions.index(tempFunc[0])](calculateFunc(string[:string.find('!') - 3], mainString, *arg), int(not calculateFunc(string[string.find('!') + 2: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg))), calculateFunc(string[findRightBracket(string.replace('(', ' ', 1)) + 4:], mainString, *arg))
        if tempFunc[0] in listOfFunctions and tempFunc[1] in listOfFunctions and tempListOfFunctions.find(tempFunc[1]) < tempListOfFunctions.find(tempFunc[0]):
            return metaOfFunctions[listOfFunctions.index(tempFunc[1])](calculateFunc(string[:string.find('!') - 3], mainString, *arg), metaOfFunctions[listOfFunctions.index(tempFunc[0])](int(not calculateFunc(string[string.find('!') + 2: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg)), calculateFunc(string[findRightBracket(string.replace('(', ' ', 1)) + 4:], mainString, *arg)))       
        elif tempFunc[0] in listOfFunctions:
            return metaOfFunctions[listOfFunctions.index(tempFunc[0])](calculateFunc(string[:string.find('!') - 3], mainString, *arg), int(not calculateFunc(string[string.find('!') + 2: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg)))
        elif tempFunc[1] in listOfFunctions:
            return metaOfFunctions[listOfFunctions.index(tempFunc[1])](int(not calculateFunc(string[string.find('!') + 2: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg)), calculateFunc(string[findRightBracket(string.replace('(', ' ', 1)) + 4:], mainString, *arg))
        return int(not calculateFunc(string[string.find('!') + 2: findRightBracket(string.replace('(', ' ', 1))], mainString, *arg))



    string = string.replace(' ', '')
    return arg[0][listOfVariables(mainString, listOfFunctions).index(string)]

def drawTable(string):
    try:
        def myBin(number, max):
            tempListt = '{0:0<{1}}'.format(bin(number)[:1:-1], max)
            tempListt = tempListt[::-1]
            return tempListt
        resultLabl["text"] = '\n'
        tempListOfVariables = listOfVariables(string, listOfFunctions)
        for variable in tempListOfVariables:
            resultLabl["text"] += f'{variable} \t'
        resultLabl["text"] += '  f\n\n'
        for i in range(pow(2, len(tempListOfVariables))):
            tempArr = []
            for counter in range(len(tempListOfVariables)):
                resultLabl["text"] += f'{myBin(i, len(tempListOfVariables))[counter]}\t'
                tempArr.append(int(myBin(i, len(tempListOfVariables))[counter]))
            resultLabl["text"] += f'  {calculateFunc(string, string, tempArr)}\n'
    except:
        resultLabl["text"] = "Следуй синтаксису написания!"


page.mainloop()