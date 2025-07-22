"""
This script generate country pages for #ohmygrid website
"""
import os
import zipfile
import pandas as pd
from pathlib import Path
import requests

COUNTRY_PAGE_TEMPLATE = "country_page_template.md"
DOCS_FOLDER_PATH = "../../docs/"
PROGRESS_PAGE_PATH = "progress.md"
COUNTRY_LIST_PATH = "countrylist.md"


DESTINATION_DIRECTORY = Path(__file__).parent.parent.parent / "docs/countrypages"
MAPS_IMAGES_DIRECTORY = Path(__file__).parent.parent.parent / "docs/images/maps_countries"
print("Destination directory = ", DESTINATION_DIRECTORY)

def main():
    df_wikidata = pd.read_csv("wikidata_countries_info_formatted.csv", na_filter=False).set_index("codeiso2")
    # wikidata_dict = {row["codeiso2"]: row for row in df_wikidata.to_dict(orient='records')}
    print(df_wikidata.columns)
    print(df_wikidata)

    df_openinframap = pd.read_csv("openinframap_countries_info_brut.csv", na_filter=False).set_index("codeiso2")
    # openinframap_dict = {row["codeiso2"]: row for row in df.to_dict(orient='records')}
    print(df_openinframap.columns)

    df_powergrid = pd.read_csv("powergrid_analysis_countries_info.csv", na_filter=False).set_index("codeiso2")
    # powergrid_dict = {row["codeiso2"]: row for row in df.to_dict(orient='records')}
    print(df_powergrid.columns)

    """ Following lines extract the country list per continent. You can use one of the following dict as a country list"""
    extract_dict = {idx: df_wikidata.loc[idx].get("name")
                    for idx in df_wikidata.index if df_wikidata.loc[idx].get("continent") == "Oceania"}
    print(extract_dict)

    extract_dict = {idx: df_wikidata.loc[idx].get("name")
                    for idx in df_wikidata.index if df_wikidata.loc[idx].get("continent") == "North America"}
    print(extract_dict)

    extract_dict = {idx: df_wikidata.loc[idx].get("name")
                    for idx in df_wikidata.index if df_wikidata.loc[idx].get("continent") == "Europe"}
    print(extract_dict)


    Africa = {'AO': 'Angola', 'BF': 'Burkina Faso', 'BI': 'Burundi', 'BJ': 'Benin', 'BW': 'Botswana',
              'CD': 'Democratic Republic of the Congo', 'CF': 'Central African Republic', 'CG': 'Republic of the Congo',
              'CI': 'Ivory Coast', 'CM': 'Cameroon', 'CV': 'Cape Verde', 'DJ': 'Djibouti', 'DZ': 'Algeria',
              'EG': 'Egypt', 'ER': 'Eritrea', 'ET': 'Ethiopia', 'GA': 'Gabon', 'GH': 'Ghana', 'GM': 'The Gambia',
              'GN': 'Guinea', 'GQ': 'Equatorial Guinea', 'GW': 'Guinea-Bissau', 'KE': 'Kenya', 'KM': 'Comoros',
              'LR': 'Liberia', 'LS': 'Lesotho', 'LY': 'Libya', 'MA': 'Morocco', 'MG': 'Madagascar', 'ML': 'Mali',
              'MR': 'Mauritania', 'MU': 'Mauritius', 'MW': 'Malawi', 'MZ': 'Mozambique', 'NA': 'Namibia', 'NE': 'Niger',
              'NG': 'Nigeria', 'RW': 'Rwanda', 'SC': 'Seychelles', 'SD': 'Sudan', 'SL': 'Sierra Leone', 'SN': 'Senegal',
              'SO': 'Somalia', 'SS': 'South Sudan', 'ST': 'São Tomé and Príncipe', 'SZ': 'Eswatini', 'TD': 'Chad',
              'TG': 'Togo', 'TN': 'Tunisia', 'TZ': 'Tanzania', 'UG': 'Uganda', 'ZA': 'South Africa', 'ZM': 'Zambia',
              'ZW': 'Zimbabwe'}
    ## SouthAmerica = {'AR': 'Argentina', 'BO': 'Bolivia', 'BR': 'Brazil', 'CL': 'Chile', 'CO': 'Colombia', 'EC': 'Ecuador', 'GY': 'Guyana', 'PA': 'Panama', 'PE': 'Peru', 'PY': 'Paraguay', 'SR': 'Suriname', 'UY': 'Uruguay', 'VE': 'Venezuela'}
    SouthAmerica_light = {'AR': 'Argentina', 'BO': 'Bolivia', 'CL': 'Chile', 'CO': 'Colombia', 'EC': 'Ecuador',
                          'GY': 'Guyana', 'PA': 'Panama', 'PE': 'Peru', 'PY': 'Paraguay', 'SR': 'Suriname',
                          'UY': 'Uruguay', 'VE': 'Venezuela'}
    ## Asia = {'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AM': 'Armenia', 'AZ': 'Azerbaijan', 'BD': 'Bangladesh', 'BH': 'Bahrain', 'BN': 'Brunei', 'BT': 'Bhutan', 'CN': "People's Republic of China", 'ID': 'Indonesia', 'IL': 'Israel', 'IN': 'India', 'IQ': 'Iraq', 'IR': 'Iran', 'JO': 'Jordan', 'JP': 'Japan', 'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KP': 'North Korea', 'KR': 'South Korea', 'KW': 'Kuwait', 'KZ': 'Kazakhstan', 'LA': 'Laos', 'LB': 'Lebanon', 'LK': 'Sri Lanka', 'MM': 'Myanmar', 'MN': 'Mongolia', 'MV': 'Maldives', 'MY': 'Malaysia', 'NP': 'Nepal', 'OM': 'Oman', 'PH': 'Philippines', 'PK': 'Pakistan', 'PS': 'State of Palestine', 'QA': 'Qatar', 'SA': 'Saudi Arabia', 'SG': 'Singapore', 'SY': 'Syria', 'TH': 'Thailand', 'TJ': 'Tajikistan', 'TL': 'Timor-Leste', 'TM': 'Turkmenistan', 'TR': 'Turkey', 'TW': 'Taiwan', 'UZ': 'Uzbekistan', 'VN': 'Vietnam', 'YE': 'Yemen'}
    Asia_light = {'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AM': 'Armenia', 'AZ': 'Azerbaijan',
                  'BD': 'Bangladesh', 'BH': 'Bahrain', 'BN': 'Brunei', 'BT': 'Bhutan', 'ID': 'Indonesia',
                  'IL': 'Israel', 'IQ': 'Iraq', 'IR': 'Iran', 'JO': 'Jordan', 'JP': 'Japan', 'KG': 'Kyrgyzstan',
                  'KH': 'Cambodia', 'KP': 'North Korea', 'KR': 'South Korea', 'KW': 'Kuwait', 'KZ': 'Kazakhstan',
                  'LA': 'Laos', 'LB': 'Lebanon', 'LK': 'Sri Lanka', 'MM': 'Myanmar', 'MN': 'Mongolia', 'MV': 'Maldives',
                  'MY': 'Malaysia', 'NP': 'Nepal', 'OM': 'Oman', 'PH': 'Philippines', 'PK': 'Pakistan',
                  'PS': 'State of Palestine', 'QA': 'Qatar', 'SA': 'Saudi Arabia', 'SG': 'Singapore', 'SY': 'Syria',
                  'TH': 'Thailand', 'TJ': 'Tajikistan', 'TL': 'Timor-Leste', 'TM': 'Turkmenistan', 'TR': 'Turkey',
                  'TW': 'Taiwan', 'UZ': 'Uzbekistan', 'VN': 'Vietnam', 'YE': 'Yemen'}
    ## NorthAmerica {'AG': 'Antigua and Barbuda', 'BB': 'Barbados', 'BS': 'The Bahamas', 'BZ': 'Belize', 'CA': 'Canada', 'CR': 'Costa Rica', 'CU': 'Cuba', 'DM': 'Dominica', 'DO': 'Dominican Republic', 'GD': 'Grenada', 'GT': 'Guatemala', 'HN': 'Honduras', 'HT': 'Haiti', 'JM': 'Jamaica', 'KN': 'Saint Kitts and Nevis', 'LC': 'Saint Lucia', 'MX': 'Mexico', 'NI': 'Nicaragua', 'SV': 'El Salvador', 'TT': 'Trinidad and Tobago', 'US': 'United States', 'VC': 'Saint Vincent and the Grenadines'}
    ## Oceania = {'AU': 'Australia', 'FJ': 'Fiji', 'FM': 'Federated States of Micronesia', 'KI': 'Kiribati', 'MH': 'Marshall Islands', 'NR': 'Nauru', 'NZ': 'New Zealand', 'PG': 'Papua New Guinea', 'PW': 'Palau', 'SB': 'Solomon Islands', 'TO': 'Tonga', 'TV': 'Tuvalu', 'VU': 'Vanuatu', 'WS': 'Samoa'}

    # No Brazil, China and India in light dict
    # COUNTRY_LIST = { **Africa, **SouthAmerica_light, **Asia_light }
    # COUNTRY_LIST = {'DK': 'Danish'}
    COUNTRY_LIST = {idx: df_wikidata.loc[idx].get("name") for idx in df_wikidata.index}
    SKIP_UNTIL = None  # not in use yet
    exit(0)
    # The following section are conditional, only for countries with map
    SECTION_PROGRESS_MAP = """
        ## Progress map

        <center>
        <img src="https://raw.githubusercontent.com/ben10dynartio/ohmygrid-website-files/refs/heads/main/docs/images/maps_countries/{{COUNTRY_CODE}}/high-voltage-network.jpg" width="60%">
        <img src="../../images/maps_countries_legend_progress.jpg" width="50%">
        </center>
        """.replace("        ", "")

    SECTION_GRID_CONNECTIVITY = """
        ## Grid connectivity overview

        Grid connectivity summary (nb of substations x nb of connections) :<br>{{POWER_GRID_CONNECTIVITY}}

        <center>
        <img src="https://raw.githubusercontent.com/ben10dynartio/ohmygrid-website-files/refs/heads/main/docs/images/maps_countries/{{COUNTRY_CODE}}/grid-connectivity.jpg" width="60%">
        <img src="../../images/maps_countries_legend_grid.jpg" width="50%">
        </center>
        """.replace("        ", "")

    ## Building MD file &

    df_collector = []  # To collect each country informations
    for country_key in COUNTRY_LIST:
        template_data = {}
        template_data["COUNTRY_CODE"] = country_key

        template_data["COUNTRY_NAME"] = df_wikidata.loc[country_key]["countryLabel"]
        template_data["COUNTRY_CONTINENT"] = df_wikidata.loc[country_key]["continent"]
        template_data["COUNTRY_POPULATION"] = df_wikidata.loc[country_key]["population"]
        template_data["COUNTRY_AREA"] = df_wikidata.loc[country_key]["area_km2"]
        template_data["COUNTRY_GDP"] = df_wikidata.loc[country_key]["gdp_bd"]
        template_data["COUNTRY_OSM_REL_ID"] = df_wikidata.loc[country_key]["osm_rel_id"]
        template_data["COUNTRY_WIKIDATA_ID"] = df_wikidata.loc[country_key]["osm_rel_id"]
        template_data["COUNTRY_FLAG_IMAGE"] = df_wikidata.loc[country_key]["flag_image_url"]
        template_data["COUNTRY_MAP_IMAGE"] = df_wikidata.loc[country_key]["locator_map_url"]

        template_data["POWER_LINES_KM"] = df_openinframap.loc[country_key]["power_line_total_length"]
        template_data["POWER_PLANTS_MW"] = df_openinframap.loc[country_key]["power_plant_output_mw"]
        template_data["POWER_PLANTS_NB"] = int(df_openinframap.loc[country_key]["power_plant_count"])

        template_data["POWER_SUBSTATIONS_NB"] = ''
        template_data["POWER_INTERCONNECTIONS_NB"] = ''
        template_data["POWER_GRID_CONNECTIVITY"] = ''
        if df_powergrid.loc[country_key].get("nb_substations"):
            template_data["POWER_SUBSTATIONS_NB"] = int(float(df_powergrid.loc[country_key]["nb_substations"]))
            template_data["POWER_INTERCONNECTIONS_NB"] = int(
                float(df_powergrid.loc[country_key]["nb_international_connections"]))
            template_data["POWER_GRID_CONNECTIVITY"] = df_powergrid.loc[country_key]["grid_connectivity"]

        template_data["SECTION_GRID_CONNECTIVITY"] = ""
        template_data["SECTION_PROGRESS_MAP"] = ""
        if Path(MAPS_IMAGES_DIRECTORY / f"{country_key}/high-voltage-network.jpg").is_file():
            template_data["SECTION_GRID_CONNECTIVITY"] = SECTION_GRID_CONNECTIVITY
            template_data["SECTION_PROGRESS_MAP"] = SECTION_PROGRESS_MAP

        # Open COUNTRY_PAGE_TEMPLATE and replace "{{ }}" string with corresponding value
        # It is done twice to manage SECTION_* values that are designed above
        with open(COUNTRY_PAGE_TEMPLATE, 'r', encoding='utf-8') as f:
            contenu = f.read()
            for key, val in template_data.items():
                contenu = contenu.replace(f'{{{{{key}}}}}', str(val))
            for key, val in template_data.items():
                contenu = contenu.replace(f'{{{{{key}}}}}', str(val))

        # Export all md files for countries
        Path.mkdir(DESTINATION_DIRECTORY, exist_ok=True)
        with open(DESTINATION_DIRECTORY / f"{template_data['COUNTRY_NAME']}.md", 'w', encoding='utf-8') as f:
            f.write(contenu)

        df_collector.append(template_data)

    # Construct the string for the list of country (to be insterted on "progress.md" pages)
    df_collector = pd.DataFrame(df_collector)
    lst_continent = df_collector['COUNTRY_CONTINENT'].unique().tolist()
    lst_continent.sort()
    mystr = ""
    for continent in lst_continent:
        # print("###", continent, "\n")
        mystr += "###" + continent + "\n"
        dft = df_collector[df_collector['COUNTRY_CONTINENT'] == continent]
        for r in dft.to_dict(orient='records'):
            # Country name link to the page, with a small flag on the left
            mystr += (f"![Flag {r['COUNTRY_NAME']}]({r['COUNTRY_FLAG_IMAGE']}){{width=20px}} "
                      f"[{r['COUNTRY_NAME']}](countrypages/{r['COUNTRY_NAME']}.md) - \n")
            # print(mystr, end="")
        mystr += "\n"
        # print("\n")

    r = requests.get(
        'https://raw.githubusercontent.com/open-energy-transition/Oh-my-Grid/refs/heads/main/docs/progress.md')
    newfile = r.text.replace("<!-- COUNTRY_LIST_INSERTION -->", mystr)
    with open(PROGRESS_PAGE_PATH, 'w') as f:
        f.write(newfile)

    with open(COUNTRY_LIST_PATH, 'w') as f:
        f.write(mystr)

    zip_folder(DESTINATION_DIRECTORY)
    zip_folder(MAPS_IMAGES_DIRECTORY)


def zip_folder(folder_path, output_path=None):
    if not os.path.isdir(folder_path):
        raise ValueError(f"Le dossier spécifié n'existe pas : {folder_path}")

    if output_path is None:
        output_path = Path(__file__).parent.parent.parent / ("zips/" + folder_path.name + ".zip")

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = "docs/" + os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, arcname=rel_path)

    print(f"Dossier zippé avec succès : {output_path}")


# Exemple d'utilisation
if __name__ == "__main__":
    main()
