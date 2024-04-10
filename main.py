import json

from fastapi import FastAPI

from models import Item, RequestItem

# Create app object of FastAPI()
app = FastAPI()

# Open json file
with open("store_items.json", "r") as file: 
    store_items_json = json.load(file)

store_items = []

for item in store_items_json:
    store_items.append(Item(**item))

def new_id() -> int:
    current_id = store_items[-1].id 
    while True:
        if current_id not in [item.id for item in store_items]:
            break
        current_id += 1
    return current_id

@app.get("/store_items")
async def get_items():
    return {"detail": store_items}

@app.post("/store_items")
async def add_item(item: RequestItem):
    item = Item(id=new_id(), **item.model_dump())
    store_items.append(item)
    return {"detail": f"Item with id: {item.id} has been inserted"}

@app.put("/store_items/{item_id}")
async def update_item(item_id: int, item: RequestItem):
    for i, item in enumerate(store_items):
        pass
        
    
    

@app.delete("/store_items/{item_id}")
async def delete_item():
    pass