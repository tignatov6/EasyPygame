import sys
import os

#Эта структура не нужна, если EasyPygame.py находится в той же папке что и этот файл
# Получаем абсолютный путь к родительской директории
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Добавляем в PythonPath
if parent_dir not in sys.path:
	sys.path.append(parent_dir)

# Теперь можно импортировать
from EasyPygame import *


class Ball(GameObject):
	def __init__(self,EasyGame,position=Vector2(0,0),scale=Vector2(25,25),sprite='examples/data/textures/ball.png',radius='auto',offset=Vector2(0,0),collisionMode ='None', tag = 'None',speed = 100):
		super().__init__(EasyGame,position,scale,sprite,radius,offset,collisionMode,tag)
		self.speed = speed

	def Update(self):
		if self.EasyGame.GetKeyState(K_w):
			self.position.y -= self.speed * self.EasyGame.delta_time
		if self.EasyGame.GetKeyState(K_a):
			self.position.x -= self.speed * self.EasyGame.delta_time 
		if self.EasyGame.GetKeyState(K_s):
			self.position.y += self.speed * self.EasyGame.delta_time
		if self.EasyGame.GetKeyState(K_d):
			self.position.x += self.speed * self.EasyGame.delta_time

class Enemy(GameObject):
	def __init__(self,EasyGame,position=Vector2(0,0),scale=Vector2(25,25),sprite='examples/data/textures/ball.png',radius='auto',offset=Vector2(0,0),collisionMode ='None', tag = 'None',player = None,moveSpeed=100, patrol_offset = 100,moveDirection=0):
		super().__init__(EasyGame,position,scale,sprite,radius,offset,collisionMode, tag)
		self.moveSpeed = moveSpeed
		self.initPosition = position
		self.player = player
		self.patrol_offset = patrol_offset
		self.moveDirection = Vector2(1,0)
	def MoveEnemy(self):
		self.position -= (self.position - self.player.position).normalize()*self.moveSpeed*self.EasyGame.delta_time
	
	def Patrol(self):
		if self.position.x >= self.patrol_offset + self.initPosition.x:
			self.moveDirection = Vector2(-1,0)
		if self.position.x <= -self.patrol_offset + self.initPosition.x:
			self.moveDirection = Vector2(1,0)
		
		self.position += self.moveDirection * self.moveSpeed * self.EasyGame.delta_time

	def Update(self):
		self.Patrol()


size = (1280,720)

game = EasyGame(size,cameraPosition=Vector2(-0,-0),cameraScale=Vector2(0.5,0.5))

ball = Ball(game,Vector2(300,300),Vector2(50,50),'examples/data/textures/ball.png',collisionMode='circle')
enemy_ball = Enemy(game,Vector2(300,300),Vector2(100,100),player=ball,collisionMode='circle')
button = Button(game,'examples/data/textures/Block.png',Vector2(50,50),'Exit',get_font(25),"#d7fcd4","White",Vector2(100,100))
lable = Lable(game,Vector2(size[0]/2,100),'',get_font(25),"#d7fcd4","White")
running = True
while running:
	running = game.processEvents()
	game.Update()

	if ball.OnCollisionStay():
		lable.setText('True')
	else:
		lable.setText('False')


	if button.clicked():
		pygame.quit()
		sys.exit()
	game.Render()
	display.update()

sys.exit()
		

