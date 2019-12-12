import os
import xml.etree.ElementTree as ET
from skimage import io
import matplotlib.pyplot as plt

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
	
	imagepath = annotation.find('path').text
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
	return imagepath,boxdata,boxclass


annotation_path = './annotation'
num_case = os.listdir(annotation_path)
cnt = 0
for i in range(len(num_case)):
	case_path = annotation_path + '/' + num_case[i]
	txt_path = './txt/' +num_case[i]
	os.makedirs(txt_path)
	case_file = os.listdir(case_path)
	for j in range(len(case_file)):
		imagepath,boxdata,boxclass = readxml(case_path + "/" + case_file[j])	
		txtfile = txt_path + "/" + case_file[j][:-3] + "txt"
		f = open(txtfile,'w')
		for k in range(len(boxdata)):
			f.write(boxclass[k]+ " ")
			box = boxdata[k]
			for m in range(4):
				f.write(str(box[m])+ " ")
			f.write('\n')
		f.close()
		cnt += 1
		print txtfile +" "+ str(cnt)

		'''
		img = io.imread(imagepath)
		io.imshow(img)
		
		for k in range(len(boxdata)):
			box = boxdata[k]
			plt.plot(box[0],box[2])
			plt.plot(box[0],box[3])
			
			plt.plot(box[1],box[2])
			plt.plot(box[1],box[3])

			plt.plot(box[0],box[2])
			plt.plot(box[1],box[2])
			plt.plot(box[0],box[3])
			plt.plot(box[1],box[3])
		plt.ion()
		plt.pause(0.01)
		test = input()
		'''

