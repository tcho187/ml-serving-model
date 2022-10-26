from sqlalchemy.orm import Session

from . import models, schemas


def get_lead(db: Session, lead_uuid: int):
    return db.query(models.Lead).filter(models.Lead.lead_uuid == lead_uuid).first()


def get_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lead).offset(skip).limit(limit).all()


def create_lead(db: Session, lead: schemas.LeadCreate):
    db_user = models.Lead(lead_uuid=lead.lead_uuid, requested=lead.requested, loan_purpose=lead.loan_purpose, credit=lead.credit, annual_income=lead.annual_income)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item




def get_click(db: Session, offer_id: int):
    return db.query(models.click).filter(models.click.offer_id == offer_id).first()


def get_clicks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.click).offset(skip).limit(limit).all()


def create_click(db: Session, click: schemas.ClickCreate):
    db_user = models.click(**click.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_offer(db: Session, offer_id: int):
    return db.query(models.offer).filter(models.offer.offer_id == offer_id).first()


def get_offers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.offer).offset(skip).limit(limit).all()


def create_offer(db: Session, offer: schemas.OfferCreate):
    db_user = models.offer(**offer.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
