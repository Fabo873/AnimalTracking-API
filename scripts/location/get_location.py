import csv
from os import stat

states = set()
municipalities = set()
locations = set()
with open('./scripts/location/data.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:

        state_id = row['CVE_ENT']
        state_name = row['NOM_ENT']
        state_init = row['NOM_ABR']

        municipality_id = state_id + row['CVE_MUN']
        municipality_name = row['NOM_MUN']

        location_id = municipality_id + row['CVE_LOC']
        location_name = row['NOM_LOC']
        location_type = row['AMBITO']
        location_lat = row['LAT_DEC']
        location_lon = row['LON_DEC']
        location_alt = row['ALTITUD']

        states.add((state_id,state_name,state_init))
        municipalities.add((municipality_id,municipality_name,state_id))
        locations.add((location_id,location_name,location_type,location_lat,location_lon,location_alt,municipality_id))

    states_query = 'INSERT INTO REPORTS.States (id,`name`,initials) VALUES'
    for state in states:
        states_query += '\n\t({id},"{name}","{initial}"),'.format(
                                                                id=state[0],
                                                                name=state[1],
                                                                initial=state[2])
    states_query = states_query[:-1] + ';'

    municipalities_query = 'INSERT INTO REPORTS.Municipalities (id,`name`,state_id) VALUES'
    for municipality in municipalities:
        municipalities_query += '\n\t({id},"{name}",{state_id}),'.format(
                                                            id=municipality[0],
                                                            name=municipality[1],
                                                            state_id=municipality[2])
    municipalities_query = municipalities_query[:-1] + ';'

    locations_query = 'INSERT INTO REPORTS.Locations (id,`name`,`type`,lat,lon,altitude,municipality_id) VALUES'
    for location in locations:
        locations_query += '\n\t({id},"{name}","{type}",{lat},{lon},{altitude},{municipality_id}),'.format(
                                                                                        id=location[0],
                                                                                        name=location[1],
                                                                                        type=location[2],
                                                                                        lat=location[3],
                                                                                        lon=location[4],
                                                                                        altitude=location[5],
                                                                                        municipality_id=location[6])
    locations_query = locations_query[:-1] + ';'

    with open('./sql/insert_locations.sql','w', encoding='utf-8') as sql_file:
        sql_file.write(states_query + '\n\n')
        sql_file.write(municipalities_query + '\n\n')
        sql_file.write(locations_query + '\n')
