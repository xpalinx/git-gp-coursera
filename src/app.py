from database import get_db, startup_event
from fastapi import FastAPI
from models import Item
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()
app.add_event_handler("startup", startup_event)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": "Validation error", "errors": exc.errors()})

@app.post("/items/")
def create_item(item:Item):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, price, is_offer) VALUES (?, ?, ?)", (item.name, item.price, int(item.is_offer) if item.is_offer else None), )
    conn.commit()
    item.id = cursor.lastrowid
    return item

@app.put("/items/{item_id}")
def update_item(item_id:int, item:Item):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE  items SET name = ?, price=?, is_offer = ?  WHERE id  = ?", (item.name, item.price, int(item.is_offer) if item.is_offer else None, item_id), )
    conn.commit()
    item.id = cursor.lastrowid
    return item

@app.delete("/items/{item_id}")
def update_item(item_id:int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE  FROM items  WHERE id  = ?", (item_id,))
    conn.commit()
    return {"message": "Item deleted"}

