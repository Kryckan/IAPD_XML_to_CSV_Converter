# IAPD XML to CSV Converter

This script is designed to convert XML files containing Investment Adviser Public Disclosure (IAPD) data into a CSV format. The XML files follow a specific structure as described in the attached document.

## Features

- Converts multiple XML files in a specified folder to a single CSV file.
- Extracts relevant data from the XML files, including individual information, current employments, exams, designations, previous registrations, employment history, other business, and disclosure reporting pages (DRPs).
- Handles missing or incomplete data gracefully.
- Provides a progress bar to track the processing of XML files.
- Automatically modifies the output CSV filename if it already exists to avoid overwriting.

## Requirements

- Python 3.x
- `tqdm` library for progress bar functionality

## Installation

1. Clone the repository or download the script file.
2. Install the required dependencies by running the following command:
   ```
   pip install tqdm
   ```
## Usage

1. Place the XML files you want to convert in a folder ('xml' as default).
2. Update the `xml_folder` (if you set another name than default) variable in the script to specify the path to your XML folder.
3. Update the `csv_file` variable in the script to specify the desired name of the output CSV file.
4. Run the script using the command: `python main.py`.
5. The script will process each XML file in the specified folder and generate a CSV file with the extracted data.
6. If the specified CSV file already exists, the script will automatically modify the filename by appending a number to avoid overwriting.

## XML Structure

The XML files processed by this script should follow the structure described in the attached document. The script expects the following elements and attributes:

- `IAPDIndividualReport`: The root element of the XML file.
- `Indvls/Indvl`: Represents an individual record.
- `Info`: Contains attributes with individual information.
- `CrntEmps/CrntEmp`: Represents current employments.
- `Exms/Exm`: Represents exams taken by the individual.
- `Dsgntns/Dsgntn`: Represents designations held by the individual.
- `PrevRgstns/PrevRgstn`: Represents previous registrations of the individual.
- `EmpHists/EmpHist`: Represents employment history of the individual.
- `OthrBuss/OthrBus`: Represents other business engagements of the individual.
- `DRPs/DRP`: Represents disclosure reporting pages for the individual.

## Error Handling

The script includes error handling to gracefully handle parsing errors or other exceptions that may occur during the processing of XML files. If an error occurs, an error message will be printed to the console, indicating the specific XML file and the details of the error.

## Output

The script generates a CSV file with the extracted data from the XML files. The CSV file will have the following columns:

- Columns corresponding to the attributes of the `Info` element.
- `CrntEmps`: Current employments concatenated with a pipe separator (|).
- `Exms`: Exam codes concatenated with a pipe separator (|).
- `Dsgntns`: Designations concatenated with a pipe separator (|).
- `PrevRgstns`: Previous registrations concatenated with a pipe separator (|).
- `EmpHists`: Employment history concatenated with a pipe separator (|).
- `OthrBuss`: Other business engagements concatenated with a pipe separator (|).
- `DRPs`: Disclosure reporting page indicators concatenated with a pipe separator (|).

Note: If any of the above elements are missing or empty in an XML file, the corresponding column in the CSV file will have an empty value.

## Customization

To customize the script to work with other XML files that have a different structure, you'll need to modify the `xml_to_csv` function according to the specific XML schema of the new files. Here are the key areas you'll need to focus on:

1. Extracting headers:
   - Adjust the XPath expressions in the code that extracts the headers from the first individual record.
   - Update the `headers.extend` block to include the desired column names based on the new XML structure.

2. Extracting data rows:
   - Modify the XPath expressions in the code that iterates over individual records and extracts data for each row.
   - Update the code blocks that extract specific data elements (e.g., current employments, exams, designations) to match the new XML structure.
   - Use the appropriate XPath expressions to locate and extract the desired data from the XML elements and attributes.

3. Handling missing or optional elements:
   - Review the code that handles missing or optional elements and adjust it based on the new XML schema.
   - Ensure that default values or empty strings are assigned appropriately when elements are not present.

4. Customizing column names and order:
   - Modify the `headers.extend` block to include the desired column names in the order you want them to appear in the CSV file.
   - Ensure that the order of data extraction in the `xml_to_csv` function matches the order of the headers.

5. Error handling:
   - Review the error handling code and adjust it if needed to handle any specific errors or exceptions that may occur with the new XML files.

Here's an example of how you can modify the `xml_to_csv` function to work with a different XML structure:

```python
def xml_to_csv(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract headers from the first record
    headers = []
    first_record = root.find("Records/Record")
    if first_record is not None:
        headers = list(first_record.attrib.keys())
        headers.extend(["Field1", "Field2", "Field3"])

    # Initialize an empty list to store the data rows
    data_rows = []

    # Iterate over records and extract data
    for record in root.findall("Records/Record"):
        row = []
        row.extend(list(record.attrib.values()))

        # Extract specific fields
        field1 = record.find("Field1").text if record.find("Field1") is not None else ""
        field2 = record.find("Field2").text if record.find("Field2") is not None else ""
        field3 = record.find("Field3").text if record.find("Field3") is not None else ""

        row.extend([field1, field2, field3])
        data_rows.append(row)

    return headers, data_rows
```

In this example, the code assumes a different XML structure where the records are located under a "Records" element, and each record has attributes and specific fields like "Field1", "Field2", and "Field3". Adjust the XPath expressions and data extraction code according to your specific XML schema.

Remember to thoroughly test the modified script with the new XML files to ensure that the data is extracted correctly and the resulting CSV file has the desired structure and content.

## License

This script is released under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Acknowledgements

- The script utilizes the `xml.etree.ElementTree` module for parsing XML files.
- The `tqdm` library is used for displaying progress bars.

