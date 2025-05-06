import os
from algorithms.huffman import decode_file
from models.Incident import Incident, IncidentType, Department
import random


def convert_time(p : int):
    carry = 0
    minutes = p % 100
    if minutes >= 60:
        carry = 1
        minutes -= 60
    hours = p // 100 + carry
    if hours >= 24:
        print("Entered time exceeds 24 hours")
        raise Exception
    return (hours * 100) + minutes

def checkForIncident(time: int):
    try:
        time = convert_time(time)
    except:
        return []

    logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
    bin_path = os.path.join(logs_dir, f"{time}.bin")
    if not os.path.exists(bin_path):
        return []
    chance = random.randint(1,2)
    if chance == 1:
        return []

    description = decode_file(time)
    address = extract_address(description)
    services = analyze_incident(description)
    severity = getSeverity(description)

    type_map = {
        "fire": IncidentType.HOUSE_FIRE,
        "smoke": IncidentType.SMOKE,
        "gas leak": IncidentType.GAS_LEAK,
        "explosion": IncidentType.EXPLOSION,
        "drowning": IncidentType.DROWNING,
        "overdose": IncidentType.OVERDOSE,
        "heart attack": IncidentType.HEART_ATTACK,
        "breathing": IncidentType.BREATHING_ISSUE,
        "unconscious": IncidentType.UNCONSCIOUS,
        "injury": IncidentType.INJURY,
        "injuries": IncidentType.INJURY,
        "collision": IncidentType.COLLISION,
        "accident": IncidentType.ACCIDENT,
        "robbery": IncidentType.ROBBERY,
        "theft": IncidentType.THEFT,
        "break-in": IncidentType.BREAK_IN,
        "assault": IncidentType.ASSAULT,
        "bomb threat": IncidentType.BOMB_THREAT
    }
    incident_type = IncidentType.NONE
    for keyword, type_val in type_map.items():
        if rabin_karp_search(desc_lower, keyword):
            incident_type = type_val
            break

    if "fire" in services:
        department = Department.FIRE
    elif "ambulance" in services:
        department = Department.MEDICAL
    elif "police" in services:
        department = Department.POLICE
    else:
        department = Department.NONE

    all_keywords = list(getSeverity.__annotations__['return'].__args__[0].__args__)
    keyword_hits = {}
    desc_lower = description.lower()
    return Incident(
        incidentType=incident_type,
        department=department,
        location=address,
        locationName = "Residence",
        time=time,
        resourceNeed=len(services),
        timeNeed=severity * 5,
        description=description,
    )
    

def analyze_incident(description: str):
    KEYWORDS_TO_SERVICES = {
        "fire": {"fire"},
        "smoke": {"fire"},
        "gas leak": {"fire"},
        "explosion": {"fire"},
        "drowning": {"ambulance"},
        "overdose": {"ambulance"},
        "heart attack": {"ambulance"},
        "breathing": {"ambulance"},
        "unconscious": {"ambulance"},
        "injury": {"ambulance"},
        "injuries": {"ambulance"},
        "collision": {"ambulance"},
        "accident": {"ambulance"},
        "robbery": {"police"},
        "theft": {"police"},
        "break-in": {"police"},
        "assault": {"police"},
        "bomb threat": {"police"}
    }

    services_needed = set()
    description_l = description.lower()
    for keyword, services in KEYWORDS_TO_SERVICES.items():
        if len(description_l) >= len(keyword):
            if rabin_karp_search(description_l, keyword):
                services_needed.update(services)
    return services_needed

def rabin_karp_search(desc, keyw, q=101):
    d = 256
    m = len(keyw)
    n = len(desc)
    h = pow(d, m-1, q)
    p_hash = 0
    t_hash = 0
    positions = []

    for i in range(m):
        p_hash = (d * p_hash + ord(keyw[i])) % q
        t_hash = (d * t_hash + ord(desc[i])) % q
    
    for i in range(n - m + 1):
        if p_hash == t_hash:
            if desc[i:i+m] == keyw:
                positions.append(i)
        
        if i < n - m:
            t_hash = (d * (t_hash - ord(desc[i]) * h) + ord(desc[i + m])) % q
            if t_hash < 0:
                t_hash += q
    return positions

def extract_address(description: str):
    pos_list = rabin_karp_search(description, 'Address: ')
    if not pos_list:
        return "Unknown Address"
    
    start_pos = pos_list[0] + len('Address: ')
    end_pos = description.find('\n', start_pos)
    if end_pos == -1:
        end_pos = len(description)
    
    return description[start_pos:end_pos].strip()


#Knuth Morris Pratt
def computer_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0 #Length of previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += i
    return lps

def Knuth_morris_pratt(text, pattern):
    n, m = len(text), len(pattern)
    lps = computer_lps(pattern)
    i = j = 0
    positions = []

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j) #match found
            j = lps[j - 1] #Continue searching
        elif i < n and pattern[j] != text[i]:
            j = lps[j - 1] if j != 0 else 0
            if j == 0:
                i += 1
    return positions

def getSeverity(desc):
    KEYWORDS_TO_SEVERITY = {
        "fire": {2},
        "smoke": {1},
        "gas leak": {1},
        "explosion": {3},
        "drowning": {1},
        "overdose": {2},
        "heart attack": {1},
        "breathing": {1},
        "unconscious": {1},
        "injury": {1},
        "injuries": {2},
        "collision": {2},
        "accident": {1},
        "robbery": {3},
        "theft": {2},
        "break-in": {1},
        "assault": {1},
        "bomb threat": {3}
    }
    totalseverity = 0
    description_l = desc.lower()
    for keyword, severity in KEYWORDS_TO_SEVERITY.items():
        if len(description_l) >= len(keyword):
            if Knuth_morris_pratt(description_l, keyword):
                totalseverity += severity
    return totalseverity