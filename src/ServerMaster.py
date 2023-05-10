from GRPCClient import grpc_client
import DBMaster
import grpc
from concurrent import futures

class Server:
    def __init__(self):
        self._db_master = DBMaster.DbMaster()
        self._grpc_client = grpc_client

    async def Connect(self):
        await self._db_master.Connect()


    async def __Get_IDs(self, jwt: str, friend_email:str):
        user_id, nextToken = await self._grpc_client.LoginWithJWT(jwt)
        if user_id == -1:
            return None
        print('Get my id')
        friend_id = await self._grpc_client.GetIdFromEmail(friend_email)
        if friend_id == -1:
            print('Bad id')
            return None
        print('Get friend id')
        return user_id, friend_id, nextToken


    async def SendToEmail(self, jwt: str, friend_email: str, text_data: str):
        ids = await self.__Get_IDs(jwt, friend_email)
        print("Get ids")
        if ids is None:
            print("Bad id")
            return None
        user_id, friend_id, nextToken = ids
        await self._db_master.SendToUser(user_id, friend_id, text_data)
        print("Sended to user")
        return nextToken
    
    async def GetChat(self, jwt: str, friend_email: str):
        ids = await self.__Get_IDs(jwt, friend_email)
        if ids is None:
            return None
        user_id, friend_id, nextToken = ids
        rows = await self._db_master.GetAllMessagesFromChat(user_id, friend_id)
        print(rows['0'])
        print(nextToken)
        print(str(rows))
        return (nextToken, rows)
    
server_master = Server()


    
