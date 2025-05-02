"""
HOW TO USE:
from algorithms.analyzeIncident import response

use response(time) with time being 3-4 digit length int

({emergency service} , 'address') = response(time)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ <- This is what you retrieve with this file
"""
from algorithms.huffman import decode_file

def convert_time(p : int):
    carry = 0
    minutes = p % 100
    if minutes >= 60:
        carry = 1
        minutes -= 60
    hours = p // 100 + carry
    if hours >= 25:
        print("Entered time exceeds 25 hours")
        raise Exception
    return (hours * 100) + minutes

def checkForIncident(time):
    return False #To change, only returns false atm

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

def response(time : int):
    desc = decode_file(time)
    return analyze_incident(desc), extract_address(desc)

#print(response(129)) - test