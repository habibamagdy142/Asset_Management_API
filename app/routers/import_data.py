from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import json
from ..dependencies import verify_api_key
from ..database import get_db
from ..models import Asset


router = APIRouter(
    prefix="/import",
    tags=["Import"]
)

@router.post("/")
async def import_assets(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    auth = Depends(verify_api_key)
):

    data = json.load(file.file)


    imported = 0
    updated = 0

    skipped = 0
    errors = []
    allowed_fields = {
        "id",
        "type",
        "value",
        "status",
        "source",
        "tags",
        "metadata"
    }

    relationships = []


    for item in data:

        try:

            if "type" not in item or "value" not in item:
                raise ValueError("Missing required fields")

            existing = db.query(Asset).filter(
                Asset.type == item["type"],
                Asset.value == item["value"]
            ).first()
            if item.get("parent") and item.get("id"):
                relationships.append(
                    {
                        "source": item["parent"],
                        "target": item["id"]
                    }
                )

            if item.get("covers") and item.get("id"):
                relationships.append(
                    {
                        "source": item["covers"],
                        "target": item["id"]
                    }
                )

            if existing:

                existing.last_seen = datetime.utcnow()
                existing.status = "active"

                existing.tags = list(
                    set(
                        (existing.tags or [])
                        +
                        item.get("tags", [])
                    )
                )

                existing.asset_metadata = {
                    **(existing.asset_metadata or {}),
                    **(item.get("metadata") or {})
                }


                updated += 1



            else:

                asset_data = {

                    key: value

                    for key, value in item.items()

                    if key in allowed_fields

                }
                if "metadata" in asset_data:
                    asset_data["asset_metadata"] = asset_data.pop("metadata")

                asset = Asset(

                    **asset_data

                )


                db.add(asset)

                imported += 1


        except Exception as e:

            skipped += 1
            errors.append(str(e))

    db.commit()

    for relation in relationships:

        source = db.query(Asset).filter(
            Asset.id == relation["source"]
        ).first()

        target = db.query(Asset).filter(
            Asset.id == relation["target"]
        ).first()

        if source and target:
          if target not in source.related_assets:
            source.related_assets.append(target)

    db.commit()

    return {
        "new_assets": imported,
        "updated_assets": updated,
        "skipped": skipped,
        "errors": errors
    }