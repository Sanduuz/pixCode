#!/usr/bin/env python
#-*- coding: utf-8 -*-

try:
	from PIL import Image
	import os, math
except ImportError:
	exit("\nPlease install PIL!")
except Exception as e:
	exit(e)

def encodeImage(message, filename, size):
	binstring = []
	for character in message:
		binstring.append("0"+str(bin(ord(character))[2:]))

	for index, byte in enumerate(binstring):
		if len(byte) < 8:
			byte = "0"+str(byte)
			binstring[index] = byte

	binstring = str(''.join(binstring))

	image = Image.new('RGB', (size,size), "white")
	pixels = image.load()

	column = 0
	row = 0
	for bit in binstring:
		if bit == "0":
			if column >= size:
				column = 0
				row += 1
			pixels[column,row] = (255,255,255)
			column += 1
		elif bit == "1":
			if column >= size:
				column = 0
				row += 1
			pixels[column,row] = (0,0,0)
			column += 1

	image.save(filename+str(".png"))
	return

def decodeImage(image):
	data = []
	pixels = list(image.getdata())
	for pixel in pixels:
		if pixel == (255,255,255):
			data.append("0")
		elif pixel == (0,0,0):
			data.append("1")
		else:
			print "Invalid image!"
			return
	binary_str = ''.join(data)
	binary_chunks = ' '.join([binary_str[i:i+8] for i in range(0,len(binary_str),8)])
	chunks = binary_chunks.split(" ")
	indexnums = []
	for i, byte in enumerate(chunks):
		if len(byte) < 8:
			indexnums.append(i)
		else:
			for j, char in enumerate(byte):
				if str(char) == "1":
					break
				else:
					if j == 7:
						indexnums.append(i)
					else:
						pass
	for k in sorted(indexnums, reverse=True):
		del chunks[k]

	convertableData = []
	message = []

	for byte in chunks:
		convertableData.append('0b'+str(byte[1:]))

	for convertableByte in convertableData:
		message.append(chr(int(convertableByte,2)))

	return ''.join(message)

while True:
	print "[1. Encode] | [2. Decode] | [3. Encode (File)]"
	try:
		eod = int(raw_input(">> "))
		if eod == 1:
			message = str(raw_input("Message: "))
			size = int(math.ceil(math.sqrt(len(message)*8)))
			image_name = str(raw_input("Save as: "))
			if image_name != "":
				if not os.path.isfile(image_name+str(".png")):
					encodeImage(message, image_name, size)
					print "Image saved as:",image_name+str(".png")
				else:
					print "File already exists!"
			else:
				print "Image name can't be empty!"
		elif eod == 2:
			image_path = str(raw_input("Supply the file: "))
			image_exists = os.path.isfile(image_path)
			if image_exists:
				image = Image.open(image_path, "r").convert('RGB')
				returnedData = decodeImage(image)
				if returnedData != None:
					print "Message:",returnedData
			else:
				print "File Not Found!"
		elif eod == 3:
			file_location = str(raw_input("File location: "))
			if file_location != "":
				if os.path.isfile(file_location):
					with open(file_location, "r") as messageFile:
						contents = messageFile.read()
					size = int(math.ceil(math.sqrt(len(contents)*8)))
					image_name = str(raw_input("Save as: "))
					if image_name != "":
						if not os.path.isfile(image_name+str(".png")):
							encodeImage(contents, image_name, size)
							print "Image saved as:",image_name+str(".png")
						else:
							print "File already exists!"
					else:
						print "Image name can't be empty!"
				else:
					print "File Not Found!"
		else:
			print "Choose 1 or 2!"
	except ValueError:
		print "Use integers only!"
	except KeyboardInterrupt:
		os._exit(0)
	except EOFError:
		os._exit(0)
	except Exception as e:
		exit(e)