import socket
import os
import time
import blog

from branchpacket import BranchRequest, BranchResponse, BranchStatus

BRANCH_PROTOCOL_VERSION = 1

class branchclient():
    
    #
    # Initialize a new Branch Socket object
    #
    def __init__(self, host, port, client_name, authkey, client_type):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready = False
        blog.info("Connecting to server...")

        try:
            self._socket.connect((host, port))
        except Exception as ex:
            blog.error("Could not establish connection: {}".format(ex))
            return

        auth_request = BranchRequest("AUTH", {
                "machine_identifier": client_name,
                "machine_type": client_type,
                "machine_authkey": authkey,
                "machine_version": BRANCH_PROTOCOL_VERSION
        })
        
        auth_response = self.send_recv_msg(auth_request)
        if(auth_response == None):
            return

        match auth_response.statuscode:
            case BranchStatus.OK:
                blog.info("Connection established to server using protocol v{}. Server: {}".format(BRANCH_PROTOCOL_VERSION, auth_response.payload["logon_message"]))
            
            case BranchStatus.REQUEST_FAILURE:
                blog.error("Could not authenticate: {}".format(auth_response.payload))
                return

            case BranchStatus.INTERNAL_SERVER_ERROR:
                blog.error("Internal server error: {}".format(auth_response.payload))
                return
            
        self.ready = True
    
    #
    # Get the raw socket object
    #
    def get_socket_object(self) -> socket.socket:
        return self._socket
    
    #
    # Send data on this client socket
    # 
    def send_msg(self, message: BranchRequest):
        message = "{} {}".format(len(bytes(message.as_json(), "utf-8")), message.as_json())
        self._socket.sendall(bytes(message, "utf-8"))

    #
    # Receive data on this client socket
    # 
    def recv_msg(self) -> BranchResponse:
        data = None

        try:
            data = self._socket.recv(4096)
        except ConnectionResetError:
            return None

        data_str = data.decode("utf-8")
        data_str_loc = data_str.find(" ")
        cmd_bytes = 0

        data_trimmed = data[data_str_loc+1:len(data)]

        if(data_str_loc == -1):
            blog.error("Connection failed.")
            return None

        try:
            cmd_bytes = int(data_str[0:data_str_loc])
        except ValueError:
            blog.warn("Byte count error from server.")
            return None

        while(len(data_trimmed) != cmd_bytes):
            data_trimmed += self._socket.recv(4096)

        return BranchResponse.from_json(data_trimmed.decode("utf-8"))

    #
    # Receive a BranchRequest on this client socket (Buildbot)
    # 
    def recv_branch_request(self) -> BranchRequest:
        data = None

        try:
            data = self._socket.recv(4096)
        except ConnectionResetError:
            return None

        data_str = data.decode("utf-8")
        data_str_loc = data_str.find(" ")
        cmd_bytes = 0

        data_trimmed = data[data_str_loc+1:len(data)]

        if(data_str_loc == -1):
            blog.error("Connection failed.")
            return None

        try:
            cmd_bytes = int(data_str[0:data_str_loc])
        except ValueError:
            blog.warn("Byte count error from server.")
            return None

        while(len(data_trimmed) != cmd_bytes):
            data_trimmed += self._socket.recv(4096)

        return BranchRequest.from_json(data_trimmed.decode("utf-8"))


    
    #
    # Send a message and read response
    #
    # Returns: NONE on Failure
    def send_recv_msg(self, message: BranchRequest) -> BranchResponse:
        self.send_msg(message)
        return self.recv_msg()

    
    #
    # Send a file to the server (needs to be set up
    # previously)
    #
    def send_file(self, filepath) -> BranchResponse:
        with open(filepath, "rb") as file:
            file_size = os.path.getsize(filepath)
            bytes_sent = 0
            start_time = time.time()
            elapsed_time = 0

            while True:
                # Use sendfile to transfer the contents of the file
                # directly to the network buffer
                bytes_sent += self._socket.sendfile(file, bytes_sent, file_size - bytes_sent)

                # Print progress report every 10 seconds
                elapsed_time += time.time() - start_time
                start_time = time.time()
                if(elapsed_time > 10):
                    speed = bytes_sent / elapsed_time / 1024
                    blog.info("{:.2f} KB / {:.2f} KB, {:.2f} KB/sec".format(bytes_sent / 1024, file_size / 1024, speed))
                    elapsed_time = 0  # Reset elapsed time

                # we are done sending
                if(bytes_sent == file_size):
                    break
            
            res = self.recv_msg()
            return res

    #
    # Receives a file from the server (needs to be set up
    # previously). Needs bytes to read and target filepath.
    #
    # True if received all expected bytes,
    # False if bytes were lost or socket died
    def receive_file(self, filepath, filesize):
        with open(filepath, "wb") as _file:
            bytes_read = 0

            while(not bytes_read == filesize):
                data = self._socket.recv(4096)
                
                # no more data, socket died.
                if(data == b""):
                    break

                bytes_read += len(data)
                _file.write(data)
            
            if(bytes_read == filesize):
                return True
            else:
                return False

    
    #
    # Close the connection
    #
    def disconnect(self):
        self._socket.close()
