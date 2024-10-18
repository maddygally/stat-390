setImageType('BRIGHTFIELD_H_E');
setColorDeconvolutionStains('{"Name" : "H&E default", "Stain 1" : "Hematoxylin", "Values 1" : "0.65111 0.70119 0.29049", "Stain 2" : "Eosin", "Values 2" : "0.2159 0.8012 0.5581", "Background" : " 255 255 255"}');
resetSelection();
general_shape = createAnnotationsFromPixelClassifier("H&E_findshape", 0.0, 0.0)


//def roi_shape = general_shape.getROI()

//double width_shape = roi_shape.getBounds().getWidth()


// Define the parameters for the annotation
double x = 2.0 // X coordinate (in pixels)
double y = 20.0 // Y coordinate (in pixels)
double width = 300.0 // Width of the annotation (in pixels)
double height = 200.0 // Height of the annotation (in pixels)

// Create a rectangle ROI based on the specified parameters
def roi = new qupath.lib.roi.RectangleROI(x, y, width, height)

// Create a new annotation object
def annotation = new qupath.lib.objects.PathAnnotationObject(roi)

// Set the name and other properties if desired
annotation.setName("New Annotation")

// Add the annotation to the current image
addObject(annotation)

// Define the parameters for the annotation
double x2 = 20.0 // X coordinate (in pixels)
double y2 =600.0 // Y coordinate (in pixels)
double width2 = 300.0 // Width of the annotation (in pixels)
double height2 = 175.0 // Height of the annotation (in pixels)

// Create a rectangle ROI based on the specified parameters
def roi2 = new qupath.lib.roi.RectangleROI(x2, y2, width2, height2)

// Create a new annotation object
def annotation2 = new qupath.lib.objects.PathAnnotationObject(roi2)

// Set the name and other properties if desired
annotation2.setName("New Annotation2")


// Add the annotation to the current image
addObject(annotation2)

// Define the parameters for the annotation
double x3 = 150.0 // X coordinate (in pixels)
double y3 =300.0 // Y coordinate (in pixels)
double width3 = 125.0 // Width of the annotation (in pixels)
double height3 = 75.0 // Height of the annotation (in pixels)

// Create a rectangle ROI based on the specified parameters
def roi3 = new qupath.lib.roi.RectangleROI(x3, y3, width3, height3)

// Create a new annotation object
def annotation3 = new qupath.lib.objects.PathAnnotationObject(roi3)

// Set the name and other properties if desired
annotation3.setName("New Annotation3")


// Add the annotation to the current image
addObject(annotation3)

// export annotations to new images




