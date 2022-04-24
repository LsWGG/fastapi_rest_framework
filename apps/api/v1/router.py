import time

from fastapi import APIRouter

from apps.api.v1.books_api import books_router
from apps.api.v1.books_api.book_manage import BookViewSet

api_router = APIRouter()
api_router.include_router(books_router.is_view(BookViewSet))
