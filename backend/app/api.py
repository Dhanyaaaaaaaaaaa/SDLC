from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from app.models import *
from app.services import *
from app.utils import get_current_user

api_router = APIRouter()

# --- Auth ---
@api_router.post("/auth/register", response_model=UserOut)
def register(user: UserCreate):
    try:
        return create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token({"sub": user.id})
    return Token(access_token=token, token_type="bearer")

@api_router.get("/auth/me", response_model=UserOut)
def get_me(user: UserOut = Depends(get_current_user)):
    return user

# --- Crop CRUD ---
@api_router.post("/crops", response_model=CropOut)
def add_crop(crop: CropCreate, user: UserOut = Depends(get_current_user)):
    return create_crop(user.id, crop)

@api_router.get("/crops", response_model=List[CropOut])
def get_crops(user: UserOut = Depends(get_current_user)):
    return list_crops(user.id)

@api_router.get("/crops/{crop_id}", response_model=CropOut)
def get_crop_detail(crop_id: str, user: UserOut = Depends(get_current_user)):
    crop = get_crop(user.id, crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop

@api_router.put("/crops/{crop_id}", response_model=CropOut)
def update_crop_api(crop_id: str, crop: CropUpdate, user: UserOut = Depends(get_current_user)):
    updated = update_crop(user.id, crop_id, crop)
    if not updated:
        raise HTTPException(status_code=404, detail="Crop not found or not owned by user")
    return updated

@api_router.delete("/crops/{crop_id}")
def delete_crop_api(crop_id: str, user: UserOut = Depends(get_current_user)):
    if not delete_crop(user.id, crop_id):
        raise HTTPException(status_code=404, detail="Crop not found or not owned by user")
    return {"ok": True}

@api_router.post("/crops/{crop_id}/harvest", response_model=CropOut)
def mark_harvested(crop_id: str, user: UserOut = Depends(get_current_user)):
    crop = mark_crop_harvested(user.id, crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found or not owned by user")
    return crop

# --- Task CRUD ---
@api_router.post("/tasks", response_model=TaskOut)
def add_task(task: TaskCreate, user: UserOut = Depends(get_current_user)):
    return create_task(user.id, task)

@api_router.get("/tasks", response_model=List[TaskOut])
def get_tasks(crop_id: Optional[str] = None, user: UserOut = Depends(get_current_user)):
    return list_tasks(user.id, crop_id)

@api_router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task_detail(task_id: str, user: UserOut = Depends(get_current_user)):
    task = get_task(user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@api_router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task_api(task_id: str, task: TaskUpdate, user: UserOut = Depends(get_current_user)):
    updated = update_task(user.id, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return updated

@api_router.delete("/tasks/{task_id}")
def delete_task_api(task_id: str, user: UserOut = Depends(get_current_user)):
    if not delete_task(user.id, task_id):
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return {"ok": True}

@api_router.post("/tasks/{task_id}/complete", response_model=TaskOut)
def mark_task_complete_api(task_id: str, user: UserOut = Depends(get_current_user)):
    task = mark_task_complete(user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return task

# --- Notifications ---
@api_router.get("/notifications", response_model=List[NotificationOut])
def get_notifications(user: UserOut = Depends(get_current_user)):
    return list_notifications(user.id)

@api_router.post("/notifications/{notif_id}/read", response_model=NotificationOut)
def mark_notification_read_api(notif_id: str, user: UserOut = Depends(get_current_user)):
    notif = mark_notification_read(user.id, notif_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found or not owned by user")
    return notif

# --- Book Catalog ---
@api_router.post("/books", response_model=BookOut)
def add_book(book: BookCreate):
    return create_book(book)

@api_router.get("/books", response_model=List[BookOut])
def get_books():
    return list_books()

@api_router.get("/books/{book_id}", response_model=BookOut)
def get_book_detail(book_id: str):
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@api_router.put("/books/{book_id}", response_model=BookOut)
def update_book_api(book_id: str, book: BookUpdate):
    updated = update_book(book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@api_router.delete("/books/{book_id}")
def delete_book_api(book_id: str):
    if not delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"ok": True}

# --- Cart ---
@api_router.get("/cart", response_model=CartOut)
def get_cart_api(user: UserOut = Depends(get_current_user)):
    return get_cart(user.id)

@api_router.post("/cart/add", response_model=CartOut)
def add_to_cart_api(item: CartItem, user: UserOut = Depends(get_current_user)):
    return add_to_cart(user.id, item)

@api_router.post("/cart/remove", response_model=CartOut)
def remove_from_cart_api(book_id: str, user: UserOut = Depends(get_current_user)):
    return remove_from_cart(user.id, book_id)

# --- Orders ---
@api_router.post("/orders", response_model=OrderOut)
def create_order_api(order: OrderCreate, user: UserOut = Depends(get_current_user)):
    return create_order(user.id, order)

@api_router.get("/orders", response_model=List[OrderOut])
def get_orders_api(user: UserOut = Depends(get_current_user)):
    return list_orders(user.id)

# --- Restaurant ---
@api_router.post("/restaurants", response_model=RestaurantOut)
def add_restaurant(rest: RestaurantCreate):
    return create_restaurant(rest)

@api_router.get("/restaurants", response_model=List[RestaurantOut])
def get_restaurants():
    return list_restaurants()

@api_router.get("/restaurants/{rest_id}", response_model=RestaurantOut)
def get_restaurant_detail(rest_id: str):
    rest = get_restaurant(rest_id)
    if not rest:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return rest

@api_router.put("/restaurants/{rest_id}", response_model=RestaurantOut)
def update_restaurant_api(rest_id: str, rest: RestaurantUpdate):
    updated = update_restaurant(rest_id, rest)
    if not updated:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return updated
