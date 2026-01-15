#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:33:54 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import matplotlib
import numpy
import os
import pathlib
import seaborn
import pandas


class Colorful:
    # if snsColorPalette and matplotlibColorMap are None and colorNumber < 21 use distinctColorlist

    def get_indy_color_list(colorNumber=None,
                            colorList=None,
                            shuffling=False,
                            blindness_level=4,
                            use_white=False,
                            use_black=True,
                            use_beige=False,
                            use_lavender=False,
                            use_grey=False,
                            snsColorPalette=None,
                            matplotlibColorMap=None,  # e.g. matplotlib.pyplot.cm.gist_ncar
                            matplotlibLimiter=0.95
                            ):

        if colorList is not None:
            colorList = colorList

        nmax = 22 - int(not use_white) - int(not use_black) - int(not use_beige) - int(not use_lavender) - int(not use_grey)

        if snsColorPalette is None and matplotlibColorMap is None and colorNumber < nmax:
            colorList = Colorful.getDistinctColorList(colorNumber, blindness_level=blindness_level,
                                                      use_white=use_white, use_black=use_black,
                                                      use_beige=use_beige, use_lavender=use_lavender,
                                                      use_grey=use_grey)
        elif snsColorPalette is None and matplotlibColorMap is None and colorNumber > nmax:
            colorList = seaborn.color_palette(snsColorPalette, colorNumber)
        elif snsColorPalette is not None:
            colorList = seaborn.color_palette(snsColorPalette, colorNumber)
        elif matplotlibColorMap is not None:
            colorList = [matplotlibColorMap(i) for i in numpy.linspace(0, matplotlibLimiter, colorNumber)]

        if shuffling:
            colorList = numpy.random.shuffle(colorList)

        for ind, value in enumerate(colorList):
            colorList[ind] = matplotlib.colors.to_hex(value)

        return colorList

    def get_scientific_colormap(cmap_name,
                                scm_base_dir=os.environ["SCRIPT"] + "/" + "ScientificColourMaps5/",
                                reverse=False):

        cmap_file = pathlib.Path(scm_base_dir) / cmap_name / (cmap_name + '.txt')

        cmap_data = numpy.loadtxt(cmap_file)

        if reverse:
            cmap_data = numpy.flip(cmap_data)

        return matplotlib.colors.LinearSegmentedColormap.from_list(cmap_name, cmap_data)

    def get_distinct_colors_df():

        folder = pathlib.Path(__file__).parent
        return pandas.read_csv(folder / "colormap.csv", index_col=0)

    def get_distinct_color_list_by_name(elements):
        distinct_colors_df = Colorful.get_distinct_colors_df()
        if isinstance(elements, str):
            elements = elements.lower()
            color_list = distinct_colors_df.loc[elements, "color"]
        elif isinstance(elements, list):
            elements = [ele.lower() for ele in elements]
            color_list = list(distinct_colors_df.loc[elements, "color"].values)
        else:
            raise Exception("elements should be either str or list")

        return color_list

    def get_distinct_color_list_by_number(elements: int,
                                          blindness_level=1,
                                          order_by_convenient=True,
                                          use_black=True,
                                          use_white=False,
                                          use_lavender=False,
                                          use_beige=False,
                                          use_grey=False,
                                          ):

        distinct_colors_df = Colorful.get_distinct_colors_df()

        distinct_colors_df["name"] = distinct_colors_df.index
        blindness_level_sql = f"blindness_level_{blindness_level}==True"

        if order_by_convenient:
            order_by_convenient_sql = "convenient"
        else:
            order_by_convenient_sql = "rainbow"

        use_color = {"black": use_black,
                     "white": use_white,
                     "lavender": use_lavender,
                     "beige": use_beige,
                     "grey": use_grey}

        use_color_sql_dict = {}
        for color in use_color:
            if use_color[color]:
                use_color_sql_dict[color] = ""
            else:
                use_color_sql_dict[color] = f"is_{color}==False"
        use_color_sql = " AND ".join(list(filter(len, list(use_color_sql_dict.values()))))

        if len(use_color_sql) > 0:
            use_color_sql = f" and {use_color_sql}"

        query_str = f"{blindness_level_sql}{use_color_sql}"
        color_df = (distinct_colors_df
                    .query(query_str)
                    .sort_values(by=order_by_convenient_sql))
        color_list_all_possible = list(color_df["color"].values)

        # if the number of colors needed is larger than within the blindness_level, use recursion and decrease blindness_level
        if elements > len(color_list_all_possible) and (blindness_level > 1):
            return Colorful.getDistinctColorList(elements,
                                                 blindness_level - 1,
                                                 use_black=use_black,
                                                 use_white=use_white,
                                                 use_lavender=use_lavender,
                                                 use_beige=use_beige,
                                                 use_grey=use_grey)

        # if the number of colors needed is larger than possible colors and blindness_level can't be decreased, return False value
        elif elements > len(color_list_all_possible) and (blindness_level == 1):
            raise Exception("list of colors not possible to generate with the given number")
        else:
            color_list = color_list_all_possible[:elements]  # give list of distinctColors with given number, blindness_level and choice of using white & black

        return color_list
