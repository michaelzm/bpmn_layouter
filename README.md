# BPMN Layouter

## Overview
BPMN Layouter is a Python-based tool that processes BPMN data from text files, structures it, computes positional data for elements, and generates BPMN XML files with updated layout information. This procts utilizes the Sugiyama (Dot) Layout algorithm.

## Features
- Parses BPMN data from text files, extracting and cleaning JSON content
- Generates incoming and outgoing flow connections for BPMN elements
- Computes positional shifts and depths for elements
- Initializes and assigns positional data to BPMN elements
- Generates BPMN XML files with embedded positional data

## Installation
Ensure Python is installed, then clone the repository and install dependencies:

```sh
git clone https://github.com/michaelzm/bpmn_layouter.git
cd bpmn_layouter
pip install -r requirements.txt
```

## Usage
### Running the Code
To process and generate BPMN XML files from your data, follow these steps:

```python
import re
import ast
import json
from xml_generator import generate_flows_based_on_elements, xml_position_appender, generate_top_bpmn_xml
from data_structure_methods import init_element_positions, assign_shift_and_depth

parsed_jsons = []

def clean_line(line):
    line = re.sub(r"ObjectId\('.*?'\)", '"ObjectId"', line)
    line = re.sub(r"datetime\.datetime\([^\)]+\)", '"datetime"', line)
    return line

with open("out_public.txt", "r") as file:
    for line in file:
        try:
            cleaned_line = clean_line(line)
            line_dict = ast.literal_eval(cleaned_line)
            content_raw = line_dict.get('content')
            if content_raw:
                content_dict = ast.literal_eval(content_raw)
                parsed_jsons.append(content_dict)
        except Exception as e:
            print(f"Failed to parse line: {e}")

for process_i, json_process in enumerate(parsed_jsons):
    print("Processing entry", process_i)
    json_data = json.dumps(json_process, indent=4)
    parsed_json_input = json.loads(json_data)

    for elem in parsed_json_input["elements"]:
        elem["outgoing_flows"] = []
        elem["incoming_flows"] = []

    parsed_json = generate_flows_based_on_elements(parsed_json_input)
    elements_as_data_struc = assign_shift_and_depth(parsed_json)

    elem_pos = init_element_positions(elements_as_data_struc)

    top_xml_part = generate_top_bpmn_xml(elem_pos)
    xml_position_appender(elem_pos, top_xml_part, f"json_process_v12_{process_i}")
```

### Input
- **out_public.txt:** Text file containing raw JSON data with nested BPMN content.

### Output
- **json_process_v12_[index].xml**: BPMN XML files generated with computed positional data for each processed entry.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License
This project is licensed under the Apache 2.0 License.

## Contact
For questions, please open an issue on GitHub.

---

### Example Layouts:

#### Autogenerated Layout based on semantic BPMN:
![Screenshot 2025-03-23 at 15 40 01](https://github.com/user-attachments/assets/4829219d-442a-4de6-b467-883c4223955d)



