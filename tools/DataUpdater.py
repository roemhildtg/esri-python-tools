#-------------------------------------------------------------------------------
# Name:        Data_Updater
# Purpose:      See tool metadata
#
# Author:      groemhildt
#
# Created:     17/03/2016
# Copyright:   (c) groemhildt 2016
#-------------------------------------------------------------------------------
from arcpy import Parameter, AddError
from arcpy.da import UpdateCursor
try:
    from arcpy.mp import ArcGISProject
except ImportError as e:
    AddError('This script requires ArcGIS Pro: {}'.format(e))


def update_layer(layer, field, value, new_value):
    if(field and value):
        where_clause = '{} = \'{}\''.format(field, value)
    else:
        where_clause = None
    try:
        cursor = UpdateCursor(layer, field, where_clause)
    except(TypeError):
        return "Error loading table {}".format(layer)

    try:
        for row in cursor:
            row[0] = new_value
            cursor.updateRow(row);
    except(RuntimeError):
        del cursor
        return "Error modifying table {}".format(layer)

    return 'Layer Updated: {}'.format(layer)

def get_layer_names(map='Map'):
    doc = ArcGISProject('current')
    m = doc.listMaps(map)[0]

    return [layer.name for layer in map.listLayers() if layer.visible and layer.isFeatureLayer]

def main():
    layers = get_layer_names()
    for layer in layers:
        print(update_layer(layer, 'Plan_ID', '1415', '1415TownSquareLn'))

if __name__ == '__main__':
    main()

class MultipleLayerUpdater(object):
    def __init__(self):
        self.label = 'Multiple Layer Updater'
        self.description = """
            Updates a field in multiple layers in the current map document with a value.
            If the field is not visible or is not a feature layer it will be skipped.
        """
        self.canRunInBackground = False

    def getParameterInfo(self):
        return [Parameter(
            displayName='Map',
            name='map',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        ),Parameter(
            displayName='Field',
            name='field',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        ), Parameter(
            displayName='Old Value',
            name='old_value',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        ), Parameter(
            displayName='New Value',
            name='new_value',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        )]

    def execute(self, parameters, messages):
        layers= get_layer_names(parameters[0].valueAsText)
        for layer in layers:
            messages.addMessage(
            update_layer(layer, parameters[1].valueAsText, parameters[2].valueAsText,parameters[3].valueAsText))
