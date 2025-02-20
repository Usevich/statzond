import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import pandas as pd
from tkinter import filedialog

class CPTVisualizer:
    def __init__(self):
        self.depth = None
        self.pressure1 = None
        self.pressure2 = None
        self.fig = None
        self.ax = None
        self.lines = []
        self.selected_line = None
        self.data_file = None

    def load_data(self):
        # Открытие диалога выбора файла
        self.data_file = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not self.data_file:
            return False

        # Чтение данных (предполагаем, что файл CSV с 4 колонками)
        try:
            data = pd.read_csv(self.data_file)
            # Предполагаем, что колонки: depth, pressure1, pressure2, angle1, angle2
            self.depth = data.iloc[:, 0].values  # Глубина
            self.pressure1 = data.iloc[:, 1].values  # Давление 1
            self.pressure2 = data.iloc[:, 2].values  # Давление 2
            return True
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return False

    def save_data(self, event):
        save_file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if save_file:
            df = pd.DataFrame({
                'Depth': self.depth,
                'Pressure1': self.pressure1,
                'Pressure2': self.pressure2
            })
            df.to_csv(save_file, index=False)
            print(f"Данные сохранены в {save_file}")

    def on_pick(self, event):
        # Определяем, какая линия была выбрана
        self.selected_line = event.artist
        return True

    def on_motion(self, event):
        # Если выбрана линия и мышь движется
        if self.selected_line is None or event.xdata is None or event.ydata is None:
            return

        # Определяем, какую линию редактируем
        if self.selected_line == self.lines[0]:
            data = self.pressure1
        else:
            data = self.pressure2

        # Находим ближайшую точку
        idx = np.argmin(np.abs(self.depth - event.ydata))
        # Обновляем значение
        data[idx] = event.xdata

        # Обновляем данные линии
        self.selected_line.set_data(data, self.depth)
        self.fig.canvas.draw()

    def on_release(self, event):
        self.selected_line = None

    def reset_data(self, event):
        if self.load_data():
            self.lines[0].set_data(self.pressure1, self.depth)
            self.lines[1].set_data(self.pressure2, self.depth)
            self.fig.canvas.draw()

    def run(self):
        # Загружаем данные
        if not self.load_data():
            return

        # Создаем график
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.2)

        # Рисуем линии давления
        line1, = self.ax.plot(self.pressure1, self.depth, 'b-', picker=5, label='Pressure 1')
        line2, = self.ax.plot(self.pressure2, self.depth, 'r-', picker=5, label='Pressure 2')
        self.lines = [line1, line2]

        # Настройка графика
        self.ax.set_xlabel('Pressure')
        self.ax.set_ylabel('Depth')
        self.ax.invert_yaxis()  # Глубина увеличивается вниз
        self.ax.grid(True)
        self.ax.legend()

        # Добавляем кнопки
        ax_reset = plt.axes([0.7, 0.05, 0.1, 0.075])
        ax_save = plt.axes([0.81, 0.05, 0.1, 0.075])
        btn_reset = Button(ax_reset, 'Reset')
        btn_save = Button(ax_save, 'Save')

        # Подключение обработчиков событий
        btn_reset.on_clicked(self.reset_data)
        btn_save.on_clicked(self.save_data)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

        plt.show()

if __name__ == "__main__":
    # Пример использования
    visualizer = CPTVisualizer()
    visualizer.run()