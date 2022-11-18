TEAMS_URL = "https://lol.fandom.com/wiki/Special:CargoExport?tables=Teams%2C&&fields=Teams.Name%2C+Teams.Location%2C+Teams.Region%2C+Teams.Short%2C+Teams.IsDisbanded%2C&&order+by=%60cargo__Teams%60.%60Name%60%2C%60cargo__Teams%60.%60Location%60%2C%60cargo__Teams%60.%60Region%60%2C%60cargo__Teams%60.%60Short%60%2C%60cargo__Teams%60.%60IsDisbanded%60&limit={}&offset={}&format=json"
TEAMS_HEADERS = {
    "Name": "name",
    "Location": "location",
    "Region": "region",
    "Short": "short_name",
    "IsDisbanded": "is_disbanded"
}
