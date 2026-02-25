import os
import pickle
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .logic import Item

app = FastAPI()
DB_FILE = "inventory_data.pkl"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    return {
        "items": [],
        "deleted": [],
        "categories": ["General"],
        "history": []
    }

db = load_db()

def save_db():
    with open(DB_FILE, "wb") as f:
        pickle.dump(db, f)

# ---------------- ITEMS ----------------

@app.get("/items")
def get_items():
    return db["items"]

@app.post("/items")
def add_item(item: Item):
    if item.id == 0:
        item.id = int(time.time())

    db["items"].append(item.dict())
    db["history"].append({"time": time.ctime(), "msg": f"Added {item.name}"})
    save_db()
    return {"status": "success"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    item = next((i for i in db["items"] if i["id"] == item_id), None)
    if item:
        db["items"] = [i for i in db["items"] if i["id"] != item_id]
        db["deleted"].append(item)
        db["history"].append({"time": time.ctime(), "msg": f"Deleted {item['name']}"})
        save_db()
    return {"status": "deleted"}

@app.post("/items/recover/{item_id}")
def recover_item(item_id: int):
    item = next((i for i in db["deleted"] if i["id"] == item_id), None)
    if item:
        db["items"].append(item)
        db["deleted"] = [i for i in db["deleted"] if i["id"] != item_id]
        db["history"].append({"time": time.ctime(), "msg": f"Recovered {item['name']}"})
        save_db()
        return {"status": "recovered"}
    return {"status": "error"}

@app.post("/items/consume/{item_id}")
def consume_item(item_id: int, amount: int):
    item = next((i for i in db["items"] if i["id"] == item_id), None)

    if not item:
        return {"status": "error"}

    if item["qty"] < amount:
        return {"status": "not enough stock"}

    item["qty"] -= amount
    db["history"].append({"time": time.ctime(),
                          "msg": f"Consumed {amount} of {item['name']}"})
    save_db()
    return {"status": "consumed"}

@app.put("/items/update/{item_id}")
def update_item(item_id: int, qty: int):
    item = next((i for i in db["items"] if i["id"] == item_id), None)
    if item:
        item["qty"] = qty
        db["history"].append({"time": time.ctime(),
                              "msg": f"Updated {item['name']} quantity to {qty}"})
        save_db()
        return {"status": "updated"}
    return {"status": "error"}

# ---------------- CATEGORY ----------------

class CategoryModel(BaseModel):
    category: str

@app.get("/categories")
def get_categories():
    return db["categories"]

@app.post("/categories")
def add_category(cat: CategoryModel):
    if cat.category not in db["categories"]:
        db["categories"].append(cat.category)
        save_db()
    return {"status": "added"}

# ---------------- HISTORY ----------------

@app.get("/history")
def get_history():
    return db["history"]
