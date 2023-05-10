from fastapi.responses import JSONResponse, FileResponse, Response
from application import app
from GroupsMaster import SendModel, GetChatModel
from ServerMaster import server_master





main_app = app

@app.get("/")
async def root():
    return FileResponse('public/test.html')

@app.post("/send", response_class=JSONResponse)
async def TrySend(request: SendModel):
    try:
        print("Get request")
        result = await server_master.SendToEmail(request.jwt, request.friend_email, request.text_data)
        if result is None:
            raise Exception()
        return JSONResponse({'nextToken': result})
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=401)
    

@app.post('/get_chat', response_class=JSONResponse)
async def GetChat(request: GetChatModel):
    try:
        result = await server_master.GetChat(request.jwt, request.friend_email)
        if result is None:
            raise Exception()
        return JSONResponse({'nextToken': result[0], 'rows': str(result[1])})
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=401)
    

