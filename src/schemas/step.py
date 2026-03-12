from typing import List

from pydantic import BaseModel


class Step(BaseModel):
    description: str


class PlannedTask(BaseModel):
    steps: List[Step]
