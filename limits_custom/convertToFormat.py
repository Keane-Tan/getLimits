import ROOT as rt
import numpy as np

rootFile = rt.TFile("../stat_hist_MET_Keane_pT170_eta2p4_compFlorian.root","recreate")

histFileDir = "/uscms/home/keanet/nobackup/SVJ/t-channel_Analysis/condor/testHadd_full_pT170_eta2p4_compFlorian"
pre = "trg_flmetfilter_0l"
var = "h_met_{}".format(pre)
njetList = ["0FJ","1FJ","2FJ","3FJ","4FJ","5PFJ"]
dirs = ["SVJ0_Run2","SVJ1_Run2","SVJ2_Run2","SVJ3_Run2","SVJ4_Run2","SVJ5P_Run2"]
# njetList = ["0SVJ","1SVJ","2SVJ","3SVJ","4SVJ"]
# dirs = ["SVJ0_Run2","SVJ1_Run2","SVJ2_Run2","SVJ3_Run2","SVJ4_Run2"]
mMeds = [500,600,800,1000,1500,2000,3000,4000]

for i in range(len(dirs)):
    d = dirs[i]
    jetBin = njetList[i]
    SVJ_Run2 = rootFile.mkdir(d)
    # bkg
    fileName = "{}/2018_QCD.root".format(histFileDir)
    histFile = rt.TFile.Open(fileName,"READ")
    METHist = histFile.Get(var + "_{}".format(jetBin))
    print(var + "_{}".format(jetBin))
    METHist.Rebin(5)
    METHist.SetNameTitle("QCD","MET_pt")
    METHist.GetYaxis().SetTitle("")
    METHist.GetXaxis().SetTitle("MET_pt")
    SVJ_Run2.cd()
    METHist.Write()
    METHist.SetNameTitle("Bkg","MET_pt")
    METHist.Write()
    METHist.SetNameTitle("data_obs","MET_pt")
    METHist.Write()
    # signals
    for mMed in mMeds:
        fileName = "{}/2018_mMed-{}_mDark-20_rinv-0p3_alpha-peak_yukawa-1.root".format(histFileDir,mMed)
        histFile = rt.TFile.Open(fileName,"READ")
        METHist = histFile.Get(var + "_{}".format(jetBin))
        METHist.Rebin(5)
        METHist.SetNameTitle("mZprime{}_rinv0p3".format(mMed),"MET_pt")
        METHist.GetYaxis().SetTitle("")
        METHist.GetXaxis().SetTitle("MET_pt")
        SVJ_Run2.cd()
        METHist.Write()
rootFile.Close()
