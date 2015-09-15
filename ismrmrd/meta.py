import xml.etree.ElementTree as ET
from io import StringIO

class Meta(dict):
    """A wrapper around a `dict` that allows for serialization and
    deserialization to and from XML, respectively. It serves as a Python
    representation of the ISMRMRD Meta attributes"""

    def serialize(self):
        """Converts a Meta instance into a "valid" ISMRMRD Meta XML string"""
        root = ET.Element('ismrmrdMeta')
        tree = ET.ElementTree(root)
        for k, v in self.items():
            child = ET.SubElement(root, 'meta')
            name = ET.SubElement(child, 'name')
            name.text = k
            if type(v) == list:
                for item in v:
                    value = ET.SubElement(child, 'value')
                    value.text = str(item)
            else:
                value = ET.SubElement(child, 'value')
                value.text = str(v)
        # this is a 'workaround' to get ElementTree to generate the XML declaration
        output = StringIO.StringIO()
        tree.write(output, encoding="UTF-8", xml_declaration=True)
        return output.getvalue()

    @staticmethod
    def deserialize(xml):
        """Creates a Meta instance from an ISMRMRD Meta XML string"""
        root = ET.fromstring(xml)
        assert root.tag == 'ismrmrdMeta'

        meta = Meta()

        for child in root.findall('meta'):
            name = child.find('name')
            assert name is not None
            values = child.findall('value')
            assert values is not None

            # only make the Meta value a list if necessary
            if len(values) == 1:
                value = values[0].text
            else:
                value = [v.text for v in values]

            key = name.text
            existing = meta.get(key, None)
            # make the current Meta value a list if necessary then either extend
            # it with the new list value, or append the new value to it
            if existing is not None:
                if type(existing) != list:
                    meta[key] = [meta[key]]
                if type(value) == list:
                    meta[key].extend(value)
                else:
                    meta[key].append(value)
            else:
                meta[key] = value

        return meta
