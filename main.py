from fastapi import FastAPI
from routes import basalam_client


app = FastAPI()



app.include_router(basalam_client.basalam_client, prefix="/basalam/client", tags=["basalam_client"])


@app.get("/")
async def get_root():
    return "You are very welcome :)"