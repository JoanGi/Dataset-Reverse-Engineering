from dataclasses import dataclass
from pickle import DICT

@dataclass(unsafe_hash=True)
class DatasetDescription:
    metadata =  {
        "Title": str,
        "Unique-Identifier": str,
        "Version": str,
        "Release Date": str,
        "Citation": str,
        "Description": {
            "Purposes": str,
            "Tasks": [str],
            "Gaps": str
        },
        "Licences": str,
        "Tags": [str],
        "Area": [str],
        "Uses": {
            "Past Uses": [str],
            "Recommended": [str],
            "Non-recommended": [str],
            "Uses repository": [str]
        },
        "Distribution": {
            "Is public": str,
            "Hos is distributed": str,
            "Distribution license": str,
        },
        "Authoring": {
            "Authors": [],
            "Funders": [],
            "Maintainers": [],
            "Erratum": str,
            "Data Retention": str,
            "Version lifecycle": str,
            "Contribution guidelines": str
        }
    }
    composition = {}
    provenance = {}
