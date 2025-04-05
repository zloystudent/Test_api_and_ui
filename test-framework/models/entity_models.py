from pydantic import BaseModel
from typing import List


class Addition(BaseModel):
    additional_info: str
    additional_number: int


class AdditionExport(BaseModel):
    id: int
    additional_info: str
    additional_number: int


class EntityData(BaseModel):
    addition: Addition
    important_numbers: List[int]
    title: str
    verified: bool


class ExportData(BaseModel):
    id: int
    title: str
    verified: bool
    addition: AdditionExport
    important_numbers: List[int]


class EntityResponse(BaseModel):
    entity: List[ExportData]


class IdPerson(BaseModel):
    id: int
