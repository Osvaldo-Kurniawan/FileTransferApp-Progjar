import socket
import json
import base64
import logging

server_address = ('0.0.0.0', 7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message")
        sock.sendall(command_str.encode())
        data_received = ""  # empty string
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received.strip())
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {str(e)}")
        return False

def remote_list():
    command_str = "LIST"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print("daftar file:")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb') as fp:
            fp.write(isifile)
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filepath=""):
    try:
        with open(filepath, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode()
        filename = filepath.split('/')[-1]
        command_str = f"UPLOAD {filename} {encoded_string}"
        hasil = send_command(command_str)
        if hasil and hasil['status'] == 'OK':
            print(f"File {filename} uploaded successfully.")
            return True
        else:
            print("Gagal upload file.")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print(f"File {filename} deleted successfully.")
        return True
    else:
        print("Gagal menghapus file.")
        return False

def main():
    while True:
        print("\nCommands: LIST, GET <filename>, UPLOAD <filepath>, DELETE <filename>, EXIT")
        command = input("Enter command: ").strip().split(maxsplit=1)
        action = command[0].upper()

        if action == "LIST":
            remote_list()
        elif action == "GET" and len(command) > 1:
            remote_get(command[1])
        elif action == "UPLOAD" and len(command) > 1:
            remote_upload(command[1])
        elif action == "DELETE" and len(command) > 1:
            remote_delete(command[1])
        elif action == "EXIT":
            break
        else:
            print("Invalid command or missing filename/filepath.")

if __name__ == '__main__':
    server_address = ('172.16.16.101', 6667)
    main()
