from fastapi import APIRouter
from .auth_user import router_auth
from .whitelist import router_whitelist

router = APIRouter(prefix='/user', tags=['Users'])
router.include_router(router_auth)
router.include_router(router_whitelist)