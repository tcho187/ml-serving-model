from typing import Union

from pydantic import BaseModel


class LeadBase(BaseModel):
    requested: int
    loan_purpose: Union[str, None] = None
    credit: int
    annual_income: int


class LeadCreate(LeadBase):
    pass


class Lead(LeadBase):
    lead_uuid: str

    class Config:
        orm_mode = True


class ClickBase(BaseModel):
    clicked_at: int


class ClickCreate(ClickBase):
    pass


class Click(ClickBase):
    offer_id: int

    class Config:
        orm_mode = True


class OfferBase(BaseModel):
    apr: int
    lead_uuid: str
    lender_id: int


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    offer_id: int


class Model(BaseModel):
    model_name: str


