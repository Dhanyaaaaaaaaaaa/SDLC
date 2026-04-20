from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import date, datetime

# User Models
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: str
    is_active: bool
    role: str

# Auth Token
class Token(BaseModel):
    access_token: str
    token_type: str

# Crop Models
class CropBase(BaseModel):
    crop_type: str
    planting_date: date
    expected_harvest_date: date
    growth_stage: Optional[str] = None
    health_status: Optional[str] = None
    notes: Optional[str] = None

class CropCreate(CropBase):
    pass

class CropUpdate(BaseModel):
    crop_type: Optional[str]
    planting_date: Optional[date]
    expected_harvest_date: Optional[date]
    growth_stage: Optional[str]
    health_status: Optional[str]
    notes: Optional[str]

class CropOut(CropBase):
    id: str
    owner_id: str
    is_harvested: bool
    created_at: datetime
    updated_at: datetime

# Task Models
class TaskBase(BaseModel):
    crop_id: str
    title: str
    description: Optional[str] = None
    due_date: date
    status: str = "pending"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[date]
    status: Optional[str]

class TaskOut(TaskBase):
    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

# Notification Models
class NotificationOut(BaseModel):
    id: str
    user_id: str
    message: str
    created_at: datetime
    read: bool

# Weather Models
class WeatherOut(BaseModel):
    location: str
    current: Dict
    forecast: List[Dict]
    alerts: List[Dict]

# Reporting
class ReportRequest(BaseModel):
    crop_ids: List[str]
    start_date: date
    end_date: date
    format: str = Field(regex="^(pdf|csv)$")

class ReportOut(BaseModel):
    url: str
    generated_at: datetime

# Book Catalog
class BookBase(BaseModel):
    title: str
    author: str
    price: float
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    price: Optional[float]
    description: Optional[str]

class BookOut(BookBase):
    id: str
    created_at: datetime
    updated_at: datetime

# Cart
class CartItem(BaseModel):
    book_id: str
    quantity: int

class CartOut(BaseModel):
    user_id: str
    items: List[CartItem]

# Order
class OrderCreate(BaseModel):
    items: List[CartItem]
    shipping_address: str
    payment_method: str

class OrderOut(BaseModel):
    id: str
    user_id: str
    items: List[CartItem]
    total: float
    status: str
    created_at: datetime

# Restaurant
class RestaurantBase(BaseModel):
    name: str
    address: str
    contact: str
    hours: str
    rating: float
    menu: List[Dict]

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    contact: Optional[str]
    hours: Optional[str]
    rating: Optional[float]
    menu: Optional[List[Dict]]

class RestaurantOut(RestaurantBase):
    id: str
    created_at: datetime
    updated_at: datetime
