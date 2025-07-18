from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from utils.ping_checker import check_online_sync
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import asyncio

router = APIRouter(tags=["utils"])
security = HTTPBasic()

async def check_ip(ip: str) -> tuple[str, bool]:
    status = await asyncio.to_thread(check_online_sync, ip)
    return ip, status

@router.post("/sites/status", response_model=Dict[str, bool])
async def get_sites_status(ips: List[str], credentials: HTTPBasicCredentials = Depends(security)):
    if not ips:
        raise HTTPException(status_code=400, detail="Nenhum IP fornecido.")
    
    results = await asyncio.gather(*(check_ip(ip) for ip in ips))
    status_map = dict(results)
    return status_map
