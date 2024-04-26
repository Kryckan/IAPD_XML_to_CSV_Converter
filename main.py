import os
import csv
import xml.etree.ElementTree as ET
from tqdm import tqdm

version = "1.0.0"


# Function to convert XML file to CSV format
def xml_to_csv(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract headers from the first individual record
    headers = []
    first_indvl = root.find("Indvls/Indvl")
    if first_indvl is not None:
        info = first_indvl.find("Info")
        if info is not None:
            headers = list(info.attrib.keys())
        else:
            headers = []
        headers.extend(
            [
                "CrntEmps",
                "Exms",
                "Dsgntns",
                "PrevRgstns",
                "EmpHists",
                "OthrBuss",
                "DRPs",
            ]
        )

    # Initialize an empty list to store the data rows
    data_rows = []

    # Iterate over individual records and extract data
    for indvl in root.findall("Indvls/Indvl"):
        row = []
        info = indvl.find("Info")
        if info is not None:
            row.extend(list(info.attrib.values()))
        else:
            row.extend([""] * len(headers))

        # Extract current employments
        crnt_emps = "|".join(
            [emp.attrib.get("orgNm", "") for emp in indvl.findall("CrntEmps/CrntEmp")]
        )
        row.append(crnt_emps)

        # Extract exams
        exms = "|".join(
            [exm.attrib.get("exmCd", "") for exm in indvl.findall("Exms/Exm")]
        )
        row.append(exms)

        # Extract designations
        dsgntns = "|".join(
            [
                dsgntn.attrib.get("dsgntnNm", "")
                for dsgntn in indvl.findall("Dsgntns/Dsgntn")
            ]
        )
        row.append(dsgntns)

        # Extract previous registrations
        prev_rgstns = "|".join(
            [
                rgstn.attrib.get("orgNm", "")
                for rgstn in indvl.findall("PrevRgstns/PrevRgstn")
            ]
        )
        row.append(prev_rgstns)

        # Extract employment history
        emp_hists = "|".join(
            [hist.attrib.get("orgNm", "") for hist in indvl.findall("EmpHists/EmpHist")]
        )
        row.append(emp_hists)

        # Extract other business
        othr_buss = "|".join(
            [bus.attrib.get("desc", "") for bus in indvl.findall("OthrBuss/OthrBus")]
        )
        row.append(othr_buss)

        # Extract DRPs
        drps = "|".join(
            [drp.attrib.get("hasRegAction", "") for drp in indvl.findall("DRPs/DRP")]
        )
        row.append(drps)

        data_rows.append(row)

    return headers, data_rows


# Function to process XML files and generate CSV file
def process_xml_files(xml_folder, csv_file):
    # Check if the CSV file already exists and modify the filename by appending a new number
    counter = 1
    original_csv_file = csv_file
    while os.path.exists(csv_file):
        base_name = os.path.splitext(original_csv_file)[0]
        csv_file = f"{base_name}_{counter:02d}.csv"
        counter += 1

    # Get a list of XML files in the specified folder
    xml_files = [file for file in os.listdir(xml_folder) if file.endswith(".xml")]

    # Open the CSV file in write mode
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Process each XML file with a tqdm progress bar
        for i, xml_file in enumerate(tqdm(xml_files, desc="Processing XML files")):
            xml_path = os.path.join(xml_folder, xml_file)

            try:
                headers, data_rows = xml_to_csv(xml_path)

                # Write headers to the CSV file only for the first XML file
                if i == 0:
                    writer.writerow(headers)

                # Write data rows to the CSV file
                writer.writerows(data_rows)

            except ET.ParseError:
                print(f"Error parsing XML file: {xml_file}")
            except Exception as e:
                print(f"Error processing XML file: {xml_file}")
                print(f"Error details: {str(e)}")

    print(f"CSV file '{csv_file}' created successfully.")


# Example usage
xml_folder = "xml"
csv_file = "output.csv"
process_xml_files(xml_folder, csv_file)
