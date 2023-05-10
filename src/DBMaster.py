import asyncio
import asyncpg
import json
import ssl
from pathlib import Path

class DbMaster:
    def __init__(self):
        #cred data parsing
        base_dir = Path(__file__).parent.parent.resolve()
        cur_path = base_dir.joinpath('configs', 'db_auth_config.json')
        with open(cur_path) as json_config:
            pg_cred_data_json = json.load(json_config)
        self.user = pg_cred_data_json['pg_user']
        self.db_name = pg_cred_data_json['db_name']
        self.host = pg_cred_data_json['host']
        pass_path = pg_cred_data_json['pathToPassword']
        with open(pass_path) as json_config:
            pg_cred_data_json = json.load(json_config)
        self.password = pg_cred_data_json['password']
        self.is_connected = False

    async def Connect(self):
        self.is_connected = True
        self.connection = await asyncpg.connect(user=self.user, database=self.db_name,\
                                                 host=self.host, password=self.password, ssl='prefer')

    def ConfigureUsersPair(self, id1: int, id2: int):
        print('start configuring')
        print(id1)
        print(id2)
        first, second = id1, id2
        if id1> id2:
            (first, second) = (second, first)
        return first, second


    async def SendToUser(self, my_id: int, another_id: int, text_data: str):
        if not self.is_connected:
            await self.Connect()
        id1, id2 = self.ConfigureUsersPair(my_id, another_id)
        print("pair configured")
        await self.connection.execute('''INSERT into soc_net_chats.chats_(id, 
        u_id1, u_id2, sended_data, sender)
        VALUES(DEFAULT ,$1, $2, $3, $4)''', id1, id2, text_data, my_id)
        print("executed")


    async def GetAllMessagesFromChat(self, my_id: int, another_id: int):
        if not self.is_connected:
            await self.Connect()
        id1, id2 = self.ConfigureUsersPair(my_id, another_id)
        print("GET IDS")
        rows = await self.connection.fetch(''' SELECT * from soc_net_chats.chats_
         WHERE u_id1 = $1 and u_id2 = $2''', id1, id2)
        print("exec row")
        return {str(row['id']) : {"u_id1": id1, "u_id2": id2, "sender": row['sender'], \
                 'sended': row['sended_data']} for row in rows}
