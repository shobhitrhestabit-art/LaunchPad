from dataclasses import dataclass  
from typing import Dict,Any


@dataclass
class IngestDocument :
    text : str
    source_type :str
    source_id :str
    metadata : Dict[str,Any]