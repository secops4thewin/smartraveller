#Import Modules
import requests, json,re,time,csv,sys
from bs4 import BeautifulSoup
#Reload Sys module
reload(sys)  
#Set Default Enconding
sys.setdefaultencoding('utf8')

#Set Header for User Agents
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
#Issue request to smartraveller
r = requests.get('http://smartraveller.gov.au/countries/pages/list.aspx',headers)
#Parse HTML
soupMain = BeautifulSoup(r.text,"html.parser")

#Find 13th Javascript File
js_text = soupMain.findAll('script', type="text/javascript")[12].text

#Replace any escape characters
js_text2 = js_text.strip().replace("\\","")

#Slice up array
dict_json = js_text2[61:-3]
#Open a file for writing
csv_stdata = open('./smartraveller.csv', 'wb')
#Stipulate the format is excel 
csvwriter = csv.writer(csv_stdata,dialect='excel')

#Write the csv header to a list
csv_header = ["title","more_info","date_of_release","travel_advisory","level","text"]

#Write the header to the csv files
csvwriter.writerow(csv_header)

#Split the JSON array and replace any null dates with a value
for a in re.findall('(\{"Title".+?Date\(\d+\)\/"\})',dict_json.replace('null','"/Date(0000)/"')):
	#Fix up JSON array for parsing with json loads
	z = a.replace('"{','{').replace('}]}"','}]}').replace('[]}"','[]}')
	#Parse json script
	x = json.loads(z)
	#Grab the Country Name
	title = x['Title']
	#Provide a link for users
	more_info = 'http://smartraveller.gov.au/' + x['FileRef'].split("#")[1]
	#Extract the date with regex
	date_len = re.findall('(\d{13})',x['ArticleStartDate'])
	#Extract the items
	item_len = 	x['Smartraveller_x0020_Advice_x0020_Levels']['items']
	
	#If the length of date is greater than 0
	if len(date_len)>0:
		#Parse the date to localtime of running the script
		time_local = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(date_len[0])/1000.))
	#If the length of date is 0
	elif len(date_len)==0:
		#Set time_local to no time
		time_local = "No Time"
	#If length of item is greater than 0
	if len(item_len)>0:
		#For each item in range of items
		for a in range(0,len(x['Smartraveller_x0020_Advice_x0020_Levels']['items'])):
			#Output the variables exported from json
			isTA = 	str(x['Smartraveller_x0020_Advice_x0020_Levels']['isTA'])
			level = x['Smartraveller_x0020_Advice_x0020_Levels']['items'][a]['level']
			text = x['Smartraveller_x0020_Advice_x0020_Levels']['items'][a]['text']
			#Format data neatly and write the row
			csvwriter.writerow([str(title),str(more_info),str(time_local),str(isTA),str(level),str(text)])
	elif len(item_len)==0:
		#If there are no items then there is no Travel Advisory
		isTA = 	"null"
		level = "null"
		text = "null"
		#Format data neatly and write the row
		csvwriter.writerow([str(title),str(more_info),str(time_local),str(isTA),str(level),str(text)])
		


