from dataclasses import dataclass, field

@dataclass
class Survey:
    survey_key: str
    dataset_name: str
    description: str
    year: int
    variable_key: str
    lookup_key: str
    exclude: list
    variable_ends_with: str = None
    labels: dict = field(default_factory=dict)
    rows: list = field(default_factory=list)
