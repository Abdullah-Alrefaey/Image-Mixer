# Importing Packages
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import numpy as np
import mainGUI as m
import cv2 as cv
from imageClass import *
from modesEnum import Modes
from imageModel import ImageModel

#importing module
import logging

#Create and configure logger
logging.basicConfig(level=logging.DEBUG,
                    filename="app.log",
					format='%(lineno)s - %(name)s - %(levelname)s - %(message)s',
					filemode='w')

#Creating an object
logger=logging.getLogger()

#Test messages
# logger.debug("Harmless debug Message")
# logger.info("Just an information")
# logger.warning("Its a Warning")
# logger.error("Did you try to divide by zero")
# logger.critical("Internet is down")


class imagesMixer(m.Ui_MainWindow):

    def __init__(self, starterWindow):
        """
        Main loop of the UI
        :param mainWindow: QMainWindow Object
        """
        super(imagesMixer, self).setupUi(starterWindow)

        self.imageComponents = ...                                      # Dictionary contains the fourier transform components
        self.imageComponentsDict = {"image1": ..., "image2": ...}       # Dictionary contains the components of the 2 images
        self.firstComponent = ...                                       # First Component of the mix
        self.secondComponent = ...                                      # Second Component of the mix
        self.sliderOneValue = 0                                         # Value of Slider One
        self.sliderTwoValue = 0                                         # Value of Slider Two
        self.outID = 0                                                  # ID of output image
        self.imageNumber = [..., ...]

        # Load Buttons
        self.loadButtons = [self.actionImage1, self.actionImage2]

        # Images Lists
        self.inputImages = [self.img1_original, self.img2_original]
        self.updatedImages = [self.img1_updated, self.img2_updated]
        self.outputImages = [self.output_img1, self.output_img2]

        self.imageWidgets = [self.img1_original, self.img2_original, self.img1_updated, self.img2_updated, self.output_img1, self.output_img2]

        # Combo Lists
        self.updateCombos = [self.combo_input1, self.combo_input2]
        self.imageCombos = [self.combo_select_img1, self.combo_select_img2]
        self.componentCombos = [self.combo_select_mode1, self.combo_select_mode2]

        # Sliders List
        self.sliders = [self.slider_comp1, self.slider_comp2]
        self.slidersValues = [self.sliderOneValue, self.sliderTwoValue]

        # combos and sliders list
        self.components = [self.combo_select_img1, self.combo_select_img2, self.combo_select_mode1, self.combo_select_mode2, self.slider_comp1, self.slider_comp2, self.combo_output]

        # Adjust the shape and scales of the widgets
        for widget in self.imageWidgets:
            widget.ui.histogram.hide()
            widget.ui.roiBtn.hide()
            widget.ui.menuBtn.hide()
            widget.ui.roiPlot.hide()
            widget.getView().setAspectLocked(False)
            widget.view.setAspectLocked(False)

        # Setup Load Connections
        self.actionImage1.triggered.connect(lambda: self.loadFile(0))
        self.actionImage2.triggered.connect(lambda: self.loadFile(1))

        # Combo Connections
        self.combo_input1.activated.connect(lambda: self.updateCombosChanged(0))
        self.combo_input2.activated.connect(lambda: self.updateCombosChanged(1))

        self.combo_select_img1.activated.connect(lambda: self.imageCombosChanged(0))
        self.combo_select_img2.activated.connect(lambda: self.imageCombosChanged(1))

        self.combo_select_mode1.activated.connect(lambda: self.selectCombosChanged(0))
        self.combo_select_mode2.activated.connect(lambda: self.selectCombosChanged(1))

        # Slider Connections
        self.sliders[0].valueChanged.connect(lambda: self.sliderChanged(0))
        self.sliders[1].valueChanged.connect(lambda: self.sliderChanged(1))

        # self.componentCombos[comboID + 1].setItemData(1, QtCore.QSize(0, 0), QtCore.Qt.SizeHintRole)


    def loadFile(self, imgID):
        """
        Load the File from User
        :param imgID: 0 or 1
        :return:
        """
        # Open File & Check if it was loaded correctly
        repo_path = "D:\Study\Courses\Python\DSP Tasks - 3rd Year\sbe309-2020-task3-Abdullah-Alrefaey\images"
        self.filename, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "Load Image", repo_path, "*.jpg;;" "*.jpeg;;" "*.png;;")
        if self.filename == "":
            pass
        else:
            self.image = cv.imread(self.filename, flags=cv.IMREAD_GRAYSCALE).T
            height, width = self.image.shape
            if self.image.shape[0] != 500 or self.image.shape[1] != 500:
                self.showMessage("Warning!!", "The uploaded image size is: " + str(height) + " x " + str(width) +
                                 "\nImage size must be 250 x 250, please upload another image", QMessageBox.Ok, QMessageBox.Warning)
            else:
                # Fourier Transform and its components
                self.inputImages[imgID].imgByte = self.image
                self.inputImages[imgID].dft = np.fft.fft2(self.image)
                self.inputImages[imgID].magnitude = np.abs(self.inputImages[imgID].dft)
                self.inputImages[imgID].imaginary = np.imag(self.inputImages[imgID].dft)
                self.inputImages[imgID].phase = np.angle(self.inputImages[imgID].dft)
                self.inputImages[imgID].real = np.real(self.inputImages[imgID].dft)
                self.inputImages[imgID].uniformMagnitude = np.ones(self.image.shape)
                self.inputImages[imgID].uniformPhase = np.zeros(self.image.shape)

                # Display the original Image
                self.inputImages[imgID].displayImage(self.image)
                self.updateCombos[imgID].setEnabled(True)

                if self.updateCombos[0].isEnabled() and self.updateCombos[1].isEnabled():
                    self.enableOutputCombos()


    def updateCombosChanged(self, id):
        selectedComponent = self.getComboValue(self.updateCombos[id])

        if selectedComponent == "choose ft component":
            pass
        elif selectedComponent == "magnitude":
            self.updatedImages[id].displayImage(self.inputImages[id].magnitude)
        elif selectedComponent == "phase":
            self.updatedImages[id].displayImage(self.inputImages[id].phase)
        elif selectedComponent == "real":
            self.updatedImages[id].displayImage(self.inputImages[id].real)
        elif selectedComponent == "imaginary":
            self.updatedImages[id].displayImage(self.inputImages[id].imaginary)


    def imageCombosChanged(self, comboID):
        # self.imageNumber = self.getComboValue(self.imageCombos[comboID])
        # self.selectCombosChanged(comboID)
        pass

    def selectCombosChanged(self, comboID):
        self.getOutputID()
        mixOutput = ...

        # get the selected value
        self.imageNumber[comboID] = self.getComboValue(self.imageCombos[comboID])
        self.imageNumber[~comboID] = self.getComboValue(self.imageCombos[~comboID])
        print("selected image comp:" , comboID, self.imageNumber[comboID])
        print("selected image comp:", ~comboID, self.imageNumber[~comboID])


        selectedComponent = self.getComboValue(self.componentCombos[comboID])
        otherSelect = self.getComboValue(self.componentCombos[~comboID])
        print("current Combo Value: ", selectedComponent)
        print("other Combo Value: ", otherSelect)
        self.sliderOneValue = self.slider_comp1.value() / 100
        self.sliderTwoValue = self.slider_comp2.value() / 100


        # # Update the other combo with the correct choices
        if comboID == 0:
            self.adjustComboBox(comboID + 1, selectedComponent)
        else:
            self.adjustComboBox(comboID - 1, selectedComponent)

        if selectedComponent == "choose component":
            pass

        try:
            if (selectedComponent == "magnitude" and otherSelect == "phase") or (selectedComponent == "phase" and otherSelect == "magnitude"):
                if self.imageNumber[comboID] == "image2":
                    self.slidersValues[comboID] = 1 - self.slidersValues[comboID]
                if self.imageNumber[~comboID] == "image2":
                    self.slidersValues[~comboID] = 1 - self.slidersValues[~comboID]
                mixOutput = self.inputImages[0].mix(self.inputImages[1], self.sliderOneValue, self.sliderTwoValue, Modes.magnitudeAndPhase)

            elif (selectedComponent == "real" and otherSelect == "imaginary") or (selectedComponent == "imaginary" and otherSelect == "real"):
                if self.imageNumber[comboID] == "image2":
                    self.slidersValues[comboID] = 1 - self.slidersValues[comboID]
                if self.imageNumber[~comboID] == "image2":
                    self.slidersValues[~comboID] = 1 - self.slidersValues[~comboID]
                mixOutput = self.inputImages[0].mix(self.inputImages[1], self.sliderOneValue, self.sliderTwoValue, Modes.realAndImaginary)

            self.outputImages[self.outID].displayImage(mixOutput)
        except Exception as e:
            logger.error("Exception occurred", exc_info=True)


    def enableOutputCombos(self):
        for item in self.components:
            item.setEnabled(True)


    def getComboValue(self, comboName):
        """
        :param name: object name of the combo
        :return: value of the combo
        """
        value = comboName.currentText().lower()
        return value


    def adjustComboBox(self, comboID, type):
        """

        :param comboID: index of the other comboBox
        :param mode: type of component (clear the other types)
        :return:
        """
        selectedItem = self.componentCombos[comboID].currentText()

        self.componentCombos[comboID].clear()
        self.componentCombos[comboID].addItem("Choose Component")

        if type == "choose component":
            for i in range(2):
                self.componentCombos[i].clear()
                self.componentCombos[i].addItem("Choose Component")
                self.componentCombos[i].addItem("Magnitude")
                self.componentCombos[i].addItem("Phase")
                self.componentCombos[i].addItem("Real")
                self.componentCombos[i].addItem("Imaginary")
                self.componentCombos[i].addItem("Uniform Magnitude")
                self.componentCombos[i].addItem("Uniform Phase")
                self.componentCombos[i].setCurrentText("Choose Component")
        elif type == "magnitude":
            self.componentCombos[comboID].addItem("Phase")
            self.componentCombos[comboID].addItem("Uniform Phase")
            self.componentCombos[comboID].setCurrentText(selectedItem)
        elif type == "phase":
            self.componentCombos[comboID].addItem("Magnitude")
            self.componentCombos[comboID].addItem("Uniform Magnitude")
            self.componentCombos[comboID].setCurrentText(selectedItem)
        elif type == "real":
            self.componentCombos[comboID].addItem("Imaginary")
            self.componentCombos[comboID].setCurrentText(selectedItem)
        elif type == "imaginary":
            self.componentCombos[comboID].addItem("Real")
            self.componentCombos[comboID].setCurrentText(selectedItem)
        elif type == "uniform magnitude":
            self.componentCombos[comboID].addItem("Phase")
            self.componentCombos[comboID].addItem("Uniform Phase")
            self.componentCombos[comboID].setCurrentText(selectedItem)
        elif type == "uniform phase":
            self.componentCombos[comboID].addItem("Magnitude")
            self.componentCombos[comboID].addItem("Uniform Magnitude")
            self.componentCombos[comboID].setCurrentText(selectedItem)

    def sliderChanged(self, index):
        """

        :param index: refer to the clicked slider
        :return:
        """
        self.slidersValues[index] = self.sliders[index].value()
        # self.selectCombosChanged(index)

    def getOutputID(self):
        # Check where the output image will be displayed
        outputImage = self.getComboValue(self.combo_output)
        if outputImage == "output1":
            self.outID = 0
        elif outputImage == "output2":
            self.outID = 1

    def updateStatus(self):
        # Check which output


        pass

    def showMessage(self, header, message, button, icon):
        msg = QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(button)
        x = msg.exec_()


def main():
    """
    the application startup functions
    :return:
    """
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = imagesMixer(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
