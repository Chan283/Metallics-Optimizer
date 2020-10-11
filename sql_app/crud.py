from sqlalchemy.orm import Session

from . import models, schemas


def get_chemicals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chemical).offset(skip).limit(limit).all()


def delete_chemical(db: Session, chemical_id,commodity_id):
    db.query(models.Chemical).filter(models.Chemical.id == chemical_id, models.Chemical.cmdty_id == commodity_id).delete()
    db.commit()


def create_chemicals_for_commodity(db: Session, chemical: schemas.ChemicalCreate, commodity_id: int):
    db_chemical = models.Chemical(**chemical.dict(), cmdty_id=commodity_id)
    db.add(db_chemical)
    db.commit()
    db.refresh(db_chemical)
    return db_chemical

def create_commodity(db: Session, commodity:schemas.CommodityCreate):
    db_commodity = models.Commodity(**commodity.dict())
    db.add(db_commodity)
    db.commit()
    db.refresh(db_commodity)
    return db_commodity


def get_commodity(db: Session, commodity_id: int):
    return db.query(models.Commodity).filter(models.Commodity.id == commodity_id).first()


def update_commodity_by_id(db: Session, commodity_id, commodity:schemas.CommodityCreate):
    obj = db.query(models.Commodity).filter(models.Commodity.id == commodity_id).first()
    if obj.name:
        obj.name = commodity.name
    if obj.inventory:
        obj.inventory = commodity.inventory
    if obj.price:
        obj.price = commodity.price
    db.commit()
    return obj
