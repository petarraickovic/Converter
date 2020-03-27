import xml.etree.ElementTree as ET


class ExtractData(object):
    """Class for extracting currency rates  defined with src_currency and dest_currency from file defined with fileName"""

    def extract_rates(self,currency, filePart):
        if(currency != 'EUR'):
            try:
                data = next(curr for curr in filePart if(curr.attrib.get('currency') == currency))
            except StopIteration:
                return None
            rate = data.attrib.get('rate')
        else:
            rate = 1
        return rate


    def process_file(self,fileName,src_currency, dest_currency, reference_date):
        tree = ET.parse(fileName)
        root = tree.getroot()
        desiredFilePart = next(child for child in root if('Cube' in child.tag))
        try:
            desiredTime = next(child1 for child1 in desiredFilePart if(child1.attrib.get('time') == reference_date))
        except StopIteration:
            return None
        src_rate = ExtractData().extract_rates(src_currency, desiredTime)
        dest_rate = ExtractData().extract_rates(dest_currency, desiredTime)
        return src_rate, dest_rate

