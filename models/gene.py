from pydantic import BaseModel

# --------------------------
# Gene Model
# --------------------------
class Gene(BaseModel):
    """
    Pydantic model representing a gene entry.

    Attributes:
        species_name (str): The name of the species.
        dna_sequence (str): The DNA sequence of the gene.
        description (str): A description of the gene.
    """
    species_name: str
    dna_sequence: str
    description: str