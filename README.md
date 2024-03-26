# EDI 837 Parser
[![Python - 3.9.0+](https://img.shields.io/badge/Python-3.9.0%2B-orange)](https://www.python.org/downloads/release/python-390/)

This repository contains a Python parser designed to parse Electronic Data Interchange (EDI) 837 files.

## Overview

The EDI 837 parser is a tool developed to efficiently extract and interpret data from EDI 837 files. These files contain structured data related to healthcare claims, including patient information, procedures performed, and billing details. By parsing these files, users can easily extract relevant information for further processing or analysis.

## Features

- **Parsing**: The parser is capable of parsing EDI 837 files in accordance with the standard format, extracting essential data fields and segments.
- **Data Extraction**: It extracts key information such as patient details, provider information, service codes, drug identification etc.
- **Validation**: The parser performs basic validation checks to ensure that the parsed data conforms to the expected structure and standards.
- **Input Format**: The parser can accept data in .txt or .837 formats, or it can accept a list of files all at once.
- **Output Format**: Extracted data can be outputted in CSV format.
- **Customization**: Users can customize the parser according to specific requirements, adding support for additional segments or refining parsing logic.

## Getting Started

To use the EDI 837 parser, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine
2. **Usage**: First, open the _init_.py file located in the edi_837_parser directory. Then, within the main function, modify the following lines:
   ```python
    data = parse('~/Desktop/eobs').to_dataframe()
    data.to_csv('~/Desktop/transaction_sets.csv')
   ```
   Ensure that you replace '/Desktop/eobs' with the path to your input folder containing the EDI files, and '/Desktop/' with the path to your desired output folder.
3. **Customization**: If required, customize the parser to suit your specific use case by modifying the source code and adding or modifying parsing logic.

## Contributing
Contributions to the EDI 837 parser are welcome! If you encounter any issues, have feature requests, or would like to contribute enhancements, please feel free to open an issue or submit a pull request.

**Special Thanks**  
I would like to express my deepest gratitude to [keironstoddart](https://github.com/keironstoddart/edi-835-parser/tree/main) for their invaluable contributions and inspiration that served as the foundation for this project.
