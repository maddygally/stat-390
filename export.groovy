import qupath.lib.scripting.QP
import java.io.File

// get project
def project = getProject()

// define output directory 
def outputDir = '/Users/madelyngallagher/Desktop/stat 390/week3/qupath/output'

// ensure output directory exists
def outputDirFile = new File(outputDir)
if (!outputDirFile.exists()) {
    outputDirFile.mkdirs()  // Create the directory if it doesn't exist
}

// iterate through all images in the project
project.getImageList().each { entry ->
    // get image name
    def imageName = entry.getImageName()

    // extract patient ID from image name 
    def patientID = imageName.split(" ")[0] 

    // clean image name (remove spaces and special characters)
    def sanitizedImageName = imageName.replaceAll("[^a-zA-Z0-9]", "_")

    // create a directory for the patient if it doesn't exist
    def patientDir = new File(outputDir, patientID)
    if (!patientDir.exists()) {
        patientDir.mkdirs()  // create patient-specific directory if it doesn't exist
    }

    // get the actual source file path
    def sourceFilePath = entry.getEntryPath().toString() // convert path to string

    // construct the output file path, ensuring a valid filename
    def outputFilePath = "${patientDir}/${sanitizedImageName}.ome.tiff"  // export as OME-TIFF

    // export image using the actual file path
    def sourceFile = new File(sourceFilePath) // create a file object from the string path
    if (sourceFile.exists()) {
        def imageData = entry.readImageData() // read image data
        def server = imageData.getServer() // get ImageServer
        QP.writeImage(server, outputFilePath) // write the image data to the output path
        print("Exported: ${outputFilePath}")
    } else {
        print("Source file does not exist: ${sourceFilePath}")
    }
}
