from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(tags=["scores"])


@router.post("/scores", status_code=201)
def save_score(
    body: schemas.GameRecordCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = models.GameRecord(
        user_id=current_user.id,
        score=body.score,
        level=body.level,
        lines=body.lines,
    )
    db.add(record)
    db.commit()
    return {"message": "점수가 저장됐습니다"}


@router.get("/scores/top", response_model=schemas.TopScore)
def get_top_score(db: Session = Depends(get_db)):
    row = (
        db.query(models.User.nickname, models.GameRecord.score)
        .join(models.GameRecord, models.User.id == models.GameRecord.user_id)
        .order_by(models.GameRecord.score.desc())
        .first()
    )
    if not row:
        return {"nickname": "-", "score": 0}
    return {"nickname": row.nickname, "score": row.score}


@router.get("/scores/me", response_model=list[schemas.GameRecordOut])
def get_my_scores(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.GameRecord)
        .filter(models.GameRecord.user_id == current_user.id)
        .order_by(models.GameRecord.played_at.desc())
        .all()
    )
