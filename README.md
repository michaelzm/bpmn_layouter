# BPMN Layouter

## Overview
BPMN Layouter is a Python-based tool that processes BPMN XML files, converts them into structured JSON, and appends position data to the elements.

## Features
- Converts BPMN XML to structured JSON
- Flattens JSON into a dictionary for easy manipulation
- Builds a tree structure of BPMN elements
- Computes and assigns element positions
- Writes back positional data to XML

## Installation
Ensure you have Python installed. Then, clone the repository and install the required dependencies:

```sh
# Clone the repository
git clone https://github.com/michaelzm/bpmn_layouter.git
cd bpmn_layouter

# Install dependencies
pip install -r requirements.txt
```

## Usage
### Running the Code
To process a BPMN XML file and generate a positioned file, use the following script:

```python
from bpmn_to_json_parser import bpmn_to_json, json_to_flattened_dict
from xml_string import xml_file
from data_structures import Tree, Node
from data_structure_methods import parse_tree, find_preceeding_element_position, init_element_positions
from placement_config import lookup_placement
from xml_position_appender import xml_position_appender

# Convert BPMN XML to structured JSON
flattened_json = bpmn_to_json(xml_data=xml_file)
flattened_dict = json_to_flattened_dict(flattened_json)

# Initialize elements
elements_not_in_tree = {}
for element_id in flattened_dict:
    elements_not_in_tree[element_id] = Node(flattened_dict[element_id])

# Parse tree and compute positions
elements_not_in_tree = parse_tree(elements_not_in_tree=elements_not_in_tree)
elements_not_in_tree = init_element_positions(lookup_placement, elements_not_in_tree)

# Append position data back to XML
xml_position_appender(elements_not_in_tree, xml_file, "positioned_file.xml")
```

### Input
- **BPMN XML File:** This should be stored in `xml_string.py` as `xml_file`.

### Output
- **positioned_file.xml**: The processed XML file with added positional data.

## Contributing
Feel free to fork the repository and submit pull requests!

## License
This project is licensed under the Apache 2.0 License.

## Contact
For any questions, reach out via GitHub issues. 

---
Happy coding! 🚀