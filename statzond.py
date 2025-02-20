import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

# 1. Загрузка данных
data = pd.read_csv('data.csv')  # Предположим, что файл содержит колонки: глубина, давление_1, давление_2, угол_1, угол_2
depth = data['глубина']
pressure1 = data['давление_1']
pressure2 = data['давление_2']

# 2. Функции для обновления графиков
def update_plot1():
    ax1.clear()
    ax1.plot(depth, pressure1, 'o-', label='Давление 1', color='blue')
    ax1.set_xlabel('Глубина')
    ax1.set_ylabel('Давление 1')
    ax1.legend()
    plt.draw()

def update_plot2():
    ax2.clear()
    ax2.plot(depth, pressure2, 'o-', label='Давление 2', color='green')
    ax2.set_xlabel('Глубина')
    ax2.set_ylabel('Давление 2')
    ax2.legend()
    plt.draw()

# 3. Обработчики кликов для редактирования данных
def on_click_graph1(event):
    if event.inaxes != ax1:
        return
    x_click, y_click = event.xdata, event.ydata
    distances = np.sqrt((depth - x_click) ** 2 + (pressure1 - y_click) ** 2)
    closest_index = distances.idxmin()
    pressure1[closest_index] = y_click  # Обновляем значение давления
    update_plot1()

def on_click_graph2(event):
    if event.inaxes != ax2:
        return
    x_click, y_click = event.xdata, event.ydata
    distances = np.sqrt((depth - x_click) ** 2 + (pressure2 - y_click) ** 2)
    closest_index = distances.idxmin()
    pressure2[closest_index] = y_click  # Обновляем значение давления
    update_plot2()

# 4. Сохранение данных
def save_data(event):
    data['давление_1'] = pressure1
    data['давление_2'] = pressure2
    data.to_csv('updated_data.csv', index=False)
    print('Данные сохранены в updated_data.csv!')

# 5. Создание графиков
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))  # Два графика в одном окне
plt.subplots_adjust(bottom=0.2)  # Оставим место для кнопки

update_plot1()
update_plot2()

# 6. Добавление кнопки "Сохранить"
ax_save = plt.axes([0.7, 0.05, 0.1, 0.075])  # Позиция кнопки
btn_save = Button(ax_save, 'Сохранить')
btn_save.on_clicked(save_data)

# 7. Добавление интерактивности
fig.canvas.mpl_connect('button_press_event', on_click_graph1)  # Для первого графика
fig.canvas.mpl_connect('button_press_event', on_click_graph2)  # Для второго графика

plt.show()
