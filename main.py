import json

from fastapi import FastAPI, HTTPException, status

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
    latest_id = store_items[-1].id 
    while True:
        if latest_id not in [item.id for item in store_items]:
            break
        latest_id += 1
    return latest_id

@app.get("/store_items")
async def get_items():
    return {"detail": store_items}

@app.post("/store_items")
async def add_item(item: RequestItem):
    item = Item(id=new_id(), **item.model_dump())
    store_items.append(item)
    with open("store_items.json", "w") as file:
        json.dump([store_item.json() for store_item in store_items], file, indent=4)
    return {"detail": f"Item with id: {item.id} has been inserted."}

@app.put("/store_items/{item_id}")
async def update_item(item_id: int, new_item: RequestItem):
    for item in store_items:
        if item.id == item_id:
            for attr, value in new_item.model_dump().items():
                setattr(item, attr, value)
            with open("store_items.json", "w") as file:
                json.dump([store_item.json() for store_item in store_items], file, indent=4)
            return {"detail": f"Item with id: {item.id} has been updated."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id: {item_id} not found.")


@app.delete("/store_items/{item_id}")
async def delete_item(item_id: int):
    for i, item in enumerate(store_items):
        if item.id == item_id:
            store_items.pop(i)
            with open("store_items.json", "w") as file:
                json.dump([store_item.json() for store_item in store_items], file, indent=4)
            return {"detail": f"Item with id: {item_id} has been deleted."}
            