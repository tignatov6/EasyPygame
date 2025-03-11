import sys
import os

# Эта структура не нужна, если EasyPygame.py находится в той же папке что и этот файл
# Получаем абсолютный путь к родительской директории
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Добавляем в PythonPath
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Теперь можно импортировать

from EasyPygame import *


import time
import json

def save_game_state(field, XorO,changes):
	# Форматируем состояние поля в строку
	field_key = ",".join(map(str, field)) + f",{XorO}"
	
	
	# Создание структуры данных для сохранения
	game_state = {
		field_key: changes
	}

	# Имя файла для сохранения данных
	filename = "game_state.json"
	
	# Проверка, существует ли файл
	if os.path.exists(filename):
		# Если файл существует, открываем его и загружаем существующие данные
		with open(filename, 'r') as f:
			try:
				data = json.load(f)
			except json.JSONDecodeError:
				data = {}  # Если файл пустой или поврежден, начинаем с пустого словаря
	else:
		data = {}  # Если файл не существует, начинаем с пустого словаря

	# Объединяем новое состояние с существующими данными
	data.update(game_state)

	# Сохраняем обновленные данные обратно в файл
	with open(filename, 'w') as f:
		json.dump(data, f, indent=4)  # Сохраняем с отступами для удобочитаемости


# Функция проверки победы
def check_winner():
	# Все возможные выигрышные комбинации
	winning_combinations = [
		(0, 1, 2),  # 1st row
		(3, 4, 5),  # 2nd row
		(6, 7, 8),  # 3rd row
		(0, 3, 6),  # 1st column
		(1, 4, 7),  # 2nd column
		(2, 5, 8),  # 3rd column
		(0, 4, 8),  # diagonal \
		(2, 4, 6)   # diagonal /
	]
	
	for combo in winning_combinations:
		if field[combo[0]] == field[combo[1]] == field[combo[2]] != 0.5:
			return field[combo[0]]  # Возвращаем победителя (1 или 0)
	
	return None  # Нет победителя


def is_board_full():
	return all(cell != 0.5 for cell in field)  # Проверяем, заполнено ли всё поле

def get_changes(current_field, previous_field):
	return [1 if current_field[i] != previous_field[i] else 0 for i in range(9)]






size = (640,640)

field = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] # 1 = X 0 = O 0.5 = None
previousField = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
XorO = 1 # 1 = X 0 = O

buttons = []
buttonsScale = ((size[0] + size[1]) /2 )/3
offset = buttonsScale/2

game = EasyGame(size,(255,255,255))
running = True


for y in range(3):
	for x in range(3):
		buttons.append(Button(game,'examples/data/textures/-.png',Vector2(offset+buttonsScale*x,offset+buttonsScale*y),'',get_font(25),"#d7fcd4","White",Vector2(buttonsScale,buttonsScale)))


while running:
	running = game.processEvents()
	game.Update()
	for button in buttons:
		if button.clicked():
			idx = buttons.index(button)  # Индекс кнопки
			if field[idx] == 0.5:  # Проверка, свободна ли кнопка
				field[idx] = XorO  # Установка значения в поле
				if XorO == 1:
					button.setImage('examples/data/textures/X.png')  # Установка изображения X
				else:
					button.setImage('examples/data/textures/O.png')  # Установка изображения O
				# Переключение XorO после установки изображения
				XorO = 1 - XorO  # Переключение между 1 и 0
				changes = get_changes(field, previousField)  # Получаем массив изменений
				previousField = field.copy()
				#print("Изменения:", changes)  # Выводим массив изменений

				#save_game_state(field,XorO,changes)



	game.Render()
	display.update()
	winner = check_winner()  # Проверка победителя
	if winner is not None:
		if winner == 1:
			print("Победил X!")
		else:
			print("Победил O!")
	
		field = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] # 1 = X 0 = O 0.5 = None
		previousField = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
		XorO = 1 # 1 = X 0 = O
		for button in buttons:
			button.setImage('examples/data/textures/-.png')
		game.Render()
		display.update()
	elif is_board_full():
		print("Ничья!")
		field = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5] # 1 = X 0 = O 0.5 = None
		previousField = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
		XorO = 1 # 1 = X 0 = O
		for button in buttons:
			button.setImage('examples/data/textures/-.png')
		game.Render()
		display.update()

sys.exit()
		

