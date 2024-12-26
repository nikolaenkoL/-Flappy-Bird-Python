import socket
import threading
import pickle

HOST = '25.22.229.167'
PORT = 65432


game_state = {
    'player_pos': [[300, 300], [300, 350]],
    'scores': [0, 0],
    'lives': [3, 3],
    'pipes': [],
}


def handle_client(conn, addr, player_id):
    print(f"Подключен {addr}")
    conn.send(pickle.dumps(game_state))

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            action = pickle.loads(data)
            if action['type'] == 'move':
                game_state['player_pos'][player_id] += action['value']

            for client in clients:
                client.send(pickle.dumps(game_state))

        except Exception as e:
            print(f"Ошибка: {e}")
            break

    conn.close()
    print(f"Отключен {addr}")


clients = []

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Сервер запущен и ожидает подключения...")

        while True:
            conn, addr = s.accept()
            clients.append(conn)
            player_id = len(clients) - 1
            threading.Thread(target=handle_client, args=(conn, addr, player_id)).start()


if __name__ == "__main__":
    start_server()
