## CSC320 Winter 2018 
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
import cv2 as cv
from numpy.linalg import pinv

# If you wish to import any additional modules
# or define other utility functions,
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################


#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
    #
    # The class constructor
    #
    # When called, it creates a private dictionary object that acts as a container
    # for all input and all output images of the triangulation matting and compositing
    # algorithms. These images are initialized to None and populated/accessed by
    # calling the the readImage(), writeImage(), useTriangulationResults() methods.
    # See function run() in run.py for examples of their usage.
    #
    def __init__(self):
        self._images = {
            'backA': None,
            'backB': None,
            'compA': None,
            'compB': None,
            'colOut': None,
            'alphaOut': None,
            'backIn': None,
            'colIn': None,
            'alphaIn': None,
            'compOut': None,
        }

    # Return a dictionary containing the input arguments of the
    # triangulation matting algorithm, along with a brief explanation
    # and a default filename (or None)
    # This dictionary is used to create the command-line arguments
    # required by the algorithm. See the parseArguments() function
    # run.py for examples of its usage
    def mattingInput(self):
        return {
            'backA': {'msg': 'Image filename for Background A Color', 'default': None},
            'backB': {'msg': 'Image filename for Background B Color', 'default': None},
            'compA': {'msg': 'Image filename for Composite A Color', 'default': None},
            'compB': {'msg': 'Image filename for Composite B Color', 'default': None},
        }

    # Same as above, but for the output arguments
    def mattingOutput(self):
        return {
            'colOut': {'msg': 'Image filename for Object Color', 'default': ['color.tif']},
            'alphaOut': {'msg': 'Image filename for Object Alpha', 'default': ['alpha.tif']}
        }

    def compositingInput(self):
        return {
            'colIn': {'msg': 'Image filename for Object Color', 'default': None},
            'alphaIn': {'msg': 'Image filename for Object Alpha', 'default': None},
            'backIn': {'msg': 'Image filename for Background Color', 'default': None},
        }

    def compositingOutput(self):
        return {
            'compOut': {'msg': 'Image filename for Composite Color', 'default': ['comp.tif']},
        }

    # Copy the output of the triangulation matting algorithm (i.e., the
    # object Color and object Alpha images) to the images holding the input
    # to the compositing algorithm. This way we can do compositing right after
    # triangulation matting without having to save the object Color and object
    # Alpha images to disk. This routine is NOT used for partA of the assignment.
    def useTriangulationResults(self):
        if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
            self._images['colIn'] = self._images['colOut'].copy()
            self._images['alphaIn'] = self._images['alphaOut'].copy()

    # If you wish to create additional methods for the
    # Matting class, include them here

    #########################################
    ## PLACE YOUR CODE BETWEEN THESE LINES ##
    #########################################

    #########################################

    # Use OpenCV to read an image from a file and copy its contents to the
    # matting instance's private dictionary object. The key
    # specifies the image variable and should be one of the
    # strings in lines 54-63. See run() in run.py for examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # leave the matting instance's dictionary entry unaffected and return
    # False, along with an error message
    def readImage(self, fileName, key):
        success = False
        msg = 'Error: fail to execute imread()'
        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##

        #########################################
        img_temp = cv.imread(fileName)
        img_temp = img_temp.astype(np.float64)
        if type(img_temp) == None:
            success = False
            msg = "unable to read"
            return success, msg

        success = True
        msg = "read successfully"
        self._images[key] = img_temp
        #########################################
        return success, msg

    # Use OpenCV to write to a file an image that is contained in the
    # instance's private dictionary. The key specifies the which image
    # should be written and should be one of the strings in lines 54-63.
    # See run() in run.py for usage examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # return False, along with an error message
    def writeImage(self, fileName, key):
        success = False
        msg = "Error: fail to execute imwrite()"

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        if type(self._images[key]) == None:
            success = False
            msg = "fail to write"
            return success, msg
        img_temp = np.array(self._images[key])
        print(img_temp.shape)
        cv.imwrite(fileName, img_temp)


        success = True
        msg = "Successfully write into img"
        #########################################
        return success, msg

    # Method implementing the triangulation matting algorithm. The
    # method takes its inputs/outputs from the method's private dictionary
    # ojbect.
    def triangulationMatting(self):
        """
        success, errorMessage = triangulationMatting(self)

        Perform triangulation matting. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """
        success = False
        msg = 'Placeholder'
        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        comp1 = self._images['compA']
        comp2 = self._images['compB']

        back1 = self._images['backA']
        back2 = self._images['backB']
        if (comp1.shape != comp2.shape) or (back1.shape != back2.shape) or comp1.shape != back1.shape or comp2.shape!=back2.shape:
            success = False
            msg = "not same size"
            return success, msg


        colOut1 = []
        alphaOut1 = []

        for i in range(comp1.shape[0]):
            colOut1.append([])
            alphaOut1.append([])
            for j in range(comp1.shape[1]):
                A = np.array([[1, 0, 0, -back1[i][j][0]],
                              [0, 1, 0, -back1[i][j][1]],
                              [0, 0, 1, -back1[i][j][2]],
                              [1, 0, 0, -back2[i][j][0]],
                              [0, 1, 0, -back2[i][j][1]],
                              [0, 0, 1, -back2[i][j][2]]])
                B = np.array([[comp1[i][j][0] - back1[i][j][0]],
                              [comp1[i][j][1] - back1[i][j][1]],
                              [comp1[i][j][2] - back1[i][j][2]],
                              [comp2[i][j][0] - back2[i][j][0]],
                              [comp2[i][j][1] - back2[i][j][1]],
                              [comp2[i][j][2] - back2[i][j][2]]])

                vector = np.matmul(pinv(A), B)


                alphaVec = vector[3][0]
                colVec = [vector[0,0], vector[1,0], vector[2,0]]

                colOut1[i].append(colVec)
                alphaOut1[i].append(alphaVec * 255)
        self._images['colOut'] = colOut1
        self._images['alphaOut'] = alphaOut1

        success = True
        msg = "complete"
        #########################################

        return success, msg

    def createComposite(self):
        """
        success, errorMessage = createComposite(self)

        Perform compositing. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################'
        cIn = self._images['colIn']
        bIn = self._images['backIn']
        aIn = self._images['alphaIn']

        self._images['compOut'] = (cIn / 255 + bIn / 255 - (aIn / 255) * (bIn / 255)) * 255
        success = True
        msg = 'complete'
        #########################################

        return success, msg