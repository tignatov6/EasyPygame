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
import random

class FlappyBirdGame(EasyGame):
	def __init__(self, size=(256,256),color=(0,0,0),cameraPosition=Vector2(0,0), cameraScale = Vector2(1,1)):
		super().__init__(size,color,cameraPosition,cameraScale)
		self.tubes = []
		self.score = 0


	def Update(self):
		for gameObject in self.gameObjects:
			if gameObject.active == True:
				gameObject.Update()
		for tube in self.tubes:
			tube.Update()


class Bird(PhysicsGameObject):
	def __init__(self,EasyGame,position=Vector2(0,0),scale=Vector2(25,25),sprite='examples/data/textures/ball.png',jumpVelocity = Vector2(0,-750),radius='auto',offset=Vector2(0,0),collisionMode ='box', tag = 'bird',gravity=Vector2(0,10),initialVelocity = Vector2(0,0),physicsMode = 'gravity',mass=1,bouncy=0.1):
		super().__init__(EasyGame,position,scale,sprite,radius,offset,collisionMode,tag,gravity,initialVelocity,physicsMode,mass,bouncy)
		self.jumpVelocity = jumpVelocity

	def Update(self):
		if self.EasyGame.MOUSEBUTTONDOWN:
			self.velocity = Vector2(0,0)
			self.velocity += self.jumpVelocity
		elif self.EasyGame.GetKeyState(pygame.K_SPACE): 
			self.velocity = Vector2(0,0)
			self.velocity += self.jumpVelocity


class Tubes():
	def __init__(self,EasyGame,position=Vector2(2000,-250),scale=Vector2(250,1000),sprite='examples/data/textures/Block.png',radius='auto',offset=Vector2(0,0),collisionMode ='box', tag = 'tube',tubesSpace=Vector2(0,400),moveVelocity = Vector2(-400,0)):
		#super().__init__(game,position,scale,sprite,radius,offset,collisionMode,tag)
		self.EasyGame = EasyGame
		self.window = self.EasyGame.window
		self.position = position
		self.tubesSpace = tubesSpace
		self.Tube1 = GameObject(EasyGame,Vector2(position.x,position.y - scale.y/2),scale,sprite,radius,offset,collisionMode,tag)
		self.Tube2 = GameObject(EasyGame,Vector2(position.x,position.y + scale.y/2)+self.tubesSpace,scale,sprite,radius,offset,collisionMode,tag)
		self.moveVelocity = moveVelocity
		self.EasyGame.tubes.append(self)
		self.scale = scale

	def Update(self):
		self.position += self.moveVelocity * self.EasyGame.delta_time
		self.Tube1.position = Vector2(self.position.x,self.position.y - self.scale.y/2)
		self.Tube2.position = Vector2(self.position.x,self.position.y + self.scale.y/2)+self.tubesSpace
		if self.position.x - self.scale.x < -self.EasyGame.size[0]:
			self.position = Vector2(2000,random.randint(-75,0)*10)
			self.EasyGame.score += 1


def main_game():
	size = (1280,720)

	game = FlappyBirdGame(size,cameraPosition=Vector2(-0,-0),cameraScale=Vector2(0.5,0.5))

	gameSpace = GameObject(game,position=Vector2(0,-375),scale=Vector2(size[0]*1.9,size[1]*1.9),collisionMode='box',tag='gameSpace',offset=Vector2(0,0),sprite='examples/data/textures/Block.png')
	gameSpace.visible = False
	bird = Bird(game,position=Vector2(size[0]/2-50,size[1]/2-50),scale=Vector2(100,100),sprite='examples/data/textures/ball.png')
	tubes1 = Tubes(game,scale=Vector2(250,1000),position=Vector2(2000,random.randint(-75,0)*10))
	tubes2 = Tubes(game,scale=Vector2(250,1000),position=Vector2(3500,random.randint(-75,0)*10))
	button = Button(game,'examples/data/textures/Block.png',Vector2(50,50),'Exit',get_font(25),"#d7fcd4","White",Vector2(100,100))
	lable = Lable(game,Vector2(size[0]/2,100),'',get_font(25),"#d7fcd4","White")

	clock = Clock()
	running = True
	while running:
		running = game.processEvents()
		game.UpdatePhysics()
		game.Update()
		if bird.OnCollisionStay(tag='gameSpace'):
			pass
		else:
			running = False
			return True

		if bird.OnCollisionStay(tag='tube'):
			running = False
			return True

		if button.clicked():
			pygame.quit()
			sys.exit()
			return False
		lable.setText(f'{game.score}')
		game.Render()
		display.update()
		clock.tick(120)
		


mainGameRunning = True
while mainGameRunning:
	mainGameRunning = main_game()

sys.exit()
		

