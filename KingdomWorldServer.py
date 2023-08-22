import json
import redis

from threading import Thread
from Engine.World import World
from Engine.Account import Account
from Engine.Connection import Connection

def messaging_thread_func(world):
    print("Connecting to redis for messaging relay")
    telnet_receive = redis.Redis(host='localhost', port=6379, decode_responses=True)

    while world.running:
        message = telnet_receive.blpop("gs_inbox", 1)
        """
        gs_message = {
            "time": int(time.time()),
            "client": "telnet",
            "ip_address": client.ip,
            "user_id": client.id,
            "content": message,
            "meta": type
        }
        """
        if message:
            message = json.loads(message[1])

            connection = world.locate_connection(message["client"], message["user_id"])

            if not connection:
                connection = Connection(message["client"], message["user_id"], message["ip_address"])
                world.connections.append(connection)
                connection.last_command = message["time"]

            print(message)
            
            if message["meta"] == "new_connection":
                # Send a welcome message
                # TODO: include MOTD or cool graphic
                if not connection:
                    pass

                world.send_reply(message, "Account Name (Email Address):")

            elif message["meta"] == "disconnect":
                # don't immediately pull players out of the game, they will use disconnect as a cheat death
                pass

            elif message["meta"] == "game_command":
                pass

if __name__ == '__main__':
    print("Setting up World Server")

    world = World()
    world.setup()

    thread = Thread(target = messaging_thread_func, args = (world,))

    thread.start()
    world.loop()