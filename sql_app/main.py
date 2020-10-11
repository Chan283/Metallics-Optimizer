import secrets

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

####################################################################################################

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "chan")
    correct_password = secrets.compare_digest(credentials.password, "chan123")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

####################################################################################################


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/chemicals/", response_model=List[schemas.Chemical])
def get_all_chemicals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    chemicals = crud.get_chemicals(db, skip=skip, limit=limit)
    return chemicals


@app.post("/commodity/{commodity_id}/chemicals/", response_model=schemas.Chemical)
def create_chemicals_for_commodity(
    commodity_id: int, chemical: schemas.ChemicalCreate, db: Session = Depends(get_db), username: str = Depends(get_current_username)
):
    return crud.create_chemicals_for_commodity(db=db, chemical=chemical, commodity_id=commodity_id)


@app.delete("/commodity/{commodity_id}/{chemical_id}")
def delete_chemicals_for_commodity(commodity_id: int, chemical_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    crud.delete_chemical(db=db, chemical_id=chemical_id,commodity_id=commodity_id)
    return {"commodity_id":commodity_id,"chemical_id":chemical_id}


@app.post("/commodity/", response_model=schemas.Commodity)
def create_commodity(commodity: schemas.CommodityCreate, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    return crud.create_commodity(db=db, commodity=commodity)


@app.get("/commodities/{commodity_id}", response_model=schemas.Commodity)
def get_commodity_by_id(commodity_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    db_commodity = crud.get_commodity(db, commodity_id=commodity_id)
    """
    chem_compo_sum= sum([i.percentage for i in db_commodity.chemicals])
    if chem_compo_sum<100:
        per_to_add=100-chem_compo_sum
        crud.create_chemicals_for_commodity(commodity_id=commodity_id, chemical=schemas.ChemicalCreate("name":"unknown","percentage":per_to_add),db=db)
    """
    if db_commodity is None:
        raise HTTPException(status_code=404, detail="Commodity not found")
    return db_commodity


@app.put("/commodities/{commodity_id}", response_model=schemas.Commodity)
def update_commodity_by_id(commodity_id: int, commodity: schemas.CommodityCreate, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    crud.get_commodity(db, commodity_id=commodity_id)
    obj = crud.update_commodity_by_id(db=db, commodity_id=commodity_id, commodity=commodity)
    return obj
