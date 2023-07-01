import panel as pn
import numpy as np
import pandas as pd
from html_parinsing_function import *


pn.extension('katex')
template = pn.template.BootstrapTemplate(title='Split thy bills!')

Input = {}
w0 = 220
Input['people'] = pn.widgets.TextInput(value='Ananth,Shubha,Tanmay', name='people', width=w0)
Input['upload'] = pn.widgets.Button(name='Upload!', width=w0)
#input html receipt to parse, accept only html files
Input['file_input'] = pn.widgets.FileInput( accept='.html', name='HTML receipt', width=w0)

inputs = ['people', 'file_input', 'upload']
for item in inputs:
    template.sidebar.append(Input[f'{item}'])
template.main.append(pn.Column()) #for the delivery string
template.main.append(pn.Column()) #for the items and charges
template.main.append(pn.Column()) #for the split charges
template.sidebar.append(pn.Column()) #for comments/errors

#Parse the html receipt and return a dataframe with the receipt information and populate the panel template
def upload(*events, template=template, Input=Input):
    template.main[0].clear()
    column = pn.Column()
    #obtain the people involved in the transaction
    People = Input['people'].value.split(',')
    People.append('ALL')
    file_name = Input['file_input'].filename
    html_path = fr'{file_name}'
    delivered_items_df, misc_charges_df, delivery_string =  parse_html_receipt(html_path)#DataFrame containing the items
    template.main[0].append(pn.pane.Markdown(delivery_string))
    # item_features = ['item-name', 'item-price', 'item-image']
    # check_boxes = []
    selection_widget = {}
    m = 15
    align = 'center'
    #adding details of delivered item to the main template
    for index, item in delivered_items_df.iterrows():
        item_name = item['item-name']
        item_cost = item['item-price']
        item_image = item['item-image']
        item_index_pane = pn.pane.LaTeX(object=f'{index})', name='item_pane', width=5,margin=(m,m),align=align)
        item_name_pane = pn.pane.Markdown(object=f'{item_name}', name='item_pane', width=400,margin=(m,m),align=align)
        item_cost_pane = pn.pane.LaTeX(object=f'$\${item_cost}$', name='item_pane', width=50,margin=(m,m),align=align)
        selection_widget[index] = pn.widgets.CheckButtonGroup(name='', value=[], options=People,margin=(m,m),align=align)
        h = item_cost_pane.height
        item_image_pane = pn.pane.Image(item_image, fixed_aspect=True, height=h)    
        #append everyhting to the main template
        column.append(pn.Column(pn.Row(item_index_pane, item_image_pane, item_name_pane, item_cost_pane, selection_widget[index]),pn.layout.Divider()))
        print(item_name, item_cost)
        # template.main.append(pn.Row(item_index_pane, item_name_pane, item_cost_pane, selection_widget[index]))


    #adding details of miscellaneous charges to the main template
    for index, item in misc_charges_df.iterrows():
        item_name = item['charge-type']
        item_cost = item['amount']
        item_index_pane = pn.pane.LaTeX(object=f'{index})', name='item_pane', width=5,margin=(m,m),align=align)
        # item_image_pane = pn.pane.PNG(item_image, sizing_mode='scale_width')    
        item_name_pane = pn.pane.Markdown(object=f'{item_name}', name='item_pane', width=400,margin=(m,m),align=align)
        item_cost_pane = pn.pane.LaTeX(object=f'$\${item_cost}$', name='item_pane', width=50,margin=(m,m),align=align)
        column.append(pn.Column(pn.Row(item_index_pane, item_name_pane, item_cost_pane), pn.layout.Divider()))
        print(item_name, item_cost)
    
    template.main[0].append(column)
    
    return

#run the split function when the split button is pressed
Input['upload'].param.watch(upload, 'value')

#Split the bills after the selections have been made
# def split_bills(*events, template=template, Input=Input):




template.servable()