from PIL import Image
import PySimpleGUI as sg
import os.path
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

def run_GUI():

	file_list_column = [
		[
			sg.Text("Image Folder"),
			sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
			sg.FolderBrowse(),
		],
		[
			sg.Listbox(
				values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
			)
		],
	]

	image_viewer_column = [
		[sg.Text("Choose an image from list on left:")],
		[sg.Text(size=(40, 1), key="-TOUT-")],
		[sg.Image(key="-IMAGE-")],
		[sg.Text(size=(40,1),key="-PREDICTION-")],
	]

	layout = [
		[
			sg.Column(file_list_column),
			sg.VSeperator(),
			sg.Column(image_viewer_column),
		]
	]

	window = sg.Window("Image Viewer", layout)

	model = load_model('final_model.h5')

	while True:
		event, values = window.read()
		if event == "Exit" or event == sg.WIN_CLOSED:
			break
		if event == "-FOLDER-":
			folder = values["-FOLDER-"]
			try:
				file_list = os.listdir(folder)
			except:
				file_list = []

			fnames = [
				f
				for f in file_list
				if os.path.isfile(os.path.join(folder, f))
				and f.lower().endswith((".png", ".gif"))
			]
			window["-FILE LIST-"].update(fnames)
		elif event == "-FILE LIST-":
			try:
				filename = os.path.join(
					values["-FOLDER-"], values["-FILE LIST-"][0]
				)
				window["-TOUT-"].update(filename)
				image = Image.open(filename)
				temp = image.resize((400,400))
				temp.save('temp.png')
				window["-IMAGE-"].update(filename='temp.png')
				window["-PREDICTION-"].update(str(model_predict(model,filename)))

			except:
				pass

	window.close()

def load_image(filename):
	# load the image
	img = load_img(filename, grayscale=True, target_size=(28, 28))
	# convert to array
	img = img_to_array(img)
	# reshape into a single sample with 1 channel
	img = img.reshape(1, 28, 28, 1)
	# prepare pixel data
	img = img.astype('float32')
	img = img / 255.0
	return img
 
def model_predict(model,filename):
	# load the image
    img = load_image(filename)
    # predict the class
    digit = model.predict_classes(img)
    return digit[0]

run_GUI()