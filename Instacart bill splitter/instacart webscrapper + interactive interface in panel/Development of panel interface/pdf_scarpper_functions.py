import pdfplumber
import re
import pandas as pd

#Reads a pdf reciept and returns a DataFrame of items.
def read_pdf(infile):    
    #intializing features
    reg_expressions = {} #mandatory features of items
    # reg_expressions['item_cost'] = r'\)\n\ (.*?) \n'
    reg_expressions['item_cost'] = r'\n\$\d+\.\d+\n'#r'\n$\d+\.\d+\n'
    reg_expressions['item_cost_description'] = r'\d+ x \$\d+\.\d+'
    reg_expressions['item_name'] = r'^[A-Z,\s,a-z].*'

    optional_reg_expressions = {} #optional fratures of items
    optional_reg_expressions['item_quantity'] = r'\((.*?)\)'
    for dicts in [reg_expressions, optional_reg_expressions]:
        for key, value in dicts.items():
            dicts[key] = re.compile(value)

    Items = {}
    all_keys = list(reg_expressions.keys()) + list(optional_reg_expressions.keys())
    for key in all_keys:
            Items[key] = []

            
    # reading the pdf        
    with pdfplumber.open(infile) as pdf:
    # iterate over each page
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables[1:]:
                for [string] in table:    
                    status = [0]*len(reg_expressions.keys())
                    new_item = {}
                    for ind, (key, value) in enumerate(reg_expressions.items()):
                            match = value.findall(string)
                            if match:
                                status[ind] = 1
                                new_item[key] = re.sub(r'\n','', match[0])
                                # print(key, new_item[key])
                    if sum(status) == len(reg_expressions.keys()): #have successfully identified the item line
                        for ind, (key, value) in enumerate(optional_reg_expressions.items()):
                            match = value.findall(string)
                            if match:
                                new_item[key] = re.sub(r'\n','', match[0])
                                # print(key, new_item[key])
                            else:
                                new_item[key] = ''
                        for key in all_keys:
                            Items[key].append(new_item[key])

    Items = pd.DataFrame(Items)
    Items = Items[['item_cost_description', 'item_quantity', 'item_name', 'item_cost']]
    Items['item_cost'] = Items['item_cost'].map(lambda x:float(x.replace('$','')))
    return Items
    