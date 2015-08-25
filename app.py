import subprocess
import bottle

def parse_coord(c):
    c = c.replace('\xc2\xb0', '')
    c = c.split()
    n = float(c[0])
    s = -1 if c[1] == "S" else 1
    e = float(c[2])
    w = -1 if c[3] == "W" else 1
    return (n*s, e*w)

@bottle.route('/<loc>')
def lookup(loc):
    o = subprocess.check_output(['tide', '-l', loc.replace('-', ' ')]).split('\n')
    if len(o) == 1:
        return bottle.abort(404, 'Location Not Found')
    l = []
    for i in o:
        if 'Tide' in i:
            split = i.split()
            d = ' '.join(split[:3])
            event = ' '.join(split[6:])
            height = ' '.join(split[4:6])
            l.append({'date': d, 'event': event, 'height': height})
    location = o[0]
    coord = parse_coord(o[1])
    return {'location': location, 'coord': coord, 'events': l}

bottle.run(port=5050)
