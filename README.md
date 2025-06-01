# Serve map files for #ohmygrid website

## Information

Country map images are produced by : https://github.com/ben10dynartio/osm-power-grid-map-analysis

The repository works with a docs folder at the root. This folder is not synchronized with the repository (added in .gitignore) : it is not versionned file and this added as a zip file on releases.

Structure of `docs` repository :
```
docs
|-- countrypages
|   |-- Afghanistan.md
|   |-- ...
|   |-- Zimbabwe.md
|-- images
    |-- maps_countries
        |-- AE
        |   |-- grid-connectivity.png
        |   |-- high-voltage-network.png
        |-- ...
        |-- ZW
            |-- grid-connectivity.png
            |-- high-voltage-network.png
```

Each new realease contains a `docs.zip` which is a docs folder that have to be merged the docs folder of the website before mkdocs build.

`country_page_generation.py` script takes data from `openinframap_countries_info_brut.csv`, `powergrid_analysis_countries_info.csv`, `wikidata_countries_info_formatted.csv` files, and builds corresponding `[country].md` files in `countrypages` folder. Finally, it takes `docs` folder and zip it for associating to new release.

## Technical notes

URL to get latest release metadata : https://api.github.com/repos/ben10dynartio/ohmygrid-website-files/releases/latest

See https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8 to get the file `docs.zip`.

