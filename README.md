# BPMN Layouter

## Overview
BPMN Layouter is a Python-based tool that processes BPMN data in JSON format, structures it, computes positional data for elements, and writes it back to a BPMN XML file.

## Features
- Parses BPMN data from JSON format
- Generates incoming and outgoing flow connections for elements
- Converts structured BPMN JSON into a flattened dictionary
- Builds a tree representation of BPMN elements
- Computes and assigns positional data to elements
- Appends positional data to BPMN XML

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
To process BPMN JSON data and generate a BPMN XML file with positional data, use the following approach:

```python
import json
from xml_generator import json_to_flattened_dict, generate_flows_based_on_elements, xml_position_appender, generate_top_bpmn_xml
from data_structure_methods import parse_tree, init_element_positions, init_shift_and_depth, get_longest_path_from_start, assign_depth_and_shift
from data_structures import Node

# Load JSON data
parsed_json_input = json.loads(json_data)

# Initialize flow connections
for elem in parsed_json_input["elements"]:
    elem["outgoing_flows"] = []
    elem["incoming_flows"] = []

# Generate flow mappings
parsed_json = generate_flows_based_on_elements(parsed_json_input)

# Convert structured JSON to a flattened dictionary
flattened_dict = json_to_flattened_dict(parsed_json)

# Convert elements to nodes
elements_as_nodes = {element_id: Node(flattened_dict[element_id]) for element_id in flattened_dict}

# Parse the BPMN tree structure
elements_linked = parse_tree(elements_linked=elements_as_nodes)

# Initialize shift and depth\init_shift_and_depth(elements_linked)

# Alternative layouter option
# base_path = get_longest_path_from_start(elements_linked)
# base_path_id = [i.id for i in base_path]
# assign_depth_and_shift(elements_as_nodes, base_path_id)

# Initialize element positions
elements_linked, id_depth_mapping = init_element_positions(elements_as_nodes)

# Generate XML with positional data
top_xml_part = generate_top_bpmn_xml(elements_linked)
xml_position_appender(elements_linked, top_xml_part, "file1version_same_working_orig")
```

### Input
- **BPMN JSON Data:** The input data should be a valid JSON structure containing BPMN elements.

### Output
- **file1version_same_working_orig.xml**: The BPMN XML file generated with computed positional data.

## Contributing
Feel free to fork the repository and submit pull requests!

## License
This project is licensed under the Apache 2.0 License.

## Contact
For any questions, reach out via GitHub issues.

---
### Modeled Layout:
<img width="1023" alt="Screenshot 2025-02-19 at 17 17 22" src="https://github.com/user-attachments/assets/24159112-0192-4dc8-9b67-db6d5d816785" />

### Autogenerated Layout based on semantic BPMN part:
<img width="1008" alt="Screenshot 2025-02-19 at 17 17 16" src="https://github.com/user-attachments/assets/fd2a68dd-91f7-4b0e-a9da-af89d81874d9" />

