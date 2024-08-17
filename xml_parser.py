import sys
import xml.etree.ElementTree as ET
import traceback

from parser_config import PART_NAME


def run_xml_parser(path_to_xml: str, option: int = 0):
    '''
    Function run_xml_parser process xml file and print data defined by option

    Input: option - (0 default print all, 1 - count of collected products, 2 - list of product names, 3 - list of replace part names)
    Output: print result or error message
    '''

    # range <0,4)
    if option in range(0, 4):

        input_vaild = False
        xml_tree = None

        if path_to_xml:
            try:
                xml_tree = ET.parse(path_to_xml)
            except Exception:
                print(f'Exception: {traceback.format_exc()}')
            else:
                input_vaild = True

        if input_vaild and xml_tree:
            product_cout = 0
            for item in xml_tree.find('items').findall('item'):

                if item:

                    product_name = item.get('name')

                    # count of collected product items
                    if (option == 0 or option == 1) and product_name:
                        product_cout += 1

                    # product names
                    if (option == 0 or option == 2) and product_name:
                        print(product_name)

                    # product replase part names
                    if (option == 0 or option == 3) and item.find('parts'):
                        for part_data in item.find('parts').findall('part'):
                            if part_data.get('name') == PART_NAME:
                                if option == 3:
                                    print(product_name)
                                for part_item in part_data.findall('item'):
                                    replace_part = part_item.get('name')
                                    if replace_part:
                                        print('\t{}'.format(replace_part))
            if option <= 1:
                print('Product cout: {}'.format(product_cout))

        else:
            print('Error_message: Invalid input data.')
    else:
        print('Error_message: Invalid option range.')


def main():
    args_count = len(sys.argv)
    if args_count < 3:
        print('Invalid number of arguments {}, expect 2: full file path to xml file, option int code'.format((args_count - 1)))
    elif args_count == 3:
        path_to_xml = sys.argv[1]
        option = int(sys.argv[2])
        run_xml_parser(option=option, path_to_xml=path_to_xml)
    else:
        print('Invalid number of arguments {}, expect 2: full file path to xml file, option int code'.format((args_count - 1)))


if __name__ == '__main__':
    main()
