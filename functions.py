import requests
import zipfile
import io
import xml.etree.ElementTree as ET

def download_zip():
    url = "https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip"
    
    response = requests.get(url)

    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            xml_filename = zip_file.namelist()[0]
            with zip_file.open(xml_filename) as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()
    else:
        print("Error while downloading ZIP:", response.status_code)
    return root

def number_of_products(root):
    item_count = len(root.findall("./items/item"))
    return item_count

def name_of_products(root):
    out_lines = []
    for i, item in enumerate(root.findall("./items/item[@name]"), start=1):
        name = item.get('name')
        out_lines.append(f"{i}. {name} \n")
        #print(f"{i}. Name: {name}")
    return "".join(out_lines) + "\n"
    
def name_of_parts(root):
    out_lines = []
    for i, item in enumerate(root.findall("./categoriesWithParts//category/item"), start=1):
        name = item.get("name")
        code = item.get("code")
        out_lines.append(f"{i}. Code: {code}, Name: {name}\n")
        #print(f"{i}. Code: {code}, Name: {name}")
    return "".join(out_lines) + "\n"
