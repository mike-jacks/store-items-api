import json

from fastapi import FastAPI, HTTPException, status

from models import Item, RequestItem

# Create app object of FastAPI()
app = FastAPI()

# Open json file
with open("store_items.json", "r") as file: 
    store_items_json = json.load(file)


def load_items() -> list[Item]:
    store_items = []
    with open("store_items.json", "r") as file: 
        store_items_json = json.load(file)
    for item in store_items_json:
        store_items.append(Item(**item))
    return store_items
    
    
def save_items(data: list[Item]):
    with open("store_items.json", "w") as file:
        json.dump([store_item.model_dump() for store_item in data], file, indent=2)
        
def new_id_from(data: list[Item]) -> int:
    latest_id = data[-1].id 
    while True:
        if latest_id not in [item.id for item in data]:
            break
        latest_id += 1
    return latest_id

data = load_items()

@app.get("/store_items")
async def get_items():
    return {"detail": data}

@app.post("/store_items")
async def add_item(item: RequestItem):
    item = Item(id=new_id_from(data=data), **item.model_dump())
    data.append(item)
    save_items(data)
    return {"detail": f"Item with id: {item.id} has been inserted."}

@app.put("/store_items/{item_id}")
async def update_item(item_id: int, new_item: RequestItem):
    for item in data:
        if item.id == item_id:
            for attr, value in new_item.model_dump().items():
                setattr(item, attr, value)
            save_items(data)
            return {"detail": f"Item with id: {item.id} has been updated."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id: {item_id} not found.")


@app.delete("/store_items/{item_id}")
async def delete_item(item_id: int):
    for i, item in enumerate(data):
        if item.id == item_id:
            data.pop(i)
            save_items(data)
            return {"detail": f"Item with id: {item_id} has been deleted."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id: {item_id} not found.")
            