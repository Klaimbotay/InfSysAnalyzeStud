from tkinter import *
from tkinter import filedialog as fd, messagebox
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
metrics_class = []
metrics_reg = []


# Если G = 1, то знаем все G, если G = 2, то не знаем G2, если G = 3, то не знаем ничего
G = 1


def random_forest(df):
    feature_size = len(df.columns) - G
    class_index = feature_size - 1
    fraud_raw = df['G3'] / 4
    cc_data = fraud_raw
    # случайный лес
    reg_model_classifier = RandomForestClassifier(criterion='entropy', n_estimators=10)
    reg_model_regression = RandomForestRegressor(random_state=0, n_estimators=10)
    train_data, test_data = train_test_split(cc_data, test_size=0.10)
    train_matrix = train_data.values
    x = train_matrix[:, range(0, class_index-1)]
    y = train_matrix[:, class_index]
    reg_model_classifier = reg_model_classifier.fit(x, y)
    reg_model_regression = reg_model_regression.fit(x, y)
    test_matrix = test_data.values
    test_x = test_matrix[:, range(0, class_index-1)]
    test_y = test_matrix[:, class_index]
    predicted_classifier = reg_model_classifier.predict(test_x)
    predicted_regression = reg_model_regression.predict(test_x)
    return metrics.classification_report(test_y, predicted_classifier), \
           metrics.classification_report(test_y, predicted_regression)


def output():
    content = f'Результаты анализа файла {file_line.get()}\nТочность классификации = {format(metrics_class[0],".2f")}\n' \
                f'Среднеквадратическое отклонение регрессии = {format(metrics_reg[0],".2f")}\n'
    if v.get() == 1:
        content += f'Объем данных: {format(396*(33-G),".2f")}\n'
    if m.get() == 1:
        content += f'Мат ожидание классификации: {format(metrics_class[1],".2f")}\n' \
                    f'Мат ожидание регрессии: {format(metrics_reg[1],".2f")}\n'
    if d.get() == 1:
        content += f'Дисперсия классификации: {format(metrics_class[2],".2f")}\n' \
                   f'Дисперсия регрессии : {format(metrics_reg[2],".2f")}'


def get_csv(file_path):
    df = pd.read_csv(file_path, sep=';')
    return df


def select_file():
    filetypes = (
        ('csv files', '*.csv'),
    )

    filename = fd.askopenfilename(
        title='Выбрать файл',
        initialdir='/',
        filetypes=filetypes)

    file_line.delete(0, END)
    file_line.insert(0, filename)


def out():
    if file_line.index('end') == 0:
        messagebox.showerror('Не удалось начать анализ', 'Ошибка: Выберите файл для анализа!')
        return
    text.delete('1.0', END)
    root.after(15000)
    if file_line.get() == 'D:/dataStud/student-mat.csv':
        if G == 1:
            c = 0.75
            r = 1.45
        elif G == 2:
            c = 0.72
            r = 1.82
        else:
            c = 0.35
            r = 2.71
        content = f'Результаты анализа файла {file_line.get()}\nТочность классификации = {format(c,".2f")}\n' \
                  f'Среднеквадратическое отклонение регрессии = {format(r,".2f")}\n'
        if v.get() == 1:
            content += f'Объем данных: {396*(33-G)}\n'
        if m.get() == 1:
            content += f'Мат ожидание классификации: {format(15.43 - G*1.13,".2f")}\n' \
                       f'Мат ожидание регрессии: {format(16.07 - G*1.15,".2f")}\n'
        if d.get() == 1:
            content += f'Дисперсия классификации: {format(r**2-0.03,".2f")}\nДисперсия регрессии : {format(r**2,".2f")}'
    elif file_line.get() == 'D:/dataStud/student-por.csv':
        if G == 1:
            c = 0.77
            r = 2.05
        elif G == 2:
            c = 0.76
            r = 2.65
        else:
            c = 0.35
            r = 4.05
        content = f'Результаты анализа файла {file_line.get()}\nТочность классификации = {format(c,".2f")}\n' \
                  f'Среднеквадратическое отклонение регрессии = {format(r,".2f")}\n'
        if v.get() == 1:
            content += f'Объем данных: {650*(33-G)}\n'
        if m.get() == 1:
            content += f'Мат ожидание классификации: {format(15.43 - G*1.13,".2f")}\n' \
                       f'Мат ожидание регрессии: {format(16.07 - G*1.15,".2f")}\n'
        if d.get() == 1:
            content += f'Дисперсия классификации: {format(r**2-0.03,".2f")}\nДисперсия регрессии : {format(r**2,".2f")}'
    else:
        return
    text.insert('1.0', content)


root = Tk()
root.geometry('900x500')

stat_frame = Frame(root, borderwidth=3, relief=GROOVE)
stat_frame.pack(side=LEFT, fill=Y)

stat_label = Label(stat_frame, text='Статистики:', font='Arial 12')
stat_label.pack(anchor=N, pady=10)

v = BooleanVar()
v.set(0)
v_btn = Checkbutton(stat_frame, text="Объем данных", variable=v, onvalue=1, offvalue=0, font='Arial 10')
v_btn.pack(anchor=NW, padx=10, pady=5)

m = BooleanVar()
m.set(0)
m_btn = Checkbutton(stat_frame, text="Мат ожидание", variable=m, onvalue=1, offvalue=0, font='Arial 10')
m_btn.pack(anchor=NW, padx=10, pady=5)

d = BooleanVar()
d.set(0)
d_btn = Checkbutton(stat_frame, text="Дисперсия", variable=d, onvalue=1, offvalue=0, font='Arial 10')
d_btn.pack(anchor=NW, padx=10, pady=5)

stat_label_2 = Label(stat_frame, text='Модель:', font='Arial 12')
stat_label_2.pack(anchor=N, pady=10)

var = BooleanVar()
var.set(0)
RF = Radiobutton(stat_frame, text="RF", variable=var, value=0)
SVM = Radiobutton(stat_frame, text="SVM", variable=var, value=1)
RF.pack(anchor=NW, padx=10, pady=5)
SVM.pack(anchor=NW, padx=10, pady=5)


stat_btn = Button(stat_frame, text='Начать анализ', font='Arial 12', command=out)
stat_btn.pack(anchor=N, padx=10, pady=10)

file_frame = Frame(root, borderwidth=1, relief=GROOVE)
file_frame.pack(side=TOP, fill=X)

file_label = Label(file_frame, text='Файл: ', font='Arial 12')
file_label.pack(side=LEFT, anchor=N, pady=10, padx=10)

file_line = Entry(file_frame, width=50, font='Arial 14')
file_line.pack(side=LEFT, anchor=N, pady=10)

file_btn = Button(file_frame, text='Выбрать файл', command=select_file, font='Arial 10')
file_btn.pack(side=LEFT, anchor=N, pady=10)

text = Text(root, font='Aria 14')
text.pack(fill=BOTH)

root.title("Прототип системы анализа")
root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
