# functions.py
import requests, zipfile, io
import xml.etree.ElementTree as ET

URL = "https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip"

def _local(tag: str) -> str:
    return tag.split('}', 1)[-1]  

def _open_xml_stream():
    """Stáhne ZIP a vrátí stream na první XML soubor."""
    resp = requests.get(URL, stream=True, timeout=60)
    resp.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    xml_name = next(n for n in zf.namelist() if n.lower().endswith(".xml"))
    return zf.open(xml_name)  

    
def number_of_products() -> int:
    """Stream spočítá počet /root/items/item (stejné jako len(root.findall("./items/item")))."""
    count = 0
    path = []
    in_root_items = False
    root_seen = False

    with _open_xml_stream() as xf:
        for event, elem in ET.iterparse(xf, events=("start", "end")):
            tag = _local(elem.tag)

            if event == "start":
                path.append(tag)

                if not root_seen:
                    root_seen = True


                elif tag == "items" and len(path) == 2:
                    in_root_items = True

            else:  
                if tag == "item" and in_root_items and len(path) == 3:
                    count += 1

                if tag == "items" and in_root_items and len(path) == 2:
                    in_root_items = False

                path.pop()
                elem.clear()
    return count



def name_of_products(limit: int | None = 100) -> str:
    """
    Vrátí text s názvy produktů z ./items/item (omezeno limitem řádků).
    Stream verze ekvivalentní root.findall("./items/item").
    """
    lines: list[str] = []

    path: list[str] = []
    in_root_items = False
    root_seen = False
    idx = 0  

    with _open_xml_stream() as xf:
        for event, elem in ET.iterparse(xf, events=("start", "end")):
            tag = _local(elem.tag)

            if event == "start":
                path.append(tag)

                if not root_seen:
                    root_seen = True

                elif tag == "items" and len(path) == 2:
                    in_root_items = True

            else:  
                if tag == "item" and in_root_items and len(path) == 3:
                    if limit is not None and len(lines) >= limit:
                        lines.append("... (zkráceno)\n")
                        path.pop()
                        elem.clear()
                        break

                    idx += 1
                    name = elem.attrib.get("name", "")
                    lines.append(f"{idx}. {name}\n")

                if tag == "items" and in_root_items and len(path) == 2:
                    in_root_items = False

                path.pop()
                elem.clear()

    return "".join(lines)


def name_of_parts(limit: int | None = None) -> str:
    """
    Vrátí text s díly z ./categoriesWithParts//category/item (omezeno limitem).
    Stream verze ekvivalentní root.findall("./categoriesWithParts//category/item").
    """
    lines: list[str] = []
    path: list[str] = []
    in_cwp = False
    idx = 0

    with _open_xml_stream() as xf:
        for event, elem in ET.iterparse(xf, events=("start", "end")):
            tag = _local(elem.tag)

            if event == "start":
                path.append(tag)

                if tag == "categoriesWithParts":
                    in_cwp = True

            else:  
                if tag == "categoriesWithParts":
                    in_cwp = False

                if (
                    in_cwp
                    and tag == "item"
                    and len(path) >= 2
                    and path[-2] == "category"
                ):
                    idx += 1

                    if limit is not None and idx > limit:
                        lines.append("... (zkráceno)\n")
                        path.pop()
                        elem.clear()
                        break

                    code = elem.attrib.get("code")
                    name = elem.attrib.get("name")
                    lines.append(f"{idx}. Code: {code}, Name: {name}\n")

                if path:
                    path.pop()
                elem.clear()

    return "".join(lines)

