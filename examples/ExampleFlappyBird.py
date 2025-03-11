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
import random

#Создаём класс-наследник игры для хранения переменных
class FlappyBirdGame(EasyGame):
	def __init__(self, size=(256,256),color=(0,0,0),cameraPosition=Vector2(0,0), cameraScale = Vector2(1,1)):
		super().__init__(size,color,cameraPosition,cameraScale)
		# Переменная, хранящая все экземпляры объектов "труб"
		self.tubes = []
		# Переменная, хранящая счёт
		self.score = 0


	# Переопределяем функцию Update
	# Нужна для выполнения метода Update у всех игровых объектов
	def Update(self):
		for gameObject in self.gameObjects:
			if gameObject.active == True:
				gameObject.Update()
		#Добавляем выполнение метода Update у всех "труб".
		for tube in self.tubes:
			tube.Update()


# Создаём класс птицы(игрока)
class Bird(PhysicsGameObject):
	def __init__(self,EasyGame,position=Vector2(0,0),scale=Vector2(25,25),sprite='examples/data/textures/ball.png',jumpVelocity = Vector2(0,-750),radius='auto',offset=Vector2(0,0),collisionMode ='box', tag = 'bird',gravity=Vector2(0,10),initialVelocity = Vector2(0,0),physicsMode = 'gravity',mass=1,bouncy=0.1):
		super().__init__(EasyGame,position,scale,sprite,radius,offset,collisionMode,tag,gravity,initialVelocity,physicsMode,mass,bouncy)
		#Переменная, хранящая ускорение, добавляемое при прыжке.
		self.jumpVelocity = jumpVelocity

	# Переопределяем метод Update для выполнения прыжка и звука 
	def Update(self):
		if self.EasyGame.CheckEvent(pygame.MOUSEBUTTONDOWN): # также в этом случае можно исп. self.EasyGame.MOUSEBUTTONDOWN 
			self.velocity = Vector2(0,0)
			self.velocity += self.jumpVelocity
			self.EasyGame.PlaySound('examples/data/sfx/jump.wav')


# Создаём класс труб(препядствий)
class Tubes():
	def __init__(self,EasyGame,position=Vector2(2000,-250),scale=Vector2(250,1000),sprite='examples/data/textures/Block.png',radius='auto',offset=Vector2(0,0),collisionMode ='box', tag = 'tube',tubesSpace=Vector2(0,400),moveVelocity = Vector2(-400,0)):
		self.EasyGame = EasyGame
		self.window = self.EasyGame.window
		self.position = position
		self.tubesSpace = tubesSpace
		# Создаём 2 объекта трубы
		self.Tube1 = GameObject(EasyGame,Vector2(position.x,position.y - scale.y/2),scale,sprite,radius,offset,collisionMode,tag)
		self.Tube2 = GameObject(EasyGame,Vector2(position.x,position.y + scale.y/2)+self.tubesSpace,scale,sprite,radius,offset,collisionMode,tag)
		self.moveVelocity = moveVelocity
		# Добавляем этот объект труб в FlappyBirdGame.tubes
		# Нужно для выполнения метода Update ниже ⬇️
		self.EasyGame.tubes.append(self)
		self.scale = scale

	# Создём метод Update
	def Update(self):
		# Двигаем себя и задаём нужное положение каждой требе
		self.position += self.moveVelocity * self.EasyGame.delta_time
		self.Tube1.position = Vector2(self.position.x,self.position.y - self.scale.y/2)
		self.Tube2.position = Vector2(self.position.x,self.position.y + self.scale.y/2)+self.tubesSpace
		# Проверяем выход за экран
		if self.position.x - self.scale.x < -self.EasyGame.size[0]:
			# Передвигаем в начало и задаём случайную позицию по Y
			self.position = Vector2(2000,random.randint(-75,0)*10) # Умножаем на 10 для большего контраста высот(я не увререн что это так работает)
			self.EasyGame.score += 1 # +1 очко к счёту


# Главная функция игры (нужна для удобного перезапуска сцены при смерти)
# Можно создавать несколько похожих функций для реализации меню/уровней
def main_game():
	# Задаём размер окна
	size = (1280,720)

	# Создаём объект игры
	game = FlappyBirdGame(size,cameraPosition=Vector2(-0,-0),cameraScale=Vector2(0.5,0.5))

	# Создаём "игрорвое поле"
	gameSpace = GameObject(game,position=Vector2(0,-375),scale=Vector2(size[0]*1.9,size[1]*1.9),collisionMode='box',tag='gameSpace',offset=Vector2(0,0),sprite='examples/data/textures/Block.png')
	# Делаем не видимым
	gameSpace.visible = False
	# Игрок
	bird = Bird(game,position=Vector2(size[0]/2-50,size[1]/2-50),scale=Vector2(100,100),sprite='examples/data/textures/ball.png')
	# Трубы
	tubes1 = Tubes(game,scale=Vector2(250,1000),position=Vector2(2000,random.randint(-75,0)*10))
	tubes2 = Tubes(game,scale=Vector2(250,1000),position=Vector2(3500,random.randint(-75,0)*10))
	# Кнопка выхода
	button = Button(game,'examples/data/textures/Block.png',Vector2(50,50),'Exit',get_font(25),"#d7fcd4","White",Vector2(100,100))
	# Текст для вывода счёта
	lable = Lable(game,Vector2(size[0]/2,100),'',get_font(25),"#d7fcd4","White")

	# Часы для ограничения фпс (не обязательно, но ОЧЕНЬ ЖЕЛАТЕЛЬНО при использовании PhysicsGameObject и наследуемых от него классов)
	clock = Clock()
	running = True
	# Главеный цикл игры
	while running:
		# Нужно для определения работает игра или нет
		running = game.processEvents() # Обработка всех событий для возможности использования позже
		game.UpdatePhysics() # Выполнение физики(если есть PhysicsGameObject)
		game.Update() # Выполнение методов Update всех игровых объектов
		# Если вне "игрового поля" значит перезапуск сцены
		if not bird.OnCollisionStay(tag='gameSpace'):
			running = False
			return True

		# Если касается "трубы" значит перезапуск сцены
		if bird.OnCollisionStay(tag='tube'):
			running = False
			return True

		# Выход при нажатии на кнопку
		if button.clicked():
			pygame.quit()
			return False
		# Задаём текст для вывода счёта на экран
		lable.setText(f'{game.score}')
		# Рисуем сцену
		game.Render()
		# обновляем изображение на экране
		display.update()
		# Ограничиваем fps (не обязательно, но ОЧЕНЬ ЖЕЛАТЕЛЬНО при использовании PhysicsGameObject и наследуемых от него классов)
		# В данном случае без ограничения фпс физика ведёт себя странно
		clock.tick(120)
		

# Перезапускаем сцену пока игрок не захочет выйти
mainGameRunning = True
while mainGameRunning:
	mainGameRunning = main_game()

# Закрываем игру
sys.exit()
		

