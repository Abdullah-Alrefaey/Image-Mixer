# Importing Packages
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import numpy as np
import mainGUI as m
import cv2
from modesEnum import Modes
from imageModel import ImageModel

# importing module
import logging

# Create and configure logger
logging.basicConfig(level=logging.DEBUG,
                    filename="app.log",
                    format='%(lineno)s - %(levelname)s - %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()


# choose item from combo
# change combo content

class imagesMixer(m.Ui_MainWindow):

    def __init__(self, starterWindow):
        """
        Main loop of the UI
        :param mainWindow: QMainWindow Object
        """
        super(imagesMixer, self).setupUi(starterWindow)

        # Load Buttons
        self.loadButtons = [self.actionImage1, self.actionImage2]

        # Images Lists
        self.inputImages = [self.img1_original, self.img2_original]
        self.updatedImages = [self.img1_updated, self.img2_updated]
        self.outputImages = [self.output_img1, self.output_img2]
        self.imagesModels = [..., ...]
        self.imageWidgets = [self.img1_original, self.img2_original, self.img1_updated, self.img2_updated,
                             self.output_img1, self.output_img2]

        self.heights = [..., ...]
        self.weights = [..., ...]

        # Combo Lists
        self.updateCombos = [self.combo_input1, self.combo_input2]
        self.imageCombos = [self.combo_select_img1, self.combo_select_img2]
        self.componentCombos = [self.combo_select_mode1, self.combo_select_mode2]

        # Sliders List
        self.sliders = [self.slider_comp1, self.slider_comp2]

        # combos and sliders list
        self.components = [self.combo_select_img1, self.combo_select_img2, self.combo_select_mode1,
                           self.combo_select_mode2, self.slider_comp1, self.slider_comp2, self.combo_output]

        # Setup Load Connections
        self.actionImage1.triggered.connect(lambda: self.loadFile(0))
        self.actionImage2.triggered.connect(lambda: self.loadFile(1))

        # Combo Connections
        self.combo_input1.activated.connect(lambda: self.updateCombosChanged(0))
        self.combo_input2.activated.connect(lambda: self.updateCombosChanged(1))

        self.combo_select_img1.activated.connect(self.updateComboStatus)
        self.combo_select_img2.activated.connect(self.updateComboStatus)

        self.combo_select_mode1.activated.connect(self.updateComboStatus)
        self.combo_select_mode2.activated.connect(self.updateComboStatus)

        # Slider Connections
        self.sliders[0].valueChanged.connect(self.updateComboStatus)
        self.sliders[1].valueChanged.connect(self.updateComboStatus)

        self.setupImagesView()
        # self.componentCombos[comboID + 1].setItemData(1, QtCore.QSize(0, 0), QtCore.Qt.SizeHintRole)
        logger.info("The Application started successfully")

    def loadFile(self, imgID):
        """
        Load the File from User
        :param imgID: 0 or 1
        :return:
        """
        # Open File & Check if it was loaded correctly
        logger.info("Browsing the files...")
        repo_path = "D:\Study\Courses\Python\DSP Tasks - 3rd Year\sbe309-2020-task3-Abdullah-Alrefaey\images"
        self.filename, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "Load Image", repo_path,
                                                                           "*.jpg;;" "*.jpeg;;" "*.png;;")
        imgName = self.filename.split('/')[-1]
        if self.filename == "":
            pass
        else:
            image = cv2.imread(self.filename, flags=cv2.IMREAD_GRAYSCALE).T
            self.heights[imgID], self.weights[imgID] = image.shape
            self.imagesModels[imgID] = ImageModel(self.filename)

            if type(self.imagesModels[~imgID]) == type(...):
                # Create and Display Original Image
                self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
                self.updateCombos[imgID].setEnabled(True)
                logger.info(f"Added Image{imgID + 1}: {imgName} successfully")
            else:
                if self.heights[1] != self.heights[0] or self.weights[1] != self.weights[0]:
                    self.showMessage("Warning!!", "Image sizes must be the same, please upload another image",
                                     QMessageBox.Ok, QMessageBox.Warning)
                    logger.warning("Warning!!. Image sizes must be the same, please upload another image")
                else:
                    self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
                    self.updateCombos[imgID].setEnabled(True)
                    logger.info(f"Added Image{imgID + 1}: {imgName} successfully")

            if self.updateCombos[0].isEnabled() and self.updateCombos[1].isEnabled():
                self.enableOutputCombos()
                logger.info("ComboBoxes have been enabled successfully")

    def setupImagesView(self):
        """
        Adjust the shape and scales of the widgets
        Remove unnecessary options
        :return:
        """
        for widget in self.imageWidgets:
            widget.ui.histogram.hide()
            widget.ui.roiBtn.hide()
            widget.ui.menuBtn.hide()
            widget.ui.roiPlot.hide()
            widget.getView().setAspectLocked(False)
            widget.view.setAspectLocked(False)

    def displayImage(self, data, widget):
        """
        Display the given data
        :param data: 2d numpy array
        :param widget: ImageView object
        :return:
        """
        widget.setImage(data)
        widget.view.setRange(xRange=[0, self.imagesModels[0].imgShape[0]], yRange=[0, self.imagesModels[0].imgShape[1]],
                             padding=0)
        widget.ui.roiPlot.hide()

    def updateCombosChanged(self, id):
        selectedComponent = self.updateCombos[id].currentText().lower()

        fShift = np.fft.fftshift(self.imagesModels[id].dft)
        magnitude = 20 * np.log(np.abs(fShift))
        phase = np.angle(fShift)
        real = 20 * np.log(np.real(fShift))
        imaginary = np.imag(fShift)

        if selectedComponent == "magnitude":
            self.displayImage(magnitude, self.updatedImages[id])
        elif selectedComponent == "phase":
            self.displayImage(phase, self.updatedImages[id])
        elif selectedComponent == "real":
            self.displayImage(real, self.updatedImages[id])
        elif selectedComponent == "imaginary":
            self.displayImage(imaginary, self.updatedImages[id])

        logger.info(f"Viewing {selectedComponent} Component Of Image{id + 1}")

    def updateComboStatus(self):
        """
        The Main function of updating the status of the combo boxes and sliders for generating the mix
        This function is called when any action related to the comboBoxes of slider is triggered in the GUI
        :return:
        """
        # get the selected value
        mixOutput = ...
        outID = self.combo_output.currentIndex()
        imgIndex1 = self.imageCombos[0].currentIndex()
        imgIndex2 = self.imageCombos[1].currentIndex()
        componentOne = self.componentCombos[0].currentText().lower()
        componentTwo = self.componentCombos[1].currentText().lower()
        cmp2 = self.componentCombos[1].currentText()
        self.sliderOneValue = self.slider_comp1.value() / 100.0
        self.sliderTwoValue = self.slider_comp2.value() / 100.0

        # Update the other combo with the correct choices
        self.adjustComboBox(componentOne, cmp2)

        try:
            if componentOne == "magnitude":
                if componentTwo == "phase":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,
                                                                 self.sliderTwoValue, Modes.magnitudeAndPhase)
                if componentTwo == "uniform phase":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,
                                                                 self.sliderTwoValue, Modes.magnitudeAndUniformPhase)

            elif componentOne == "phase":
                if componentTwo == "magnitude":
                    mixOutput = self.imagesModels[imgIndex2].mix(self.imagesModels[imgIndex1], self.sliderTwoValue,
                                                                 self.sliderOneValue, Modes.magnitudeAndPhase)
                elif componentTwo == "uniform magnitude":
                    mixOutput = self.imagesModels[imgIndex2].mix(self.imagesModels[imgIndex1], self.sliderOneValue,
                                                                 self.sliderTwoValue, Modes.phaseAndUniformMagnitude)

            elif componentOne == "real":
                if componentTwo == "imaginary":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,
                                                                 self.sliderTwoValue, Modes.realAndImaginary)

            elif componentOne == "imaginary":
                if componentTwo == "real":
                    mixOutput = self.imagesModels[imgIndex2].mix(self.imagesModels[imgIndex1], self.sliderTwoValue,
                                                                 self.sliderOneValue, Modes.realAndImaginary)

            elif componentOne == "uniform phase":
                if componentTwo == "magnitude":
                    mixOutput = self.imagesModels[imgIndex2].mix(self.imagesModels[imgIndex1], self.sliderTwoValue,
                                                                 self.sliderOneValue, Modes.magnitudeAndUniformPhase)
                elif componentOne == "uniform magnitude":
                    mixOutput = self.imagesModels[imgIndex2].mix(self.imagesModels[imgIndex1], self.sliderTwoValue,
                                                                 self.sliderOneValue,
                                                                 Modes.uniformPhaseAndUniformMagnitude)

            elif componentOne == "uniform magnitude":
                if componentTwo == "phase":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,
                                                                 self.sliderTwoValue, Modes.uniformMagnitudeAndPhase)
                elif componentTwo == "uniform phase":
                    mixOutput = self.imagesModels[imgIndex1].mix(self.imagesModels[imgIndex2], self.sliderOneValue,
                                                                 self.sliderTwoValue,
                                                                 Modes.uniformMagnitudeAndUniformPhase)

            if type(mixOutput) != type(...):
                logger.info(
                    f"Mixing {self.sliderOneValue} {componentOne} From Image{imgIndex1 + 1} And {self.sliderTwoValue} {componentTwo} From Image{imgIndex2 + 1}")
                self.displayImage(mixOutput, self.outputImages[outID])
                logger.info(f"Output{outID + 1} has been generated and displayed")

        except Exception as e:
            logger.error("Exception occurred", exc_info=True)

    def enableOutputCombos(self):
        for item in self.components:
            item.setEnabled(True)

    def adjustComboBox(self, comp1, comp2):
        """

        :param comp1: Selected component from 1st comboBox
        :param comp2: Selected component from 2nd comboBox
        :return:
        """
        self.componentCombos[1].clear()
        self.componentCombos[1].addItem("Choose Component")

        if comp1 == "magnitude":
            self.componentCombos[1].addItem("Phase")
            self.componentCombos[1].addItem("Uniform Phase")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "phase":
            self.componentCombos[1].addItem("Magnitude")
            self.componentCombos[1].addItem("Uniform Magnitude")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "real":
            self.componentCombos[1].addItem("Imaginary")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "imaginary":
            self.componentCombos[1].addItem("Real")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "uniform magnitude":
            self.componentCombos[1].addItem("Phase")
            self.componentCombos[1].addItem("Uniform Phase")
            self.componentCombos[1].setCurrentText(comp2)
        elif comp1 == "uniform phase":
            self.componentCombos[1].addItem("Magnitude")
            self.componentCombos[1].addItem("Uniform Magnitude")
            self.componentCombos[1].setCurrentText(comp2)

        logger.info(f"ComboBoxes has been adjusted")

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
