import uuid
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.models import *

# In-memory stores for demo (replace with DB in production)
USERS: Dict[str, dict] = {}
CROPS: Dict[str, dict] = {}
TASKS: Dict[str, dict] = {}
NOTIFICATIONS: Dict[str, dict] = {}
BOOKS: Dict[str, dict] = {}
CARTS: Dict[str, dict] = {}
ORDERS: Dict[str, dict] = {}
RESTAURANTS: Dict[str, dict] = {}

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_user(user: UserCreate) -> UserOut:
    for u in USERS.values():
        if u["email"] == user.email:
            raise ValueError("Email already registered")
    user_id = str(uuid.uuid4())
    USERS[user_id] = {
        "id": user_id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "hashed_password": get_password_hash(user.password),
        "is_active": True,
        "role": "farmer",
        "created_at": datetime.utcnow(),
    }
    return UserOut(id=user_id, email=user.email, full_name=user.full_name, phone=user.phone, is_active=True, role="farmer")

def authenticate_user(email: str, password: str) -> Optional[UserOut]:
    for u in USERS.values():
        if u["email"] == email and verify_password(password, u["hashed_password"]):
            return UserOut(id=u["id"], email=u["email"], full_name=u["full_name"], phone=u["phone"], is_active=u["is_active"], role=u["role"])
    return None

def get_user_by_id(user_id: str) -> Optional[UserOut]:
    u = USERS.get(user_id)
    if not u:
        return None
    return UserOut(id=u["id"], email=u["email"], full_name=u["full_name"], phone=u["phone"], is_active=u["is_active"], role=u["role"])

def create_crop(owner_id: str, crop: CropCreate) -> CropOut:
    crop_id = str(uuid.uuid4())
    now = datetime.utcnow()
    CROPS[crop_id] = {
        **crop.dict(),
        "id": crop_id,
        "owner_id": owner_id,
        "is_harvested": False,
        "created_at": now,
        "updated_at": now,
    }
    return CropOut(id=crop_id, owner_id=owner_id, is_harvested=False, created_at=now, updated_at=now, **crop.dict())

def update_crop(owner_id: str, crop_id: str, crop: CropUpdate) -> Optional[CropOut]:
    c = CROPS.get(crop_id)
    if not c or c["owner_id"] != owner_id:
        return None
    for k, v in crop.dict(exclude_unset=True).items():
        c[k] = v
    c["updated_at"] = datetime.utcnow()
    return CropOut(**c)

def delete_crop(owner_id: str, crop_id: str) -> bool:
    c = CROPS.get(crop_id)
    if not c or c["owner_id"] != owner_id:
        return False
    del CROPS[crop_id]
    return True

def list_crops(owner_id: str) -> List[CropOut]:
    return [CropOut(**c) for c in CROPS.values() if c["owner_id"] == owner_id]

def get_crop(owner_id: str, crop_id: str) -> Optional[CropOut]:
    c = CROPS.get(crop_id)
    if not c or c["owner_id"] != owner_id:
        return None
    return CropOut(**c)

def mark_crop_harvested(owner_id: str, crop_id: str) -> Optional[CropOut]:
    c = CROPS.get(crop_id)
    if not c or c["owner_id"] != owner_id:
        return None
    c["is_harvested"] = True
    c["updated_at"] = datetime.utcnow()
    return CropOut(**c)

def create_task(owner_id: str, task: TaskCreate) -> TaskOut:
    task_id = str(uuid.uuid4())
    now = datetime.utcnow()
    TASKS[task_id] = {
        **task.dict(),
        "id": task_id,
        "owner_id": owner_id,
        "created_at": now,
        "updated_at": now,
    }
    return TaskOut(id=task_id, owner_id=owner_id, created_at=now, updated_at=now, **task.dict())

def update_task(owner_id: str, task_id: str, task: TaskUpdate) -> Optional[TaskOut]:
    t = TASKS.get(task_id)
    if not t or t["owner_id"] != owner_id:
        return None
    for k, v in task.dict(exclude_unset=True).items():
        t[k] = v
    t["updated_at"] = datetime.utcnow()
    return TaskOut(**t)

def delete_task(owner_id: str, task_id: str) -> bool:
    t = TASKS.get(task_id)
    if not t or t["owner_id"] != owner_id:
        return False
    del TASKS[task_id]
    return True

def list_tasks(owner_id: str, crop_id: Optional[str] = None) -> List[TaskOut]:
    return [TaskOut(**t) for t in TASKS.values() if t["owner_id"] == owner_id and (crop_id is None or t["crop_id"] == crop_id)]

def get_task(owner_id: str, task_id: str) -> Optional[TaskOut]:
    t = TASKS.get(task_id)
    if not t or t["owner_id"] != owner_id:
        return None
    return TaskOut(**t)

def mark_task_complete(owner_id: str, task_id: str) -> Optional[TaskOut]:
    t = TASKS.get(task_id)
    if not t or t["owner_id"] != owner_id:
        return None
    t["status"] = "completed"
    t["updated_at"] = datetime.utcnow()
    return TaskOut(**t)

def create_notification(user_id: str, message: str) -> NotificationOut:
    notif_id = str(uuid.uuid4())
    now = datetime.utcnow()
    NOTIFICATIONS[notif_id] = {
        "id": notif_id,
        "user_id": user_id,
        "message": message,
        "created_at": now,
        "read": False,
    }
    return NotificationOut(**NOTIFICATIONS[notif_id])

def list_notifications(user_id: str) -> List[NotificationOut]:
    return [NotificationOut(**n) for n in NOTIFICATIONS.values() if n["user_id"] == user_id]

def mark_notification_read(user_id: str, notif_id: str) -> Optional[NotificationOut]:
    n = NOTIFICATIONS.get(notif_id)
    if not n or n["user_id"] != user_id:
        return None
    n["read"] = True
    return NotificationOut(**n)
# --- Book Catalog ---
def create_book(book: BookCreate) -> BookOut:
    book_id = str(uuid.uuid4())
    now = datetime.utcnow()
    BOOKS[book_id] = {
        **book.dict(),
        "id": book_id,
        "created_at": now,
        "updated_at": now,
    }
    return BookOut(id=book_id, created_at=now, updated_at=now, **book.dict())

def update_book(book_id: str, book: BookUpdate) -> Optional[BookOut]:
    b = BOOKS.get(book_id)
    if not b:
        return None
    for k, v in book.dict(exclude_unset=True).items():
        b[k] = v
    b["updated_at"] = datetime.utcnow()
    return BookOut(**b)

def delete_book(book_id: str) -> bool:
    if book_id in BOOKS:
        del BOOKS[book_id]
        return True
    return False

def list_books() -> List[BookOut]:
    return [BookOut(**b) for b in BOOKS.values()]

def get_book(book_id: str) -> Optional[BookOut]:
    b = BOOKS.get(book_id)
    if not b:
        return None
    return BookOut(**b)
# --- Cart ---
def get_cart(user_id: str) -> CartOut:
    cart = CARTS.get(user_id, {"user_id": user_id, "items": []})
    return CartOut(**cart)

def add_to_cart(user_id: str, item: CartItem) -> CartOut:
    cart = CARTS.setdefault(user_id, {"user_id": user_id, "items": []})
    for i in cart["items"]:
        if i["book_id"] == item.book_id:
            i["quantity"] += item.quantity
            break
    else:
        cart["items"].append(item.dict())
    return CartOut(**cart)

def remove_from_cart(user_id: str, book_id: str) -> CartOut:
    cart = CARTS.setdefault(user_id, {"user_id": user_id, "items": []})
    cart["items"] = [i for i in cart["items"] if i["book_id"] != book_id]
    return CartOut(**cart)

def clear_cart(user_id: str):
    CARTS[user_id] = {"user_id": user_id, "items": []}
# --- Orders ---
def create_order(user_id: str, order: OrderCreate) -> OrderOut:
    order_id = str(uuid.uuid4())
    now = datetime.utcnow()
    total = 0.0
    for item in order.items:
        book = BOOKS.get(item.book_id)
        if book:
            total += book["price"] * item.quantity
    ORDERS[order_id] = {
        "id": order_id,
        "user_id": user_id,
        "items": [item.dict() for item in order.items],
        "total": total,
        "status": "confirmed",
        "created_at": now,
    }
    clear_cart(user_id)
    return OrderOut(id=order_id, user_id=user_id, items=order.items, total=total, status="confirmed", created_at=now)

def list_orders(user_id: str) -> List[OrderOut]:
    return [OrderOut(**o) for o in ORDERS.values() if o["user_id"] == user_id]
# --- Restaurant ---
def create_restaurant(rest: RestaurantCreate) -> RestaurantOut:
    rest_id = str(uuid.uuid4())
    now = datetime.utcnow()
    RESTAURANTS[rest_id] = {
        **rest.dict(),
        "id": rest_id,
        "created_at": now,
        "updated_at": now,
    }
    return RestaurantOut(id=rest_id, created_at=now, updated_at=now, **rest.dict())

def update_restaurant(rest_id: str, rest: RestaurantUpdate) -> Optional[RestaurantOut]:
    r = RESTAURANTS.get(rest_id)
    if not r:
        return None
    for k, v in rest.dict(exclude_unset=True).items():
        r[k] = v
    r["updated_at"] = datetime.utcnow()
    return RestaurantOut(**r)

def list_restaurants() -> List[RestaurantOut]:
    return [RestaurantOut(**r) for r in RESTAURANTS.values()]

def get_restaurant(rest_id: str) -> Optional[RestaurantOut]:
    r = RESTAURANTS.get(rest_id)
    if not r:
        return None
    return RestaurantOut(**r)
