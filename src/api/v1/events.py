from fastapi import APIRouter

router = APIRouter()

@router.on_event('startup')
async def startup():
    ...

@router.on_event('shutdown')
async def shutdown():
    ...
