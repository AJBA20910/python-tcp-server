import os
import socket
import requests

# TCP Server configuration
TCP_IP = os.environ.get('TCP_IP', '0.0.0.0')  # Listen on all interfaces
TCP_PORT = int(os.environ.get('PORT', 8080))  # Use PORT environment variable or default to 8080
BUFFER_SIZE = 1024

# HTTP endpoint
HTTP_ENDPOINT = os.environ.get('HTTP_ENDPOINT', 'localhost')
HTTP_PORT = os.environ.get('HTTP_PORT', '8081')
PATH = '/gps'

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(1)

print("TCP Server listening on {}:{}".format(TCP_IP, TCP_PORT))

while True:
    # Accept incoming connection
    conn, addr = server_socket.accept()
    print('Connection address:', addr)

    # Receive data from client
    data = conn.recv(BUFFER_SIZE)
    if not data:
        break
    
    # Assuming data is in JSON format
    json_data = data.decode('utf-8')

    # Make HTTP request
    try:
        print(json_data)
        print('http://' + HTTP_ENDPOINT + ':' + HTTP_PORT + PATH, json=json_data)
        response = requests.post('http://' + HTTP_ENDPOINT + ':' + HTTP_PORT + PATH, json=json_data)
        print("HTTP Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("HTTP Request Error:", e)

    conn.close()
