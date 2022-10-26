from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from .database import Base


class Lead(Base):
    __tablename__ = "leads"

    lead_uuid = Column(String, primary_key=True, index=True)
    requested = Column(Integer)
    loan_purpose = Column(String)
    credit = Column(String)
    annual_income = Column(Integer)

    offers = relationship("Offer")


class Click(Base):
    __tablename__ = "clicks"

    offer_id = Column(Integer, primary_key=True, index=True)
    clicked_at = Column(DateTime)



class Offer(Base):
    __tablename__ = "offers"

    lead_uuid = Column(String, ForeignKey("leads.lead_uuid"), index=True)
    offer_id = Column(Integer, primary_key=True, index=True)
    apr = Column(Float)
    lender_id = Column(Integer)
    
    lead = relationship("Lead", back_populates="offers")
