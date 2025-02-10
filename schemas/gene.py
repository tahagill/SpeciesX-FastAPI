def geneEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "species_name": item['species_name'],
        "dna_sequence": item['dna_sequence'],
        "description": item['description'],
    }

def genesEntity(items) -> list:
    return [geneEntity(item) for item in items]
