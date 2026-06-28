from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import AssetCreate,AssetUpdate
from .. import crud
from ..dependencies import verify_api_key

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)

@router.post("/")
def create_asset(
    asset:AssetCreate,
    db:Session=Depends(get_db),
    auth=Depends(verify_api_key)
):

    return crud.create_asset(db,asset)

@router.get("/")
def get_assets(
    type:str=None,
    status:str=None,
    value:str=None,
     tag:str=None,
    sort_by:str=None,
    skip:int=0,
    limit:int=10,
    db:Session=Depends(get_db)
):

    return crud.get_assets(
        db,
        type,
        status,
        value,
        tag,
        sort_by,
        skip,
        limit
    )


@router.get("/{asset_id}")
def get_asset(
    asset_id:str,
    db:Session=Depends(get_db)
):

    asset = crud.get_asset(
        db,
        asset_id
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset

@router.put("/{asset_id}")
def update_asset(
    asset_id:str,
    data:AssetUpdate,
    db:Session=Depends(get_db),
    auth=Depends(verify_api_key)
):
    asset = crud.update_asset(
        db,
        asset_id,
        data
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@router.delete("/{asset_id}")
def delete_asset(
    asset_id:str,
    db:Session=Depends(get_db),
    auth=Depends(verify_api_key)
):
    asset = crud.delete_asset(
        db,
        asset_id
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset

@router.patch("/{asset_id}/mark-stale")
def mark_asset_stale(
    asset_id: str,
    db: Session = Depends(get_db),
    auth = Depends(verify_api_key)
):
    asset = crud.mark_stale(db, asset_id)

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset