import time
import json
import redis 
from Engine.Scheduler import Scheduler

class World:
    def __init__(self):
        self.__running = False
        self.accounts = []
        self.entities = []
        self.connections = []
        self.online_accounts = []
        self.comms_send = redis.Redis(host='localhost', port=6379, decode_responses=True)

    @property
    def running(self):
        return self.__running
    
    def locate_connection(self, comm_method, comm_id):
        for item in self.connections:
            if item.comm_method == comm_method and item.comm_id == comm_id:
                return item
        
        return None
    
    def send_message(self, recipient, content, meta, client=None):
        client_message = {
            "time": int(time.time()),
            "user_id": recipient,
            "content": content,
            "meta": meta
        }

        if client == None:
            self.comms_send.rpush("gs_outbox_telnet", json.dumps(client_message))
            self.comms_send.rpush("gs_outbox_ws", json.dumps(client_message))
        elif client == "telnet":
            self.comms_send.rpush("gs_outbox_telnet", json.dumps(client_message))
        elif client == "ws":
            self.comms_send.rpush("gs_outbox_ws", json.dumps(client_message))

    def send_reply(self, message, content, meta="game_command"):
        self.send_message(message["user_id"], content, meta, message["client"])

    def setup(self):
        self.__running = True
        self.scheduler = Scheduler()
        self.scheduler.register("check_idle_players", "check_idle", "all", 0, 60)

    def loop(self):
        print("Entering game loop")
        try:
            while self.running:
                self.scheduler.check_jobs()
                time.sleep(0.02)


        except KeyboardInterrupt:
            print("Got keyboard interrupt, shutting down")
            self.__running = False
        # update entities
        # update environment
        # run scheduled actions

