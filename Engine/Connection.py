class Connection:
    def __init__(self, comm_method, comm_id, ip_address):
        # comm_method: telnet or ws
        self.__comm_method = comm_method
        # comm_id: uuid, identifying on comm server
        self.__comm_id = comm_id
        self.__ip_address = ip_address
        self.__last_command = None
        self.account = None

    @property
    def comm_id(self):
        return self.__comm_id
    
    @property
    def comm_method(self):
        return self.__comm_method
    
    @property
    def ip_address(self):
        return self.__ip_address
    
    @property
    def last_command(self):
        return self.__last_command