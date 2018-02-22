#Maa finne ut hvordan man bruker eksisterende cookies
from lxml import html
import requests
import ConfigParser	#For bruker og pass lesing fra fil
config = ConfigParser.RawConfigParser()
config.read('login.cfg')	#Henter passord og brukernavn fra fil. Her defineres lokasjonen
user = config.get('section1', 'user')
passw = config.get('section1', 'pass')




def bestill():
	c=requests.Session()
	url0 = 'https://tp.uio.no/ntnu/rombestilling/'
        url2 = 'https://tp.uio.no/ntnu/rombestilling/'

#####################################################################################################
	#For aa lagre cookies i variabel
		#laster inn sidne for aa skaffe cookies og token som brukes
		#i post requesten for aa logge inn gjenom feide
	data0 = {}			#Tom liste for post requesten
	a = c.get(url0)			#Selve post requesten
	SAML = c.cookies['SimpleSAMLSessionID']
	PHPSE = c.cookies['PHPSESSID']
	#print PHPSE

		#for aa skaffe riktig token og url hentes dette fra en nettside
		#Travaserer svaret fra server og henter ut token
	tree = html.fromstring(a.content)
	test = tree.xpath('//*[@id="languageSelector"]/input[2]/@value')
	test2 = ''.join(test)
	#print test2


######################################################################################################

	#skaffer lenden til teksten, forde den trengs for aa sende nummer paa lengden ogsaa
	AUTESTATE = test2
	ASLENGHT = len(AUTESTATE)	#teller karakterer i token AUTESTATE

		#url for innlogging som bruker token som er hentet tidligere
        url = 'https://idp.feide.no/simplesaml/module.php/feide/login.php?asLen=282&AuthState=_' + AUTESTATE + '&org=ntnu.no'

	login_data = {
		'asLen': ASLENGHT,
		'AuthState': test2,
		'org': 'ntnu.no',
		'has_js': 'true',
		'inside_iframe': '0',
		'feidename': user,
		'password': passw
		}
	svar = c.post(url, data=login_data) #loging in


#####################################################################################################
	#print svar.content	#For debuging

		#pga ikke javascript er i bruk i scriptet maa man innom en ekstra side for workaround
		#token fra svaren man fikk paa forje request
	tree2 = html.fromstring(svar.content)
        noJavascript = tree2.xpath('/html/body/form/input[2]/@value')
	noJavascript = ''.join(noJavascript)


	noJsData = {
			'SAMLResponse': noJavascript,
			'RelayState': 'https://tp.uio.no/ntnu/rombestilling/?'

		}
	noJsURL = 'https://tp.uio.no/simplesaml/module.php/saml/sp/saml2-acs.php/feide-sp'
	nadaJS = c.post(noJsURL, noJsData)

	#print nadaJS.content

###################################################################################################


	#for bestilling for aa faa tokenrb
		#Requeste en side med sok paa rom for aa faa token som brukes paa selve bestillingen
        beforebestill = {
                'start': '08:00',
                'size': '5',
                'roomtype': 'NONE',
                'duration': '01:00',
                'area': '50000',
                'room[]': '502k112',
                'building': "502",	#k
                'preset_date': '2018-02-28',
                'exam': "",
		'submitall': 'Bestill'
        }
        svar = c.post(url2, data=beforebestill)      #Sending bestill
        #print svar.content

	tree3 = html.fromstring(svar.content)
        token = tree3.xpath('//*[@id="origform"]/input[11]/@value')	#pass paa input nummer kan endre seg
        #print token
	token = ''.join(token)
	#print token

#################################################################################################



	#bestill
		#Selve bestillingen og de parametere man trenger
        bestill = {
		'name': "",
		'note': "",
		'confirmed': 'true',
		'start': '08:00',
		'size': '5',
		'roomtype': 'NONE',
		'duration': '01:00',
		'area': '50000',
		'room[]': '502K112',
		'building': "502",
		'preset_day': 'WED',
		'preset_date': '2018-02-28',
		'exam': "",
		'dates[]': '2018-02-28',
		'tokenrb': token,
	}
        r = c.post(url2, data=bestill)      #Sending bestill
        svar = c.post(url2, data=bestill)      #Sending bestill
	#print svar.content	"brukes for debug
bestill()


