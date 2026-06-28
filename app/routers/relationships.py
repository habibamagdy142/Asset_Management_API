from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import verify_api_key
from ..database import get_db
from ..models import Asset

router = APIRouter(
    prefix="/relationships",
    tags=["Relationships"]
)


@router.post("/")
def create_relationship(
    source_id: str,
    target_id: str,
    db: Session = Depends(get_db),
    auth=Depends(verify_api_key)
):

    source = db.query(Asset).filter(
        Asset.id == source_id
    ).first()


    target = db.query(Asset).filter(
        Asset.id == target_id
    ).first()


    if not source or not target:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )
    if target in source.related_assets:
        raise HTTPException(
            status_code=400,
            detail="Relationship already exists"
        )


    source.related_assets.append(target)

    db.commit()


    return {
        "message": "Relationship created"
    }



@router.get("/{asset_id}")
def get_relationships(
    asset_id: str,
    db: Session = Depends(get_db)
):

    asset = db.query(Asset).filter(
        Asset.id == asset_id
    ).first()


    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )


    return asset.related_assets