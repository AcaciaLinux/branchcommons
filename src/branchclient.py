import socket
import blog

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

        blog.info("Connection established!")
       
        if(authkey is not None):
            blog.info("Sending auth key...")
            data = self.send_recv_msg("AUTH {}".format(authkey))
            
            if(data == "AUTH_OK"):
                blog.info("Authkey accepted.")
            else:
                blog.error("Could not authenticate: {}".format(data))
                return

        blog.info("Sending machine type...")
        data = self.send_recv_msg("SET_MACHINE_TYPE {}".format(client_type))
        
        if(data == "CMD_OK"):
            blog.info("Machine type granted.")
        else:
            blog.error("Could not set machine type: {}".format(data))
            return None

        blog.info("Sending client name...")
        data = self.send_recv_msg("SET_MACHINE_NAME {}".format(client_name))

        if(data == "CMD_OK"):
            blog.info("Client name accepted.")
        else:
            blog.error("An error occured: {}".format(data))
            return None
        
        blog.info("Connection established.")

    
    #
    # Get the raw socket object
    #
    def get_socket_object(self):
        return self._socket
    
    #
    # Send data on this client socket
    # 
    def send_msg(self, message):
        message = "{} {}".format(len(bytes(message, "utf-8")), message)
        self._socket.sendall(bytes(message, "utf-8"))

    #
    # Receive data on this client socket
    # 
    def recv_msg(self):
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
            blog.warn("Byte count error from Server.")
            return None

        while(len(data_trimmed) != cmd_bytes):
            data_trimmed += self._socket.recv(4096)

        return data_trimmed.decode("utf-8")    
    
    #
    # Send a message and read response
    #
    # Returns: NONE on Failure
    def send_recv_msg(self, message):
        self.send_msg(message)
        return self.recv_msg()

    
    #
    # Send a file to the server (needs to be set up
    # previously)
    #
    def send_file(self, filepath):
        file = open(filename, "rb")

        file_size = os.path.getsize(filename)
        bytes_sent = 0
        start_time = time.time()
        elapsed_time = 0

        while True:
            # Use sendfile to transfer the contents of the file
            # directly to the network buffer
            bytes_sent += socket.sendfile(file, bytes_sent, file_size - bytes_sent)

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
        
        res = recv_only(socket)
        return res

