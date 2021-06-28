# state file generated using paraview version 5.7.0

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# trace generated using paraview version 5.7.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
import sys
import os

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

def generate(fileName, metaData):
    fileName1, fileName2, fileName3 = fileName[0], fileName[1], fileName[2]

    # create a new 'Image Reader'
    tS21z_X_R2_007500 = ImageReader(FileNames=[fileName1])
    tS21z_X_R2_007500.DataScalarType = 'float'
    tS21z_X_R2_007500.DataSpacing = [800.0, 800.0, 800.0]
    tS21z_X_R2_007500.DataExtent = [0, 749, 0, 374, 0, 99]

    # create a new 'Image Reader'
    tS21z_Y_R2_007500 = ImageReader(FileNames=[fileName2])
    tS21z_Y_R2_007500.DataScalarType = 'float'
    tS21z_Y_R2_007500.DataSpacing = [800.0, 800.0, 800.0]
    tS21z_Y_R2_007500.DataExtent = [0, 749, 0, 374, 0, 99]

    # create a new 'Image Reader'
    tS21z_Z_R2_007500 = ImageReader(FileNames=[fileName3])
    tS21z_Z_R2_007500.DataScalarType = 'float'
    tS21z_Z_R2_007500.DataSpacing = [800.0, 800.0, 800.0]
    tS21z_Z_R2_007500.DataExtent = [0, 749, 0, 374, 0, 99]

    # create a new 'Append Attributes'
    appendAttributes1 = AppendAttributes(Input=[tS21z_X_R2_007500, tS21z_Y_R2_007500, tS21z_Z_R2_007500])

    # create a new 'Calculator'
    calculator1 = Calculator(Input=appendAttributes1)
    calculator1.ResultArrayName = 'Vector'
    calculator1.Function = 'ImageFile*iHat+ImageFile_input_1*jHat+ImageFile_input_2*kHat'

    # create a new 'Calculator'
    calculator2 = Calculator(Input=calculator1)
    calculator2.ResultArrayName = 'VectorMag'
    calculator2.Function = 'mag(Vector)'

    # create a new 'Resample To Image'
    resampleToImage1 = ResampleToImage(Input=calculator2)
    resampleToImage1.SamplingDimensions = [375, 188, 50]
    #resampleToImage1.SamplingBounds = [0.0, 599200.0, 0.0, 299200.0, 0.0, 79200.0]
    resampleToImage1.UseInputBounds = 1

    # create a new 'TTK PersistenceDiagram'
    tTKPersistenceDiagram1 = TTKPersistenceDiagram(Input=resampleToImage1)
    tTKPersistenceDiagram1.ScalarField = 'VectorMag'
    tTKPersistenceDiagram1.InputOffsetField = 'VectorMag'

    # create a new 'Threshold'
    threshold1 = Threshold(Input=tTKPersistenceDiagram1)
    threshold1.Scalars = ['CELLS', 'Persistence']
    threshold1.ThresholdRange = [0.0025, 9999999.]

    # create a new 'TTK TopologicalSimplification'
    tTKTopologicalSimplification1 = TTKTopologicalSimplification(Domain=resampleToImage1,
        Constraints=threshold1)
    tTKTopologicalSimplification1.ScalarField = 'VectorMag'
    tTKTopologicalSimplification1.InputOffsetField = 'VectorMag'
    tTKTopologicalSimplification1.Vertexidentifierfield = 'CriticalType'
    tTKTopologicalSimplification1.OutputOffsetScalarField = ''

    # create a new 'TTK ArrayEditor'
    tTKArrayEditor1 = TTKArrayEditor(Target=tTKTopologicalSimplification1, Source=None)
    tTKArrayEditor1.TargetAttribute = 'Field Data'
    #tTKArrayEditor1.DataString = """ClusterID, 0
#myTest, 54"""
    metaDataString = ''.join([str(k)+","+str(metaData[k])+"\n" for k in metaData.keys()])
    tTKArrayEditor1.DataString = metaDataString
    tTKArrayEditor1.TargetArray = ['POINTS', 'VectorMag']
    
    res = tTKArrayEditor1
    
    return res

def processDataset():
  string = "TS21z_X"
  allFiles = [a for a in os.listdir("./nonProcessed/") if a[:len(string)] == string]
  allFiles.sort()
  
  timeSteps = ["002700", "002900", "003100", "003300", "007700", "007900", "008100", "008300", "011700", "011900", "012100", "012300"]
  clusterID = [0] * 4 + [1] * 4 + [2] * 4
  
  for i, myFile in enumerate(allFiles):
    print(i, "/", len(allFiles), ":", myFile)
    tFile = "./nonProcessed/"+myFile
    myFiles = [tFile, tFile.replace('X', 'Y'), tFile.replace('X', 'Z')]
    
    metaData = {}
    metaData["TimeStep"] = timeSteps[i]
    metaData["ClusterID"] = clusterID[i]
    metaData["Dim."] = "3D"
    metaData["Generation"] = "Simulation"
    
    res = generate(myFiles, metaData)
    
    ext = ".vtu"
    outFileName = "./processed/"+myFile.replace('X', 'XYZ')+ext
    XMLUnstructuredGridWriter(FileName=outFileName, Input=res).UpdatePipeline()
    
# ----------------------------------------------------------------

if __name__ == "__main__":
    processDataset()

