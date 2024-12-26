import pygame
import socket
import pickle
import threading

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font1 = pygame.font.Font(None, 35)
imgBG = pygame.image.load('5404360.jpg')
imgBird = pygame.image.load('мори.png')
imgPT = pygame.image.load('галагала1.png')
imgPB = pygame.image.load('галагала2.png')

HOST = '25.22.229.167'
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive_data():
    global game_state
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            game_state = pickle.loads(data)
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            break

threading.Thread(target=receive_data, daemon=True).start()

game_state = {
    'player_pos': [[300, 300], [300, 350]],
    'scores': [0, 0],
    'lives': [3, 3],
    'pipes': [],
}

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()
    move_value = 0
    if keys[pygame.K_UP]:
        move_value = -5
    if keys[pygame.K_DOWN]:
        move_value = 5

    if move_value != 0:
        action = {'type': 'move', 'value': move_value}
        client_socket.send(pickle.dumps(action))

    window.fill(pygame.Color('orange'))
    window.blit(imgBG, (0, 0))

    for pipe in game_state['pipes']:
        if pipe.y == 0:
            rect = imgPB.get_rect(bottomleft=pipe.bottomleft)
            window.blit(imgPB, rect)
        else:
            rect = imgPT.get_rect(topleft=pipe.topleft)
            window.blit(imgPT, rect)

    for i in range(len(game_state['player_pos'])):
        pos = game_state['player_pos'][i]
        image = imgBird.subsurface(22 * i, 0, 22, 24)
        window.blit(image, (pos[0], pos[1]))



    text_score_1 = font1.render('Очки: ' + str(game_state['scores'][0]), True, pygame.Color('blue'))
    window.blit(text_score_1, (10, 10))

    text_score_2 = font1.render('Очки: ' + str(game_state['scores'][1]), True, pygame.Color('green'))
    window.blit(text_score_2, (10, 35))

    text_lives_1 = font1.render('Жизни: ' + str(game_state['lives'][0]), True, pygame.Color('red'))
    window.blit(text_lives_1, (10, 60))

    text_lives_2 = font1.render('Жизни: ' + str(game_state['lives'][1]), True, pygame.Color('purple'))
    window.blit(text_lives_2, (10, 85))

    pygame.display.update()
    clock.tick(FPS)

client_socket.close()
pygame.quit()
