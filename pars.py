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
                x[round][1][theme][1][question].append(True)
                x[round][1][theme][1][question].append(p.attrib['price'])
                x[round][1][theme][1][question].append(p.find(".//" + xmlns + "atom").text)
                x[round][1][theme][1][question].append(p.find(".//" + xmlns + "answer").text)
    return x

#тупа по обработаному паку, создает класс, чтобы работать было приятней
#чтобы создать класс, нужно указать путь на файл content.xml в папке где распакован архив
class Packislav():
    def __init__(self):
        self.player_answer = None
        self.players = {}
        self.last_answer = ''
        self.start_answer = False
        self.end_qustion = False
        self.Posted = False
        self.start_dispute = False
        self.c_r = None
        self.c_q = None
        self.IsClear = None
        self.pack = ""
        self.IsAlive = None
        self.score=[]
        self.end_game = False
        self.ved =  None
        self.ved_last = None
        self.rounds_count = self.round_counter() #количество раундов
    def chose_pack(self, path):
        self.pack = pack(path)
    def set_ved(self, x):
        self.ved_last = self.ved
        self.ved = x
    def show_players(self):
        show = ''
        j = 0
        for i in self.players.items():
            j += 1
            show += str(j) + " : " + i[0] + "\n"
        return show
    def score_table(self):
        score = ''
        print(self.players)
        print(self.players.items())
        for i in self.players.items():
            print(i)
            score += "@" + str(i[0]) + " : " + str(i[1]) +  "\n"
        return score
    def add_player(self, x):
        print(x.from_user.id, " ", x.from_user.username, " ", 0)
        self.players[x.from_user.username] = 0
    def round_name(self, round): #имя раунда по его номеру
        return self.pack[round][0]
    def theme_name(self, round, theme): #имя темы по номеру раунда и номеру темы
        return self.pack[round][1][theme][0]
    def question(self, round, theme, question): # массив с вопросом, где 1 - True если вопрос не был задан, 2 - цена, 3 - вопрос, 4 - ответ
        return self.pack[round][1][theme][1][question]
    def question_edit(self, round, theme, question):
            self.pack[round][1][theme][1][question][0] = False
    def round_counter(self):
        return len(self.pack)
    def theme_counter(self, round): #считает количество тем в раунде, по номеру раунда
        return len(self.pack[round][1])
    def start_game(self):
        self.c_r = 0
    def round_themes(self, round):
        k = ''
        for i in range(self.theme_counter(round)):
            k += self.theme_name(round, i) + ", "
        return k
    def next_round(self):
        if self.round_counter() > self.c_r + 1:
            self.c_r += 1
        else:
            self.end_game = True

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
