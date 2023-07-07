
import time
import datetime
import os
from MD import MD
from SCD import SCD
from SCDS import SCDS
from DihedralAngle import DihedralAngle
from DihedralAngles import DihedralAngles
from DihedralAngleVertical import DihedralAngleVertical
from Tail import Tail
from Tails import Tails
from AreaPerLipid import AreaPerLipid
from AreaPerLipids import AreaPerLipids
from Temperature import Temperature

#nohup python2 -u md_analysis.py >> md_analysis1.log &
#tail -f 
#To kill you script, you can use ps -aux and kill commands 
#pid 27271

def processSingle(data_path, base, prmtop, processId):
    files = [base+'_{0:02d}.nc'.format(i) for i in range(1,11)]
    files = [os.path.join(data_path, f) for f in files if os.path.isfile(data_path+'/'+f)]
    if processId>=0 and processId<=9 :
        pass
    elif processId>=10 and processId<=19 :
        md = SCD(0, data_path, base, files, prmtop)
        if processId==10 :
            md.generate()
        elif processId==11:
            #resIDs = [200, 450, 750]
            resIDs = [750]
            c_name = 112
            md.plotScdVsFrame(resIDs, c_name)
        elif processId==12:
            md.plotScdGrid()
    elif processId>=20 and processId<=29 :
        md = DihedralAngle(0, data_path, base, files, prmtop)
        if processId==20 :
            md.generate()
        elif processId==21:
            pass
        elif processId==22:
            md.plotCount()
        elif processId==23:
            fIndex = 1999
            md.plotFrameMean(fIndex)
        elif processId==24:
            fIndex = 1999
            md.plotFrameCount(fIndex)
    elif processId>=30 and processId<=39 :
        md = Tail(0, data_path, base, files, prmtop)
        if processId==30 :
            md.generate()
        elif processId==31:
            pass
        elif processId==32:
            md.plot()
    elif processId>=40 and processId<=49 :
        md = AreaPerLipid(0, data_path, base, files, prmtop)
        if processId==40 :
            md.generate()
        elif processId==41:
            pass
        elif processId==42:
            md.plot()
    
def processGroup(processId):
    prmtop = 'DPPC_512.prmtop'
    data_path = os.path.join('/storage/scratch/syp0027', '20230116_DPPC512')
    #data_path = os.path.join('/storage/scratch/syp0027', '20230301_DPPC512')

    #category = ["010B", "025B", "050B", "075B", "100B", "125B", "150B", "175B", "200B", "225B", "250B", "275B", "300B"]
    #category = ["025B", "125B", "175B", "225B", "250B", "275B"]
    #category = ["100B", "150B", "200B", "300B"]
    #category = ["300B"]
    #category = ["06_300K_600B", "26_305K_600B", "36_310K_600B", "46_315K_600B", "56_320K_600B", "66_325K_600B", "76_330K_600B", "86_335K_600B"]
    #category = ["06_300K_300B", "26_305K_300B", "36_310K_300B", "46_315K_300B", "56_320K_300B", "66_325K_300B", "76_330K_300B", "86_335K_300B", "96_340K_300B"]
    category = ["76_330K_300B"]
    #category = ["86_335K_300B", "96_340K_300B"]
    #category = ["96_340K_300B"]
    for c in category:
        #base = "06_300K_{}".format(c)
        #base = "16_315K_{}".format(c)
        base = c
        print("processing {}".format(base))
        processSingle(data_path, base, prmtop, processId)

def plotGroup(processId):
    prmtop = 'DPPC_512.prmtop'
    #data_path_list = ["06_300K_001B", "26_305K_001B", "36_310K_001B", "46_315K_001B", "56_320K_001B", "66_325K_001B"]
    #data_path_list = ["06_300K_300B", "26_305K_300B", "36_310K_300B", "46_315K_300B", "56_320K_300B", "66_325K_300B", "76_330K_300B", "86_335K_300B"]
    data_path_list = ["06_300K_600B", "26_305K_600B", "36_310K_600B", "46_315K_600B", "56_320K_600B", "66_325K_600B", "76_330K_600B", "86_335K_600B"]
    #data_path_list = ["56_320K_300B", "66_325K_300B", "76_330K_300B"]
    plotSingle(data_path_list, prmtop, processId)

def plotSingle(data_path_list, prmtop, processId):
    file_list = []
    for data_path in data_path_list:
        base = data_path
        files = [base+'_{0:02d}.nc'.format(i) for i in range(1,11)]
        files = [os.path.join(data_path, f) for f in files if os.path.isfile(data_path+'/'+f)]
        file_list.append(files)

    if processId>=0 and processId<=9 :
        pass
    elif processId>=10 and processId<=19 :
        md = SCDS(0, data_path_list, file_list, prmtop)
        if processId==10 :
            pass
        elif processId==11:
            resIDs = [750]
            c_name = 112
            md.plotScdVsFrame(resIDs, c_name)
        elif processId==12:
            md.plotScdGrid()
        elif processId==16:
            fIndex = -1
            md.plotFrameMeanOverall(fIndex)
    elif processId>=20 and processId<=29 :
        md = DihedralAngles(0, data_path_list, file_list, prmtop)
        if processId==24:
            resIndex = 789
            md.plotResMeanEach(resIndex)
        elif processId==25:
            fIndex = 999
            md.plotFrameMeanEach(fIndex)
        elif processId==26:
            fIndex = -1
            md.plotFrameMeanOverall(fIndex)
        elif processId==27:
            md.plotCount()
    elif processId>=30 and processId<=39 :
        md = Tails(0, data_path_list, file_list, prmtop)
        if processId==30 :
            pass
        elif processId==31:
            itemIndex = 9
            md.plotItemSD(itemIndex)
        elif processId==32:
            itemIndex = 10
            md.plotItemSD(itemIndex)
        elif processId==35:
            #6-"Membrane Thickness", 7-"Tail Length", 8-"Tail Order Parameter", 9-"Tail Theta", 10-"Tail Phi"
            itemIndex = 7
            md.plotItem(itemIndex)
        elif processId==36:
            md.plot()
    elif processId>=40 and processId<=49 :
        md = AreaPerLipids(0, data_path_list, file_list, prmtop)
        if processId==46:
            md.plot()
        
def daPlotCount(temperature):
    prmtop = 'DPPC_512.prmtop'
    path1 = os.path.join('/storage/scratch/syp0027', '20230116_DPPC512')
    path2 = os.path.join('/storage/scratch/syp0027', '20230301_DPPC512')

    path_list = [path2, path1, path2]
    path_list1 = [path1, path2]
    base_list = []
    if temperature==300:
        base_list = ["06_300K_001B", "06_300K_300B", "06_300K_600B"]
    elif temperature==305:
        base_list = ["26_305K_001B", "26_305K_300B", "26_305K_600B"]
    elif temperature==310:
        base_list = ["36_310K_001B", "36_310K_300B", "36_310K_600B"]
    elif temperature==315:
        base_list = ["46_315K_001B", "46_315K_300B", "46_315K_600B"]
    elif temperature==320:
        base_list = ["56_320K_001B", "56_320K_300B", "56_320K_600B"]
    elif temperature==325:
        base_list = ["66_325K_001B", "66_325K_300B", "66_325K_600B"]
    elif temperature==330:
        base_list = ["76_330K_300B", "76_330K_600B"]
    elif temperature==335:
        base_list = ["86_335K_300B", "86_335K_600B"]
        
    file_list = []
    for index,  path in enumerate(path_list1):
        base = base_list[index]
        files = [base+'_{0:02d}.nc'.format(i) for i in range(1,11)]
        files = [os.path.join(path, f) for f in files if os.path.isfile(path+'/'+f)]
        file_list.append(files)

    md = DihedralAngleVertical(0, path_list, base_list, file_list, prmtop)
    md.plotCount()
        
        
def testSingle(processId):
    prmtop = 'DPPC_512.prmtop'
    data_path = os.path.join('/storage/scratch/syp0027', '20230301_DPPC512')
        
    base = "06_300K_001B"
    files = [base+'_{0:02d}.nc'.format(i) for i in range(1,11)]
    files = [os.path.join(data_path, f) for f in files if os.path.isfile(data_path+'/'+f)]
    print(files)
        
    if processId>=30 and processId<=39 :
        md = Tail(0, data_path, base, files, prmtop)
        if processId==30 :
            pass
        elif processId==31:
            sd = md.getDataTailThetaSD()
            print(sd.shape)
        elif processId==35:
            #6-"Membrane Thickness", 7-"Tail Length", 8-"Tail Order Parameter", 9-"Tail Theta", 10-"Tail Phi"
            itemIndex = 7
            md.plotItem(itemIndex)
        elif processId==36:
            md.plot()
            
def testTemperature(processId):
    #files = ["06_300K_001B_9_tails_plot.csv", "26_305K_300B_9_tails_plot.csv", "06_300K_600B_9_tails_plot.csv"]
    files = ["06_300K_001B_-1_SCD_plot.csv", "06_300K_300B_-1_SCD_plot.csv", "06_300K_600B_-1_SCD_plot.csv"]
    #files = ["06_300K_001B_11_areaPerlipid_plot.csv", "06_300K_300B_11_areaPerlipid_plot.csv", "06_300K_600B_11_areaPerlipid_plot.csv"]
    #files = ["06_300K_001B_11_dihedralAngle_plot.csv", "06_300K_300B_11_dihedralAngle_plot.csv", "06_300K_600B_11_dihedralAngle_plot.csv"]
    print(files)
        
    if processId>=30 and processId<=39 :
        md = Temperature(0, files)
        title = "Temperature vs SCD"
        xlabel = "Temperature (K)"
        ylabel = "SCD"
        md.parseFiles()
        md.plot(title, xlabel, ylabel)
        
        
        
    
def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time = time.time()
    ct = datetime.datetime.now()
    print("PROCESSING...")
    print("current time:-", ct)

    #processGroup(10)
    #plotGroup(16)
    #testSingle(31)
    testTemperature(31)
    #daPlotCount(335)

    end_time = time.time()
    seconds = end_time - start_time
    print("time of execution = {} seconds or hh:mm:ss {} ".format(seconds, format_seconds_to_hhmmss(seconds)))
    ct = datetime.datetime.now()
    print("current time:-", ct)