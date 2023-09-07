from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from generators.api.models import ConversionResponse, ConversionRequest
from generators.type_loader import get_source_cls, get_target_cls

router = APIRouter()


@router.post("", response_model=ConversionResponse)
async def convert(req: ConversionRequest):
    source_cls = get_source_cls(req.source_type)
    sb = source_cls(req.content)
    try:
        decoded = sb.decode()
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    try:
        target_cls = get_target_cls(req.language, req.target_type)
    except IndexError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="No such target type class")
    db = target_cls(sb.get_model(decoded), req.source_type, **(req.config or {}))
    return {"content": db.render()}
