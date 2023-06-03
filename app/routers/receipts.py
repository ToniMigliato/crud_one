from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import database, models, schemas, oauth2

router = APIRouter(
    prefix='/receipts',
    tags=['Receipts']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ReceiptResponse)
async def create_receipt(receipt: schemas.ReceiptCreate, db: Session=Depends(database.get_db)):
    db_receipt = models.Receipt(user_id_fk=receipt.user_id_fk)
    db.add(db_receipt)
    for item in receipt.items:
        product = db.query(models.Products).get(item.product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Product id {item.product_id} not found.')
        db_item = models.ReceiptItems(product_id_fk=item.product_id, 
                                      quantity=item.quantity, 
                                      price=product.product_price)
        db_receipt.receipt_items.append(db_item)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt

@router.get('/', response_model=List[schemas.ReceiptResponseTotal])
async def get_all_receipts(db: Session=Depends(database.get_db)):
    receipts = db.query(models.Receipt).all()
    for receipt in receipts:
        total = receipt.total
        print(total)
    return receipts