from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pickle import DICT
import json


class DatasetDescription:
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    metadata =  {
        "Title": str,
        "Unique-Identifier": str,
        "Version": str,
        "Release Date": int,
        "Update Date": int,
        "Published Date": int,
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
            "Is public": bool,
            "How is distributed": str,
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
    composition = {
        "Rationale": str,
        "Total Size": str,
        "Instances": 
            {
                "Instance Name": str,
                "Description": str,
                "Type": str,
                "Attribute number": int,
                "Size": int,
                "Attributes": [
                    {
                        "Attribute Name": str,
                        "Description": str,
                        "Labelling Process": str,
                        "Count": int,
                        "ofType": str, 
                        "Statistics": [{

                        }],
                    }
                ],
                "Statistics": [{

                }],
                "Consistency rules:":[{

                }]
            }
    }
    provenance = {
        "Curation Rationale": str,
        "Gathering Processes": [
            {
            "ProcessName": str,
            "Description": str,
            "Type": str,
            "Sources": [
                {
                    "Source Name": str,
                    "Description": str,
                    "Noise": str,
                }
            ],
            "Related Instaces": str,
            "Social Issues": str,
            "When data was collectes":str,
            "Process Demographics": str,
            "Gather Requeriments": [str] 
            }
        ],
        "Labeling Processes": [
            {
                "ProcessName": str,
                "Description": str,
                "Type": str,
                "Labels": [str],
                "Labeling Team": [{
                    "Description": str,
                    "Type": str,
                    "Demographics": [str],
                }],
                "Labeling Requeriments": [str]
            }
        ],
        "Preprocesses": [
            {
                "ProcessName": str,
                "Description": str,
            }
        ]
    }
    socialConcerns = {
        "Rationale": str,
        "Social Issues": [
            {
                "Issue Name": str,
                "Type": str,
                "Related Attributes": [str],
                "Description": str
            }
        ]
    }
