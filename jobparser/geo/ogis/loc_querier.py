import ast
from conf.app_settings import GIS_SOLR_HOST
from conf.app_settings import GIS_SOLR_PASSWORD
from conf.app_settings import GIS_SOLR_USERNAME
import re
import urllib2

_RE_IRRELEVANT_CHARS = re.compile("[,\\n\\r\\t;()&|!{}*?:\+\-\[\]]")
_RE_SQUASH_SPACES = re.compile(" +")
_RE_SPLIT = re.compile("[ ,-/]")

HOST = GIS_SOLR_HOST
username = GIS_SOLR_USERNAME
password = GIS_SOLR_PASSWORD


passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
# this creates a password manager
passman.add_password(None, HOST, username, password)
# because we have put None at the start it will always
# use this username/password combination for  urls
# for which `theurl` is a super-url

authhandler = urllib2.HTTPBasicAuthHandler(passman)
# create the AuthHandler

opener = urllib2.build_opener(authhandler)

urllib2.install_opener(opener)

USSTATES = ['AL ', 'AK ', 'AZ ', 'AR', 'CA ', 'CO ', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID ', 'IL ', 'IN ', 'IA', 'KS ', 'KY', 'LA', 'ME ', 'MD ', 'MA ', 'MI ', 'MN ', 'MS ', 'MO ', 'MT', 'NE ', 'NV ', 'NH ', 'NJ ', 'NM ', 'NY ', 'NC ', 'ND', 'OH ', 'OK ', 'OR', 'PA', 'RI', 'SC ', 'SD', 'TN ', 'TX', 'UT', 'VT ', 'VA', 'WA ', 'WV ', 'WI ', 'WY']
USSTATES = [e.strip() for e in USSTATES] + [e.strip().lower() for e in USSTATES]

STATE_FULL = [['Alabama', 'AL', 'Ala'], ['Alaska', 'AK', 'Alaska'], ['Arizona', 'AZ', 'Ariz'], ['Arkansas', 'AR', 'Ark'], ['California', 'CA', 'Calif'], ['Colorado', 'CO', 'Colo'], 
    ['Connecticut', 'CT', 'Conn'], ['Delaware', 'DE', 'Del'], ['District of Columbia', 'DC', 'DC'], ['Florida', 'FL', 'Fla'], ['Georgia', 'GA', 'Ga'], ['Hawaii', 'HI', 'Hawaii'],
    ['Idaho', 'ID', ''], ['Illinois', 'IL', 'Ill'], ['Indiana', 'IN', 'Ind'], ['Iowa', 'IA', ''], ['Kansas', 'KS', 'Kans'], ['Kentucky', 'KY', 'Ky'], ['Louisiana', 'LA', 'Louisiana'],
    ['Maine', 'ME', 'Me'], ['Maryland', 'MD', 'Md'], ['Massachusetts', 'MA', 'Mass'], ['Michigan', 'MI', 'Mich'], ['Minnesota', 'MN', 'Minn'], ['Mississippi', 'MS', 'Miss'],
    ['Missouri', 'MO', 'Mo'], ['Montana', 'MT', 'Mont'], ['Nebraska', 'NE', 'Nebr'], ['Nevada', 'NV', 'Nev'], ['New Hampshire', 'NH', 'NH'], ['New Jersey', 'NJ', 'NJ'], ['New Mexico', 'NM', 'NMex'],
    ['New York', 'NY', 'NY'], ['North Carolina', 'NC', 'NC'], ['North Dakota', 'ND', ''], ['Ohio', 'OH', 'Ohio'], ['Oklahoma', 'OK', 'Okla'], ['Oregon', 'OR', 'Ore'], ['Pennsylvania', 'PA', 'Penn'],
    ['Rhode Island', 'RI', 'RI'], ['South Carolina', 'SC', 'SC'], ['South Dakota', 'SD', 'South Dakota'], ['Tennessee', 'TN', 'Tenn'], ['Texas', 'TX', 'Tex'], ['Utah', 'UT', 'Utah'], ['Vermont', 'VT', 'Vt'],
    ['Virginia', 'VA', 'Va'], ['Washington', 'WA', 'Wash'], ['West Virginia', 'WV', 'WVa'], ['Wisconsin', 'WI', 'Wis'], ['Wyoming', 'WY', 'Wyo']]

BOOSTS = {'WA': ['27', '1', '1.2'], 'DE': ['27', '1', '1.2'], 'WI': ['27', '1', '1.2'], 'WV': ['27', '1', '1.2'], 'HI': ['27', '1', '1.2'], 'FL': ['29.15', '1', '1.2'], 'WY': ['27', '1', '1.2'], 
    'NH': ['27', '1', '1.2'], 'NJ': ['27', '1', '1.2'], 'NM': ['27', '1', '1.2'], 'TX': ['27', '1', '1.2'], 'LA': ['27', '1', '1.2'], 'NC': ['27', '1', '1.2'], 'ND': ['27', '1', '1.2'],
    'NE': ['27', '1', '1.2'], 'TN': ['27', '1', '1.2'], 'NY': ['27', '1', '1.2'], 'PA': ['27', '1', '1.2'], 'CA': ['29.2', '1', '1.2'], 'NV': ['27', '1', '1.2'], 'VA': ['27', '1', '1.2'],
    'CO': ['27', '1', '1.2'], 'AK': ['27', '1', '1.2'], 'AL': ['27', '1', '1.2'], 'AR': ['27', '1', '1.2'], 'VT': ['27', '1', '1.2'], 'IL': ['27', '1', '1.2'], 'GA': ['27', '1', '1.2'],
    'IN': ['29.2', '1', '1.2'], 'IA': ['27', '1', '1.2'], 'OK': ['27', '1', '1.2'], 'AZ': ['27', '1', '1.2'], 'ID': ['27', '1', '1.2'], 'CT': ['27', '1', '1.2'], 'ME': ['27', '1', '1.2'],
    'MD': ['27', '1', '1.2'], 'MA': ['27', '1', '1.2'], 'OH': ['27', '1', '1.2'], 'UT': ['27', '1', '1.2'], 'MO': ['27', '1', '1.2'], 'MN': ['27', '1', '1.2'], 'MI': ['27', '1', '1.2'],
    'RI': ['27', '1', '1.2'], 'KS': ['27', '1', '1.2'], 'MT': ['27', '1', '1.2'], 'MS': ['27', '1', '1.2'], 'SC': ['27', '1', '1.2'], 'KY': ['27', '1', '1.2'], 'OR': ['27', '1', '1.2'], 'SD': ['27', '1', '1.2']}

def query(qsr):
    QDICT = {'adm1_code':[], 'all_adm1_name':[], 'all_adm2_name':[], 'name':[], 'all_country_name':[], 'country_code':[]}
    
    #print qsr
    qsrc = _cleanup(qsr)
    try:
        sp = [unicode(e, errors='ignore') for e in list(set(filter(None, _split(qsrc))))]
    except TypeError, t:
        sp = [e for e in list(set(filter(None, _split(qsrc))))]
    if not sp:return None
    
    common = set(sp).intersection(set(USSTATES))
    sp1 = []
    if not len(common):
        for e in sp:
            for state in STATE_FULL:
                if state[0] == e or state[2] == e:
                    sp1.append(state[1])
                    break
        
    sp = list(set(sp + sp1))
    #print sp
    for e in sp:
        for k in QDICT.keys():
            QDICT[k].append(e)
    s = ''
    for k, v in QDICT.items():
        s += ' '.join([k + ':' + e for e in v])
        s += ' '
    s = s.strip()
    
    boosts = ['27', '1', '1.2']
    common = set(sp).intersection(set(USSTATES))
    if len(common):
        s += ' adm1_code:%s^5.0' % list(common)[0]
        boosts = BOOSTS.get(list(common)[0].upper(), ['27', '1', '1.2'])
    s = s.lower()
    query_str = '+(%s) feature_code:PPL^%s feature_code:ADM1^%s feature_code:ADM2^%s' % (s, boosts[0], boosts[1], boosts[2])
    if 'CA' in list(common):
        query_str += ' country_code:US'
    # Tinh Ca Mau (adm1code=77) is screwing CA USA. Bad hack
    if 'ca' in sp or 'CA' in sp:
        query_str += ' -adm1_code:77'
        
    url = HOST + 'geosearch/select?indent=on&version=2.2&q=%s&version=2.2&wt=python&rows=10&qt=advanced' % urllib2.quote(query_str)
    url += '&fl=fully_qualified_name%2Clat%2Clng%2Ccountry_code%2Cadm1_name%2Cadm1_code%2Cadm2_name%2Cadm2_code%2Cplacetype%2Cname_ascii%2Cscore%2Cfeature_code'

    
    try:
        conn = urllib2.urlopen(url)
        rsp = ast.literal_eval(conn.read())
        loc = [e for e in rsp['response']['docs']]
        #print query_str

        topscore = rsp['response']['maxScore']
        res = None
        if len(loc):
            for e in loc:
                if e['score'] < topscore:
                    break
                res = e
                if e['country_code'] == 'US':break
            loc = e
        else:return

        lat, lng = loc['lat'], loc['lng']
        if loc['country_code'] == 'US':
            if loc['feature_code'] == 'PPL':
                return (lat, lng, loc['name_ascii'], loc.get('adm2_name', ''), loc.get('adm1_code', ''), 'US')
            else:
                return (lat, lng, '', loc.get('adm2_name', ''), loc.get('adm1_code', ''), 'US')
    except Exception, e:        
        print e
        return None
    return None
    
def _cleanup(s):

    s = s.strip()
    s = _RE_IRRELEVANT_CHARS.sub(" ", s)
    s = _RE_SQUASH_SPACES.sub(" ", s)

    return s

def _split(s):

    sp = []
    sp_indices = []
    i = 0
    while True:
        m = _RE_SPLIT.search(s, i)
        if m is None:
            break

        sp.append(s[i:m.start()])
        sp_indices.append((i, m.start()))

        i = m.end()

    sp.append(s[i:])

    return sp
   
 
if __name__ == "__main__":
    print query('California-Escondido')
