# Name: svg_shaper_utility_to_glowforge.py
# Version: 0.1
# Description: This python script takes a .svg file created by the Fusion 360
#   Shaper Origin Utilities and modifies the exterior and interior paths
#   fill/stroke/strok-color as well as the Inkscape user preferences. The paths
#   are grouped appropriately. All .svg files in current working directory are 
#   manipulated; original file is overwritten.
# Use: Run in working directory with all .svg files you want to manipulate. 
#  User inputs can be edited on lines 11 through 21.

# Define user inputs, these must be strings in svg file readable format
exterior_fill_color = 'none'
exterior_stroke_color = 'rgb(0,0,0)'
exterior_stroke_width = '0.005in'

interior_fill_color = 'none'
interior_stroke_color = 'rgb(255,0,0)'
interior_stroke_width = '0.005in'

# User defined Inkscape preferences. I don't know what all these do so they are just copied from a .svg file save in Inkscape. If you do not have any you can replace this with False
inkscape_preferences = '<sodipodi:namedview pagecolor="#ffffff" bordercolor="#666666" borderopacity="1" objecttolerance="10" gridtolerance="10" guidetolerance="10" inkscape:pageopacity="0" showgrid="false" inkscape:window-maximized="1" units="in" inkscape:document-units="in" />'

# Import Libraries
import os
import svgpathtools

# Get a list of all the .svg files in current working directory
cwd = os.getcwd()
svg_file_list = []
for file in os.listdir(cwd):
    if file.endswith(".svg"):
        svg_file_list.append(file)

# Parse .svg file then update colors and groups
for svg_file in svg_file_list:
    path_list, path_attribute_list, svg_file_attributes = svgpathtools.svg2paths2(svg_file) 
    
    # Create two lists used to group paths when writing .svg file
    exterior_group_list = []
    interior_group_list = []
    
    # Loop through each path and edit attributes
    for path_dic in path_attribute_list:
        # Update exterior paths attributes and add them to list exterior_group
        if path_dic["shaper:pathType"] == "exterior":
            path_dic["fill"] = exterior_fill_color
            path_dic["stroke"] = exterior_stroke_color
            path_dic["stroke-width"] = exterior_stroke_width
            exterior_group_list.append(path_dic)
        # Update exterior paths attributes and add them to list interior_group
        elif path_dic["shaper:pathType"] == "interior":
            path_dic["fill"] = interior_fill_color
            path_dic["stroke"] = interior_stroke_color
            path_dic["stroke-width"] = interior_stroke_width
            interior_group_list.append(path_dic)

    # Write modified svg file
    output = open(svg_file, "w")
    # Write boiler plate information 
    output.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n')
    # Write svg file attribute data
    output.write('<svg' + '\n')
    for key in svg_file_attributes:
        output.write('\t' + key + '="' + svg_file_attributes[key] + '"\n')
    output.write('\t' + '>' + '\n')
    # Write inkscape preferences if they exist
    if inkscape_preferences:
        output.write('\t'+ inkscape_preferences + '\n')
    # Write path data for exterior group
    output.write('\t' + '<g>' + '\n')
    for path_dic in exterior_group_list:
        output.write('\t\t' + '<path ')
        for path_key in path_dic:
            output.write(path_key + '="' + path_dic[path_key] + '" ')
        output.write('/>' + '\n')
    # Write path data for interior group
    output.write('\t\t' + '<g>' + '\n')
    for path_dic in interior_group_list:
        output.write('\t\t\t' + '<path ')
        for path_key in path_dic:
            output.write(path_key + '="' + path_dic[path_key] + '" ')
        output.write('/>' + '\n')
    # Close groups and file
    output.write('\t\t' + '</g>'+ '\n')
    output.write('\t' + '</g>'+ '\n')
    output.write('</svg>')
    output.close()
