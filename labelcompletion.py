import os
import xml.etree.ElementTree as ET
from lxml import etree
import codecs

ENCODING = 'utf-8'
def sortbndbox(boxdata,boxclass):
	for i in range(len(boxdata)):
		for j in range(1,len(boxdata)-i):
			if boxdata[j-1][0]>boxdata[j]:
				boxdata[j-1],boxdata[j] = boxdata[j],boxdata[j-1]
				boxclass[j-1],boxclass[j] = boxclass[j],boxclass[j-1]
	return boxdata,boxclass
				
def readxml(file_path):
	tree = ET.ElementTree()
	annotation = tree.parse(file_path)
	boxes = annotation.findall('object')
	boxdata=[]
	boxclass=[]
	for i in range(len(boxes)):
		boxclass.append(boxes[i].find('name').text)
		box = boxes[i].find('bndbox')
		pixels = [int(box.find('xmin').text), int(box.find('ymin').text),
 			int(box.find('xmax').text), int(box.find('ymax').text)]
		boxdata.append(pixels)
	if len(boxdata) > 1:
		boxdata,boxclass = sortbndbox(boxdata,boxclass)
	return boxdata,boxclass

def fileparse(case_file):
	nameid=[]
	for i in range(len(case_file)):
		name = case_file[i].split('.')
		#nameid.append(int(case_file[i][:-4]))
		for j in range(len(name)):
			if len(name[j]) == 10:
				nameid.append(int(name[j]))
				break
	nameid.sort()
	filegroup =[]
	for i in range(len(nameid)-1):
		startid = nameid[i]
		endid = nameid[i+1]
		if endid - startid == 1:
			continue			
		filegroup.append(range(startid,endid+1,1))
	return filegroup 
def prettify(elem):
	rough_string = ET.tostring(elem,'utf8')
	root = etree.fromstring(rough_string)
	return etree.tostring(root, pretty_print=True, encoding = ENCODING).replace("  ".encode(), "\t".encode())
def writexml(savepath,currentbox,currentclass):
	top = ET.Element('annotation')
	path = ET.SubElement(top, 'path')
	path.text = str(image_path+savepath[-14:-4]+".jpg")
	for i in range(len(currentbox)):
		objname = currentclass[i]
		objdata = currentbox[i]

		obj = ET.SubElement(top,'object')
		name = ET.SubElement(obj, 'name')
		name.text = str(objname)
		

		bndbox = ET.SubElement(obj, 'bndbox')
		xmin = ET.SubElement(bndbox, 'xmin')
		xmin.text = str(objdata[0])
		ymin = ET.SubElement(bndbox, 'ymin')
		ymin.text = str(objdata[1])
		xmax = ET.SubElement(bndbox, 'xmax')
		xmax.text = str(objdata[2])
		ymax = ET.SubElement(bndbox, 'ymax')
		ymax.text = str(objdata[3])
	tree = ET.ElementTree(top)
	tree.write(savepath)
	#outfile = codecs.open(savepath, 'w', encoding = ENCODING)
	#prettifyResult = prettify(outfile)
	#outfile.write(prettifyResult.decode('utf8'))
	#outfile.close
	print savepath + " done!"
def getxmlname(num):
	idstr = str(num)
	name = idstr.zfill(10)+".xml"
	return name
def insertlabel(former,latter,step,count):
	newbox=[]
	for i in range(len(former)):
		value1 = former[i]
		value2 = latter[i]
		newbox.append(value1 + (value2-value1)*count/step)
	return newbox

	
def completegrouplabel(filegroups, case_path):
	for i in range(len(filegroups)):
		filegroup = filegroups[i]
		start = filegroup[0]
		end = filegroup[len(filegroup)-1]
		step = len(filegroup)-1
		box_former,class_former = readxml(case_path+getxmlname(start))
		box_latter,class_latter = readxml(case_path+getxmlname(end))
		#For the case of mult-classes:
		#check whether former classes are the same with latter classes
		for j in range(1,len(filegroup)-1):
			currentid = filegroup[j]
			currentbox=[]
			currentclass=[]
			for k in range(len(box_former)):
				box_former_k = box_former[k]
				box_latter_k = box_latter[k]
				box_k = insertlabel(box_former_k,box_latter_k,step,j)
				currentbox.append(box_k)
				currentclass.append(class_former[k])
			writexml(case_path+getxmlname(currentid),currentbox,currentclass)		

def testxml(file_path):
	tree = ET.ElementTree()
	annotation = tree.parse(file_path)
	flag = annotation.find('folder')
	if flag == None:
 		return False
	else:
		return True	
def clearinsertedlabel(case_path,case_file):
	for i in range(len(case_file)):
		currentfile = case_path + case_file[i]
		if not testxml(currentfile):
			os.remove(currentfile)
			print currentfile + " cleared!"

	

#your annotation path
annotation_path = './annotation'
#your image path while label with labelimage
image_path = '/media/huifang/document/YQ21/2017_05_09_drive_0001_sync/image_00/data/'
num_case = os.listdir(annotation_path)
for i in range(len(num_case)):
	case_path = annotation_path + '/' + num_case[i]
	case_file = os.listdir(case_path)
	#clearinsertedlabel(case_path+'/',case_file)
	
	filegroups = fileparse(case_file)
	completegrouplabel(filegroups,case_path + '/')	




	


