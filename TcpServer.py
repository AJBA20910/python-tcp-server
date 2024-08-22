import socket
import requests

# Define the server address and port
server_address = ('0.0.0.0', 8000)  # Bind to all interfaces on port 8000
http_endpoint = 'https://react-app-vwyl.onrender.com/gps'  # Replace with your actual HTTP endpoint

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and start listening
sock.bind(server_address)
sock.listen(5)  # Allow up to 5 queued connections

print(f"Server is listening on {server_address}")

try:
    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        print(f"Connection from {client_address}")
        
        try:
            while True:
                # Receive the data in small chunks
                data = connection.recv(1024).decode('utf-8')
                
                if not data:
                    print("No more data received, closing connection")
                    break  # Exit inner loop if no more data
                
                print(f"Received: {data}")
                
                # Process the received data
                if data.startswith('##,imei:') and data.endswith("A;"):
                    connection.sendall('LOAD'.encode('utf-8'))
                    print("Sent: LOAD")
                elif data == '864035051916097':
                    connection.sendall('ON'.encode('utf-8'))
                    print("Sent: ON")
                else:
                    try:
                        connection.sendall('OK'.encode('utf-8'))
                        response = requests.post(http_endpoint, data={'message': data})
                        print(f"Forwarded to HTTP endpoint, status code: {response.status_code}")
                    except requests.RequestException as e:
                        connection.sendall('OK'.encode('utf-8'))
                        print(f"Failed to forward message to HTTP endpoint: {e}")
        
        except Exception as e:
            print(f"Error during connection handling: {e}")
        
        finally:
            connection.close()  # Close connection after processing

except KeyboardInterrupt:
    print("Server stopped.")
finally:
    sock.close()  # Ensure the socket is closed
