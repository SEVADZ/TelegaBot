import os
import xml.etree.ElementTree as etree

#тупа пак раскидывает в массив вида [название раунда, [название темы, [цена вопроса, вопрос, ответ]]]
def pack(path):
    tree = etree.parse(path)
    root = tree.getroot()
    xmlns = root.tag[:len(root.tag) - 7]
    x = root.findall(".//" + xmlns + "round")
    for round in range(len(x)):
        p = x[round]
        x[round] = []
        x[round].append(p.attrib['name'])
        x[round].append(p.findall(".//" + xmlns + "theme"))
        for theme in range(len(x[round][1])):
            p = x[round][1][theme]
            x[round][1][theme] = []
            x[round][1][theme].append(p.attrib['name'])
            x[round][1][theme].append(p.findall(".//" + xmlns + "question"))
            for question in range(len(x[round][1][theme][1])):
                p = x[round][1][theme][1][question]
                x[round][1][theme][1][question] = []
                x[round][1][theme][1][question].append(p.attrib['price'])
                x[round][1][theme][1][question].append(p.find(".//" + xmlns + "atom").text)
                x[round][1][theme][1][question].append(p.find(".//" + xmlns + "answer").text)
    return x

#тупа по обработаному паку, создает класс, чтобы работать было приятней
#чтобы создать класс, нужно указать путь на файл content.xml в папке где распакован архив
class Packislav():
    def __init__(self, path):
        self.pack = pack(path)
        self.rounds_count = self.round_counter() #количество раундов
    def round_name(self, round): #имя раунда по его номеру
        return self.pack[round][0]
    def theme_name(self, round, theme): #имя темы по номеру раунда и номеру темы
        return self.pack[round][1][theme][0]
    def question(self, round, theme, question): # массив с вопросом, где 1 - цена, 2 - вопрос, 3 - ответ
        return self.pack[round][1][theme][1][question]
    def round_counter(self):
        return len(self.pack)
    def theme_counter(self, round): #считает количество тем в раунде, по номеру раунда
        return len(self.pack[round][1])
'''
чекнуть пак чисто
x = Packislav("C:\\Users\\Админ\\Desktop\\sml\\sadf\\content.xml")
for i in range(x.rounds_count):
    for j in range(x.theme_counter(i)):
        for n in range(5):
            print(x.question(i, j, n))
        print("\n")
    print("----------------")
'''
