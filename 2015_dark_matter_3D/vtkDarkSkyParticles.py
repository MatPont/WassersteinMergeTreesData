# From https://github.com/CreativeCodingLab/DarkSkyVis (slightly modified)

# import yt
import vtk
import time
import numpy as np
import random as rd
import sdfpy as sdf
#from vtkDarkSkyUtilities import l2a
import os
import sys

global ren
global iren
global renWin
global frame

def l2a(l):
    return np.array(l)

class vtkTimerCallback():
    def __init__(self, actor, camera):
        self.timer_count = 0
        self.actor = actor
        self.camera = camera

    def execute(self, obj, event):
        if self.timer_count < 800:
            self.camera.Zoom(1.005)
            try:
                self.actor.RotateWXYZ(1.001, 0.01, 0.8, 0.0)
            except Exception:
                pass
        elif self.timer_count >= 800 and self.timer_count <= 1600:
            self.camera.Zoom(0.995)
            try:
                self.actor.RotateWXYZ(0.999, 0.01, 0.8, 0.0)
            except Exception:
                pass
        else:
            self.timer_count = 0
        # print self.timer_count
        # self.actor.SetPosition(self.timer_count, self.timer_count, 0)
        iren = obj
        iren.GetRenderWindow().Render()
        self.timer_count += 1


class vtkDarkSkyParticles(object):
    """docstring for VtkDarkSky"""
    def __init__(self, filename, key, useSDF=True, cMpc=False):
        super(vtkDarkSkyParticles, self).__init__()
        self.useSDF = useSDF
        self.isCoMoving = cMpc
        self.filename = filename
        self.start = time.clock()
        self.vtkPolyData = vtk.vtkPolyData()
        # Only do one of these
        # ======================
        if self.useSDF:
            self.initSDF()
        else:
            self.initYT()
        # =======================
        self.initVTK(key)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(self.__setMapper())
        self.write(filename)

    def initSDF(self):
        self.sdfParticles = sdf.load_sdf(self.filename)
        self.sdfHeader = self.sdfParticles.parameters
        self.sdfPosition = self.sdfGetXYZ()
        self.sdfVelocity = self.sdfGetUVW()
        self.sdfMagnitude = self.sdfGetMagnitude()
        self.sdfAcceleration = self.sdfGetAcceleration()
        self.sdfPhi = self.sdfParticles['phi']
        self.sdfIdent = self.sdfParticles['ident']

    def initYT(self):
        print "Extracting YT data"
        self.ytDataSource = yt.load(self.filename)
        self.ytAllData = self.ytDataSource.all_data()
        self.ytPhi = self.__ytGetDarkMatterPaticleData(0)
        self.ytIndex = self.__ytGetDarkMatterPaticleData(1)
        self.ytPosition = self.__ytGetDarkMatterPaticleData(2)
        self.ytVelocity = self.__ytGetDarkMatterPaticleData(3)
        self.ytMagnitude = self.__ytGetDarkMatterPaticleData(4)

    def initVTK(self, key):
        print "initializing VTK objects"
        start = time.clock()
        self.__setMinMaxRange(key)
        self.__normalize(key)
        self.resetPoints()
        for i in xrange(self.sdfIdent.size):
            self.addPoints(i, key)
            if i % 500000 == 0:
                print "at {} points! {} secs".format(i, time.clock() - start)
        print "total runtime was: {}".format(time.clock() - start)

    def resetPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkScalars = vtk.vtkDoubleArray()
        self.vtkScalars.SetName("DarkMatter_Phi")

        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkScalars)
        self.vtkPolyData.GetPointData().SetActiveScalars('DarkMatter_Phi')

    def addPoints(self, index, key):
        x, y, z = self.sdfPosition[index]

        pID = self.vtkPoints.InsertNextPoint(x, y, z)
        self.vtkCells.InsertNextCell(1)
        self.vtkCells.InsertCellPoint(pID)

        v = self.__scalar(index, key)
        self.vtkScalars.InsertNextValue(v)

        self.vtkPoints.Modified()
        self.vtkScalars.Modified()
        self.vtkCells.Modified()

    def write(self, fn):
        writer = vtk.vtkXMLPolyDataWriter()
        writer.SetFileName(fn+".vtp")
        writer.SetInputData(self.vtkPolyData)
        writer.Write()

    def histo(self, key, bins=255, dRange=None):
        import matplotlib.pyplot as plt
        hist, counts = np.histogram(self.ytPhi, bins=bins, range=dRange)
        # hist, bins = np.histogram(niiData, bins=100)
        width = 0.9 * (counts[1] - counts[0])
        center = (counts[:-1] + counts[1:]) / 2

        fig, ax = plt.subplots()
        ax.bar(center, hist, align='center', width=width)
        fig.savefig("DarkSky.png")

        plt.bar(center, hist, align='center', width=width)
        plt.show()
        return hist, counts

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #                   Private Methdods
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def sdfGetXYZ(self):
        x = self.sdfParticles['x']
        y = self.sdfParticles['y']
        z = self.sdfParticles['z']
        xyz = np.dstack((x, y, z))[0]
        if self.isCoMoving:
            return self.__toCoMoving(xyz)
        else:
            return xyz

    def sdfGetUVW(self):
        u = self.sdfParticles['vx']
        v = self.sdfParticles['vy']
        w = self.sdfParticles['vz']
        return np.dstack((u, v, w))[0]

    def sdfGetMagnitude(self):
        return abs(np.sqrt(self.sdfVelocity[:, 0]**2 +
                           self.sdfVelocity[:, 1]**2 +
                           self.sdfVelocity[:, 2]**+2))
    def sdfGetAcceleration(self):
        a = self.sdfParticles['ax']
        b = self.sdfParticles['ay']
        c = self.sdfParticles['az']
        return np.dstack((a,b,c))[0]

    def __toCoMoving(self, proper):
        h_100 = self.sdfHeader['h_100']
        width = self.sdfHeader['L0']
        cosmo_a = self.sdfHeader['a']
        kpc_to_Mpc = 1./1000
        return (proper + width/2.) * h_100 * kpc_to_Mpc / cosmo_a

    def __setMinMaxRange(self, key=None):
        if key is 'phi':
            self.dMin = self.sdfPhi.min()
            self.dMax = self.sdfPhi.max()
        elif key is 'index':
            self.dMin = self.sdfIdent.min()
            self.dMax = self.sdfIdent.max()
        elif key is 'mag':
            self.dMin = self.sdfMagnitude.min()
            self.dMax = self.sdfMagnitude.max()
        elif key is 'velx':
            self.dMin = self.sdfVelocity[:, 0].min()
            self.dMax = self.sdfVelocity[:, 0].max()
        elif key is 'vely':
            self.dMin = self.sdfVelocity[:, 1].min()
            self.dMax = self.sdfVelocity[:, 1].max()
        elif key is 'velz':
            self.dMin = self.sdfVelocity[:, 2].min()
            self.dMax = self.sdfVelocity[:, 2].max()
        else:
            self.dMin = 0.0
            self.dMax = 1.0
        print "Min/Max values are: {}/{}".format(self.dMin, self.dMax)

    def __scalar(self, index, key):
        if key is 'phi':
            return self.sdfPhi[index]
        elif key is 'index':
            return self.sdfIdent[index]
        elif key is 'mag':
            return self.sdfMagnitude[index]
        elif key is 'velx':
            return self.sdfVelocity[index, 0]
        elif key is 'vely':
            return self.sdfVelocity[index, 1]
        elif key is 'velz':
            return self.sdfVelocity[index, 2]
        else:
            return rd.random()

    def __normalize(self, key):
        if self.dMin < 0.0:
            self.factor = max([self.dMax, abs(self.dMin)])
            if key is 'phi':
                self.sdfPhi = self.sdfPhi/self.factor
            elif key is 'index':
                self.sdfIdent = self.sdfIdent/self.factor
            elif key is 'mag':
                self.sdfMagnitude/self.factor
            elif key is 'velx':
                self.sdfVelocity[:, 0] = abs(self.sdfVelocity[:, 0])/self.factor
            elif key is 'vely':
                self.sdfVelocity[:, 1] = abs(self.sdfVelocity[:, 1]/self.factor)
            elif key is 'velz':
                self.sdfVelocity[:, 2] = abs(self.sdfVelocity[:, 2])/self.factor
            self.__setMinMaxRange(key)
        else:
            pass

    def __ytGetDarkMatterPaticleData(self, index):
        registry = [('dark_matter', 'particle_phi'),
                    ('dark_matter', 'particle_index'),
                    ('dark_matter', 'particle_position'),
                    ('dark_matter', 'particle_velocity'),
                    ('dark_matter', 'particle_velocity_magnitude')]
        return self.ytAllData[registry[index]]

    def __setMapper(self):
        print "Creating vtkPolyDataMapper"
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(self.dMin, self.dMax)
        mapper.SetScalarVisibility(1)
        return mapper


def print_camera_settings():
    global ren
    # ---------------------------------------------------------------
    # Print out the current settings of the camera
    # ---------------------------------------------------------------
    camera = ren.GetActiveCamera()
    print "Camera settings:"
    print "  * position:        %s" % (camera.GetPosition(),)
    print "  * focal point:     %s" % (camera.GetFocalPoint(),)
    print "  * up vector:       %s" % (camera.GetViewUp(),)
    print "  * clipping range:  %s" % (camera.GetViewUp(),)


def Smile_For_the_Camera():
    global frame
    global ren
    global renWin
    file_name = "darkSky" + str(frame).zfill(5) + ".png"
    image = vtk.vtkWindowToImageFilter()
    image.SetInput(renWin)
    png_writer = vtk.vtkPNGWriter()
    png_writer.SetInputConnection(image.GetOutputPort())
    png_writer.SetFileName(file_name)
    renWin.Render()
    png_writer.Write()
    frame += 1
    print file_name + " has been successfully exported"


def key_pressed_callback(obj, event):
    # ---------------------------------------------------------------
    # Attach actions to specific keys
    # ---------------------------------------------------------------
    key = obj.GetKeySym()
    camera = ren.GetActiveCamera()

    if key == "c":
        print_camera_settings()
    if key == "s":
        Smile_For_the_Camera()
    if key == "i":
        camera.Zoom(1.5)
    if key == "o":
        camera.Zoom(0.95)


if __name__ == '__main__':

    frame = 0
    # DarkSky
    start = time.clock()
    prepath = ""
    fn = prepath+sys.argv[1]
    if not os.path.isfile(fn):
        print "not a valid fileName"
        exit()
    dk = vtkDarkSkyParticles(fn, 'phi')

    exit()

    # Renderer
    # Create the Renderer
    ren = vtk.vtkRenderer()
    ren.AddActor(dk.vtkActor)
    ren.SetBackground(0.0, 0.0, 0.0)  # Set background to white
    ren.ResetCamera()

    # Create the RendererWindow
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(2560, 1600)
    renWin.AddRenderer(ren)

    # Interactor
    iren = vtk.vtkRenderWindowInteractor()
    iren.AddObserver("KeyPressEvent", key_pressed_callback)
    iren.SetRenderWindow(renWin)

    # Begin Interaction
    print "We drawing stuffs! {}".format(time.clock() - start)
    renWin.Render()
    iren.Initialize()

    # Sign up to receive TimerEvent
    cb = vtkTimerCallback(dk.vtkActor, ren.GetActiveCamera())
    iren.AddObserver('TimerEvent', cb.execute)
    timerId = iren.CreateRepeatingTimer(100)

    iren.Start()
