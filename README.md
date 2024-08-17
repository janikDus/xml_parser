# xml_parser
Process xml file and print data defined by option

Run XML Parser:
- expect 2 parameters: full file path to xml file, option int code (from range: 0,1,2,3)

python xml_parser.py "path_to_xml_file" option

Run XML Parser Fast API (default running on http://127.0.0.1:8000):

uvicorn xml_parser_api:app --reload

Run tests:

pytest -q parser_test.py
