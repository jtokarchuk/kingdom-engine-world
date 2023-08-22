class Account:
    def __init__(self):
        self.email = None
        self.password = None
        self.authenticated = False
        self.state = "setup"
        self.last_command = None
        self.entity = None
