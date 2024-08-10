import uvicorn
from var.vars import PORT
from endpoints.index import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(PORT))