from sqlalchemy.orm import Session
from datetime import datetime
from .models import Asset
from .schemas import AssetCreate, AssetUpdate
from sqlalchemy import asc, desc


def create_asset(db: Session, asset: AssetCreate):

    db_asset = Asset(
        **asset.model_dump()
    )

    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)

    return db_asset


def get_asset(db: Session, asset_id: str):

    return db.query(Asset).filter(
        Asset.id == asset_id
    ).first()


def get_assets(
        db: Session,
        type=None,
        status=None,
        value=None,
        tag=None,
        sort_by=None,
        skip=0,
        limit=10
):

    query = db.query(Asset)


    if type:
        query = query.filter(
            Asset.type == type
        )


    if status:
        query = query.filter(
            Asset.status == status
        )


    if value:
        query = query.filter(
            Asset.value.contains(value)
        )
    if tag:
        query = query.filter(
            Asset.tags.contains([tag])
        )
    if sort_by:

        sort_field = sort_by.lstrip("-")

        if hasattr(Asset, sort_field):

            if sort_by.startswith("-"):
                query = query.order_by(
                    desc(getattr(Asset, sort_field))
                )
            else:
                query = query.order_by(
                    asc(getattr(Asset, sort_field))
                )

    return query.offset(skip).limit(limit).all()


def update_asset(
        db: Session,
        asset_id: str,
        data: AssetUpdate
):

    asset = get_asset(db, asset_id)


    if not asset:
        return None


    for key,value in data.model_dump(
        exclude_unset=True
    ).items():

        setattr(asset,key,value)


    asset.last_seen = datetime.utcnow()


    db.commit()
    db.refresh(asset)

    return asset

def delete_asset(db:Session, asset_id:str):

    asset=get_asset(db,asset_id)


    if asset:

        db.delete(asset)
        db.commit()


    return asset

def create_relationship(
        db: Session,
        source_id: str,
        target_id: str
):

    source = db.query(Asset).filter(
        Asset.id == source_id
    ).first()


    target = db.query(Asset).filter(
        Asset.id == target_id
    ).first()

    if not source or not target:
        return None

    if source_id == target_id:
        return None


    source.related_assets.append(target)


    db.commit()


    return source

def get_relationships(
        db: Session,
        asset_id: str
):

    asset = db.query(Asset).filter(
        Asset.id == asset_id
    ).first()


    if not asset:
        return None


    return asset.related_assets

def mark_stale(db: Session, asset_id: str):

    asset = get_asset(db, asset_id)

    if not asset:
        return None

    asset.status = "stale"
    db.commit()
    db.refresh(asset)

    return asset