from pydantic import BaseModel

class Gene(BaseModel):
    species_name: str
    dna_sequence: str
    description: str
