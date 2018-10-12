from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from settings import *
from PPlay.collision import *

#Retorna 1 se colidir e 0 se não
def testaColisao(ball,pad):
	#Se for pad1
	if(pad.x < WIDTH/2):
		#Só irá rebater se estiver antes do pad
		if(ball.x > pad.x):
			#Testando se ele colidiu em relação ao x
			if(ball.x == pad.x + pad_WIDTH or ball.x < pad.x + pad_WIDTH):
				#Testando se ele colidiu em relação ao y
				if((ball.y > pad.y and ball.y < pad.y + pad_HEIGHT) or (ball.y + ball_HEIGHT > pad.y and ball.y < pad.y)):
					return 1
	#Se for pad2
	elif(pad.x > WIDTH/2):
		#Só irá rebater se estiver antes do pad
		if(ball.x + ball_WIDTH < pad.x + pad_WIDTH):
			#Testando se ele colidiu em relação ao x
			if(ball.x + ball_WIDTH == pad.x or ball.x + ball_WIDTH > pad.x):
				#Testando se ele colidiu em relação ao y
				if((ball.y > pad.y and ball.y < pad.y + pad_HEIGHT) or (ball.y + ball_HEIGHT > pad.y and ball.y < pad.y)):
					return 1

	return 0

janela = Window(WIDTH, HEIGHT)

fundo = GameImage("background.jpg")

ball = Sprite("Pong_Ball.png")
pad1 = Sprite("pad.png")
pad2 = Sprite("pad.png")

ball.set_position(WIDTH/2,HEIGHT/2)
pad1.set_position(WIDTH*0.1, HEIGHT/2 - pad_HEIGHT/2)
pad2.set_position(WIDTH*0.9 - pad_WIDTH, HEIGHT/2 - pad_HEIGHT/2)

teclado = Window.get_keyboard()

mouse = Mouse()

#Mantém o estado da última movimentação dos pad, se foi para cima, baixo ou parado. (Por default parado)
pad1_mov = 0
pad2_mov = 0

player_pt = 0
ia_pt = 0

mouse_active = False

while(True):
	placar_1 = str(player_pt)
	placar_2 = str(ia_pt)
	placar = placar_1+"/"+placar_2

	#Detecta se a bolinha saiu da tela e faz o respawn dela
	if(ball.x < 0):
		ball.x = WIDTH/2
		ball.y = HEIGHT/2
		ia_pt += 1
	elif(ball.x > WIDTH):
		ball.x = WIDTH/2
		ball.y = HEIGHT/2
		player_pt += 1

	#Esconde o cursor
	mouse.hide()

	#Detecta a variação de movimento do mouse
	mVar = mouse.delta_movement()

	#Pega a posição atual do mouse
	mPos = mouse.get_position()

	#Desenha os sprites
	fundo.draw()
	ball.draw()
	pad1.draw()
	pad2.draw()
	janela.draw_text(placar, WIDTH/2, 10, 20)

	#Ativa o controle pelo mouse
	if(teclado.key_pressed("m")):
		mouse_active = False
	if(teclado.key_pressed("n")):
		mouse_active = True

	#Limita os pads ao tamanho da tela
	if(teclado.key_pressed("up")):
		if(pad1.y - 1 > 0):
			pad1.y -= pad_SPEED * janela.delta_time()
			pad1_mov = -1
	elif(teclado.key_pressed("down")):
		if(pad1.y + pad_HEIGHT + 1 < HEIGHT):
			pad1.y += pad_SPEED * janela.delta_time()
			pad1_mov = 1
	else:
		pad1_mov = 0


	#Movimento do pad2 pela IA
	if(player_vx > 0):
		if(pad2.y > ball.y):
			if(pad2.y - 1 > 0):
				pad2.y -= pad_SPEED * janela.delta_time()
				pad2_mov = -1
		elif(pad2.y < ball.y):
			if(pad2.y + pad_HEIGHT + 1 < HEIGHT):
				pad2.y += pad_SPEED * janela.delta_time()
				pad2_mov = 1
		else:
			pad2_mov = 0

	#Movimento do pad2 pelo player
	# if(teclado.key_pressed("w")):
	# 	if(pad2.y - 1 > 0):
	# 		pad2.y -= pad_SPEED * janela.delta_time()
	# 		pad2_mov = -1
	# elif(teclado.key_pressed("s")):
	# 	if(pad2.y + pad_HEIGHT + 1 < HEIGHT):
	# 		pad2.y += pad_SPEED * janela.delta_time()
	# 		pad2_mov = 1
	# else:
	# 	pad2_mov = 0

	#Faz a movimentação do pad1 com o mouse
	if(mouse_active):
		if(mVar[1] != 0):
			if(mPos[1] + pad_HEIGHT < HEIGHT):
				pad1.y = mPos[1]
			if(mVar[1] > 0):
				pad1_mov = 1
			else:
				pad1_mov = -1

	#Faz a bolinha colidir com o "teto" e o "chão"
	if(ball.y + (player_vy * janela.delta_time()) < 0 or ball.y + ball_HEIGHT + (player_vy * janela.delta_time()) > HEIGHT):
		player_vy *= -1

	if(testaColisao(ball,pad1)):
		ball.x = pad1.x + pad_WIDTH + 1
		player_vx *= -1
		#Nos restantes dos casos o valor de player_vy se mantém constante
		if(pad1_mov == 1 and player_vy < 0):
			player_vy *= -1
		elif(pad1_mov == -1 and player_vy > 0):
			player_vy *= -1
	elif(testaColisao(ball,pad2)):
		ball.x = pad2.x-1-ball_WIDTH
		player_vx *= -1
		#Nos restantes dos casos o valor de player_vy se mantém constante
		if(pad2_mov == 1 and player_vy < 0):
			player_vy *= -1
		elif(pad2_mov == -1 and player_vy > 0):
			player_vy *= -1

	#Atualiza a posição da bolinha
	if(janela.time_elapsed() > 1500):
		ball.set_position(ball.x+player_vx * janela.delta_time(),ball.y+player_vy * janela.delta_time())


	janela.update()
