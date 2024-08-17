import pytest
from xml_parser import run_xml_parser

TEST_XML_FILE = 'test_sample.xml'

def test_count_products(capsys):
    run_xml_parser(path_to_xml=TEST_XML_FILE, option=1)
    captured = capsys.readouterr()
    _, count = captured.out.strip().split(':')
    assert int(count) == 2

def test_list_products(capsys):
    run_xml_parser(path_to_xml=TEST_XML_FILE, option=2)
    captured = capsys.readouterr()
    product_list = captured.out.split('\n')
    for index, product in enumerate(product_list):
        if product:
            assert product.strip() == 'Item_name_{}'.format(index + 1)

def test_list_replace_parts(capsys):
    run_xml_parser(path_to_xml=TEST_XML_FILE, option=3)
    captured = capsys.readouterr()
    print(captured.out)
    product, replace_part, _ = captured.out.split('\n')
    assert product.strip() == 'Item_name_2'
    assert replace_part.strip() == 'Replace_parts_1'

def test_list_replace_parts(capsys):
    run_xml_parser(path_to_xml=TEST_XML_FILE, option=0)
    captured = capsys.readouterr()
    print(captured.out)
    product1, product2, replace_part, count_text, _ = captured.out.split('\n')
    _, count = count_text.strip().split(':')
    assert product1.strip() == 'Item_name_1'
    assert product2.strip() == 'Item_name_2'
    assert replace_part.strip() == 'Replace_parts_1'
    assert int(count) == 2
