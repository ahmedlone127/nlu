from lxml import html
import requests
import os 
def get_requried_info(name_of_package):
# gets the sh ,url, and fn of the give package and retunrs a dict with all three pecies of info . 
	page = requests.get(f'https://pypi.org/project/{name_of_package}/#files')
	tree = html.fromstring(page.content)
	fn = tree.xpath('//*[@id="files"]/table/tbody/tr[2]/th/a/text()')
	fn = fn[0].strip()
	url = tree.xpath('//*[@id="files"]/table/tbody/tr[2]/th/a//@href')
	url = url[0].strip()
	sha256  = tree.xpath('.//code/text()')[3]
	return {"fn":fn,"url":url,"sha256":sha256}
def edit_file(info_,path_of_file):
	# it takes the info we got from the previous fuction and replaces it inisde the given file .
	file=open(path_of_file,"r+")
	result = open("result.yaml","w+")
	lines = file.readlines()
	for line in lines :
		if "fn:" in line:
			result.write(f"  fn: {info_['fn']}\n")
		elif "url:" in line and "license" not in line :
			result.write(f"  url: {info_['url']}\n")
		elif "sha256" in line:
			result.write(f"  sha256: {info_['sha256']}\n")
		else:
			result.write(line)
			if"version"in line :
				version= line.split(" ")
				for element in version:
					if "." in element:
						version = element
						break					
	
	result.close()
	file.close()
	file=open(path_of_file,"w+")
	result = open("result.yaml","r+")
	lines = result.readlines()
	for line in lines:
		file.write(line)
	result.close()
	file.close()
	return version
info = get_requried_info("ahmedlones")
version = edit_file(info,"meta.yaml")
version = version.rstrip("\n")
os.system("python3.6 setup.py sdist bdist_wheel ")
os.system("twine upload dist/* -u ahmedlone127 -p levi_acramen")
os.system("conda-build purge")
os.system("anaconda login --username ahmedlone127 --password xboxonelover1")
os.system("conda config --set anaconda_upload yes")
os.system("rm result.yaml -r")
os.system("conda build . --python=3.6  -c conda-forge -c johnsnowlabs")
os.system("conda build . --python=3.7  -c conda-forge -c johnsnowlabs")
#os.system(f"anaconda upload /opt/conda/conda-bld/noarch/nlu-{version}-py36_0.tar.bz2 --force")
#os.system(f"anaconda upload /opt/conda/conda-bld/noarch/nlu-{version}-py37_0.tar.bz2 --force")
