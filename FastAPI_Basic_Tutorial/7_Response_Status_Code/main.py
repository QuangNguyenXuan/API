from fastapi import FastAPI

app = FastAPI()

@app.get("/items/", status_code=201)
async def get_item(name: str):
    return {"name": name}

@app.post("/items/", status_code=203)
async def create_item(name: str):
    return {"name": name}