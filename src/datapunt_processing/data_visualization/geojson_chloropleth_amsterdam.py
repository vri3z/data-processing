import re

import folium
import pandas as pd
import requests


def create_map(df: pd.DataFrame, geotype: str, output_name: str, save: bool = False):
    """
    Input:
        - df, contains at least:
            - id (with the code of stadsdeel, gebied, buurtcombinatie or buurt)
            - value
        - geotype (string):
            - stadsdeel
            - gebied
            - buurtcombinatie
            - buurt
        - output_name (string): how do you want te file to be saved
    Ouput: html with data on map

    """
    if geotype not in ('buurtcombinatie', 'gebied', 'buurt', 'stadsdeel'):
        print(
            "geotype wordt niet ondersteund."
            "Kies een vande volgende opties: "
            "{buurtcombinatie', 'gebied', 'buurt' of 'stadsdeel'}"
        )
        return

    if bool(re.search(r"\W", output_name)):
        print("ongeldige outputnaam, " 
              "outputnaam mag alleen letters, cijfers of _ bevatten")
        return

    df.rename({c: c.lower().strip() for c in df.columns}, inplace=True)
    if "id" not in df.columns or "value" not in df.columns:
        print("dataframe moet 'ID' en 'Value' bevatten")
        return

    base = 'http://maps.amsterdam.nl/open_geodata/geojson.php?KAARTLAAG='
    api_urls = {
        'buurt': base + 'GEBIED_BUURTEN&THEMA=gebiedsindeling',
        'buurtcombinatie': base + 'GEBIED_BUURTCOMBINATIES&THEMA=gebiedsindeling',
        'gebied': base + 'GEBIEDEN22&THEMA=gebiedsindeling',
        'stadsdeel': base + 'GEBIED_STADSDELEN&THEMA=gebiedsindeling'
    }
    geo_json_data = requests.get(api_urls[geotype]).json()

    # set colormap
    linear = folium.LinearColormap(
        ['#E5F2FC', '#B1D9F5', '#71BDEE', '#00a0e6', '#004699']
    )
    colormap = linear.scale(df['value'].min(), df['value'].max())

    # convert df to dict
    df_dict = df.set_index('id')['value'].to_dict()

    # make map
    m = folium.Map(
        location=[52.379189, 4.899431],
        tiles='https://{s}.data.amsterdam.nl/topo_google/{z}/{x}/{y}.png',
        attr='Amsterdam',
        zoom_start=12,
        min_lat=52.269470,
        max_lat=52.4322,
        min_lon=4.72876,
        max_lon=5.07916,
        subdomains=['t1', 't2', 't3', 't4']
    )

    # plot data on map
    folium.GeoJson(
        geo_json_data,
        style_function=lambda feature: {
            'fillColor':
                colormap(df_dict[feature['properties']['Gebied_code']])
                if feature['properties']['Gebied_code'] in df_dict else False,
            'color':
                'white' if feature['properties']['Gebied_code'] in df_dict else False,
            'weight': 1.2,
            # 'dashArray': '2, 3',
            'fillOpacity': 0.6 if feature['properties']['Gebied_code'] in df_dict else 0
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['Gebied_code', 'Gebied', 'Opp_m2'],
            localize=True
        )
    ).add_to(m)

    # add scale to map
    colormap.caption = 'Color scale'
    colormap.add_to(m)

    # save map
    if save:
        m.save(f'{output_name}.html')

    return m
