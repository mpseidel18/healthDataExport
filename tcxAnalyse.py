"""Some functions for parsing a TCX file (specifically, a TCX file
downloaded from Strava, which was generated based on data recorded by a
Garmin vívoactive 3) and creating a Pandas DataFrame with the data.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Any, Union, Tuple

import lxml.etree
import pandas as pd
import dateutil.parser as dp
from pandas.io.pytables import format_doc #Mehrere Imports für pandas, parser etc.
# pd.set_option('display.max_rows', None)

NAMESPACES = {
    'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2', #Verschiedene Namespaces, um nach diesen Namen im .tcx File zu suchen
    'ns2': 'http://www.garmin.com/xmlschemas/UserProfile/v2',
    'ns3': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2',
    'ns4': 'http://www.garmin.com/xmlschemas/ProfileExtension/v1',
    'ns5': 'http://www.garmin.com/xmlschemas/ActivityGoals/v1'
}


POINTS_COLUMN_NAMES = ['latitude', 'longitude', 'elevation', 'time', 'heart_rate', 'cadence', 'speed', 'lap'] # Namen der Spalten für den Points Dataframe
LAPS_COLUMN_NAMES = ['number', 'start_time', 'distance', 'total_time', 'max_speed', 'max_hr', 'avg_hr'] # Namen der Spalten für den Laps Dataframe

def get_tcx_lap_data(lap: lxml.etree._Element) -> Dict[str, Union[float, datetime, timedelta, int]]: #Neue funktion, um aus einem XML Element die Runden herauszulesen. Hier wird ein 
                                                                                                     #ein Dictionary zurückgegeben
    data: Dict[str, Union[float, datetime, timedelta, int]] = {} #Neues Dict, die Einträge werden den typen entsprechend konvertiert
    
    start_time_str = lap.attrib['StartTime'] #Attribute von StartTime aus dem XML Tree ziehen
    data['start_time'] = dp.parse(start_time_str) #start_time_str
    
    distance_elem = lap.find('ns:DistanceMeters', NAMESPACES) #Sucht nach ns:DistanceMeters im Tree
    if distance_elem is not None:
        data['distance'] = float(distance_elem.text) #Unter distance wird der Output aus dem find Befehl gesichert
    
    total_time_elem = lap.find('ns:TotalTimeSeconds', NAMESPACES) #Dies wiederholt sich für jeden Eintrag..
    if total_time_elem is not None:
        data['total_time'] = timedelta(seconds=float(total_time_elem.text))
    
    max_speed_elem = lap.find('ns:MaximumSpeed', NAMESPACES)
    if max_speed_elem is not None:
        data['max_speed'] = float(max_speed_elem.text)
    
    max_hr_elem = lap.find('ns:MaximumHeartRateBpm', NAMESPACES)
    if max_hr_elem is not None:
        data['max_hr'] = float(max_hr_elem.find('ns:Value', NAMESPACES).text)
    
    avg_hr_elem = lap.find('ns:AverageHeartRateBpm', NAMESPACES)
    if avg_hr_elem is not None:
        data['avg_hr'] = float(avg_hr_elem.find('ns:Value', NAMESPACES).text)
    
    return data

def get_tcx_point_data(point: lxml.etree._Element) -> Optional[Dict[str, Union[float, int, str, datetime]]]: #Da TCX Dateien neben Laps auch Points besitzen, wird dasselbe für Points gemacht 

    data: Dict[str, Union[float, int, str, datetime]] = {} #Neues Dict..
    
    position = point.find('ns:Position', NAMESPACES)
    if position is None:
        return None
    else:
        data['latitude'] = float(position.find('ns:LatitudeDegrees', NAMESPACES).text) #Sichern von Höhen-
        data['longitude'] = float(position.find('ns:LongitudeDegrees', NAMESPACES).text)#und Breitengrad
    time_str = point.find('ns:Time', NAMESPACES).text #Und weitere Daten..
    data['time'] = dp.parse(time_str)
        
    elevation_elem = point.find('ns:AltitudeMeters', NAMESPACES)
    if elevation_elem is not None:
        data['elevation'] = float(elevation_elem.text)
    
    hr_elem = point.find('ns:HeartRateBpm', NAMESPACES)
    if hr_elem is not None:
        data['heart_rate'] = int(hr_elem.find('ns:Value', NAMESPACES).text)
        
    cad_elem = point.find('ns:Cadence', NAMESPACES)
    if cad_elem is not None:
        data['cadence'] = int(cad_elem.text)
    
    # The ".//" here basically tells lxml to search recursively down the tree for the relevant tag, rather than just the
    # immediate child elements of speed_elem. See https://lxml.de/tutorial.html#elementpath
    speed_elem = point.find('.//ns3:Speed', NAMESPACES) #Rekursive suche nach dem Speed Element
    if speed_elem is not None:
        data['speed'] = float(speed_elem.text)
    
    return data
    

def get_dataframes(fname: str) -> Tuple[pd.DataFrame, pd.DataFrame]: #Erstelle aus einer TCS File einen pandas Dataframe
    
    tree = lxml.etree.parse(fname)
    root = tree.getroot()
    activity = root.find('ns:Activities', NAMESPACES)[0]  #Annahme: Es gibt nur eine Aktivität in dieser TCX File
    points_data = [] #Erstellen der Listen, welche an den Dataframe später angehängt werden
    laps_data = []
    lap_no = 1
    for lap in activity.findall('ns:Lap', NAMESPACES):  #Daten aus der Sektion "Laps" werden geholt..
        single_lap_data = get_tcx_lap_data(lap) #Aufrufend der voherigen Funktion
        single_lap_data['number'] = lap_no  #Sichern der Rundennummer, welche mit anderen daten in single_lap_data gesichert wurde
        laps_data.append(single_lap_data) #Anhängend er Daten an die laps_data Liste
        
        # Get data about the track points in the lap
        track = lap.find('ns:Track', NAMESPACES)  #Das gleiche gilt für die Sektion "Track"
        for point in track.findall('ns:Trackpoint', NAMESPACES): #Jeder Trackpoint beinhaltet verschiedene Daten, in diesem wird nach weiteren Daten gesucht
            single_point_data = get_tcx_point_data(point) #Die Daten werden mithilfe der voherigen Funktion geholt
            if single_point_data:
                single_point_data['lap'] = lap_no #Rundennummer wird gesichert
                points_data.append(single_point_data) #An points_data werden die gesammelten Daten angehängt
        lap_no += 1 #Diese Schritte werden für jede Runde wiederholt, also wird die Rundenummer hier gezählt
    
    laps_df = pd.DataFrame(laps_data, columns=LAPS_COLUMN_NAMES) #Gesammelte Daten werden in jeweils zwei Dataframes gesichert, hier in laps_df
    laps_df.set_index('number', inplace=True) #Index setzen
    points_df = pd.DataFrame(points_data, columns=POINTS_COLUMN_NAMES) #Hier in points_df
    
    return laps_df, points_df