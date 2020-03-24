## This is the abstract class that the students should implement
import pyqtgraph
from modesEnum import Modes
import numpy as np

class ImageModel(pyqtgraph.ImageView):

    """
    A class that represents the ImageModel
    """

    def __init__(self, imgPath: str, *args):
        super().__init__(*args)
        self.imgPath = imgPath
        ###
        # ALL the following properties should be assigned correctly after reading imgPath
        ###
        self.imgByte = None
        self.dft = None
        self.real = None
        self.imaginary = None
        self.magnitude = None
        self.phase = None
        self.uniformMagnitude = None
        self.uniformPhase = None

    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ration and
        return the magnitude of ifft of the mix
        return type ---> 2D numpy array

        please Add whatever functions realted to the image data in this file
        """
        ###
        # implement this function
        ###

        w1 = magnitudeOrRealRatio
        w2 = phaesOrImaginaryRatio
        mixInverse = None
        print(mode)

        ## case 1
        # 0.3 magn img2   ---> 0.7 magn img1
        # 0.7 phase img1  ---> 0.3 phase img2

        ## case 2
        # 0.7 real img1   ---> 0.3 real img2
        # 0.3 imag img2   ---> 0.7 imag img1

        # w1=0  w2=0
        # 0 magn img1     ---> 1 magn img2
        # 0 phase img2    ---> 1 phase img1
        if mode == Modes.magnitudeAndPhase:
            print("Mixing Magnitude and Phase")
            # mix1 = (w1 * M1 + (1 - w1) * M2) * exp((1-w2) * P1 + w2 * P2)
            M1 = self.magnitude
            M2 = imageToBeMixed.magnitude

            P1 = self.phase
            P2 = imageToBeMixed.phase

            magnitudeMix = w1*M1 + (1-w1)*M2
            phaseMix = w2*P1 + (1-w2)*P2

            combined = np.multiply(magnitudeMix, np.exp(1j * phaseMix))
            mixInverse = np.real(np.fft.ifft2(combined))

        elif mode == Modes.realAndImaginary:
            # mix2 = (w1 * R1 + (1 - w1) * R2) + j * ((1 - w2) * I1 + w2 * I2)
            print("Mixing Real and Imaginary")
            R1 = self.real
            R2 = imageToBeMixed.real

            I1 = self.imaginary
            I2 = imageToBeMixed.imaginary

            realMix = w1*R1 + (1-w1)*R2
            imaginaryMix = w2*I1 + (1-w2)*I2

            combined = realMix + imaginaryMix * 1j
            mixInverse = np.real(np.fft.ifft2(combined))

        return mixInverse


    def displayImage(self, data):
        """
        Display the given data
        :param data: the data array will be displayed
        :return:
        """
        imageShape = (500, 500)

        self.setImage(data)
        self.view.setRange(xRange=[0, imageShape[0]], yRange=[0, imageShape[1]], padding=0)
        self.ui.roiPlot.hide()
