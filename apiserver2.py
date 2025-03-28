from fastapi import FastAPI
from database import collection, client
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
import os

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI Math API with MongoDB Atlas"}

@app.post("/add/{num1}/{num2}")
async def add(num1: int, num2: int):
    result = num1 + num2
    record = {"operation": "add", "num1": num1, "num2": num2, "result": result}
    insert_result = await collection.insert_one(record)
    return {"id": str(insert_result.inserted_id), "result": result}

@app.post("/subtract/{num1}/{num2}")
async def subtract(num1: int, num2: int):
    result = num1 - num2
    record = {"operation": "subtract", "num1": num1, "num2": num2, "result": result}
    insert_result = await collection.insert_one(record)
    return {"id": str(insert_result.inserted_id), "result": result}

@app.post("/multiply/{num1}/{num2}")
async def multiply(num1: int, num2: int):
    result = num1 * num2
    record = {"operation": "multiply", "num1": num1, "num2": num2, "result": result}
    insert_result = await collection.insert_one(record)
    return {"id": str(insert_result.inserted_id), "result": result}

@app.get("/history/")
async def get_history():
    history = []
    async for record in collection.find():
        history.append({
            "id": str(record["_id"]), 
            "operation": record["operation"], 
            "num1": record["num1"], 
            "num2": record["num2"], 
            "result": record["result"]
        })
    return {"history": history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apiserver2:app", host="0.0.0.0", port=8000, reload=True)
