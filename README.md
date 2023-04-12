# Introduction
This set of codes was modified from a set of codes that Jeremi Niedziela from ETH Zurich wrote.  

These scripts are meant to help produce Brazilian plots to show how much of the mediator mass we can exclude.

# Set up
We were using CMSSW_10_2_13 to run these codes.
```
wget https://raw.githubusercontent.com/Keane-Tan/getLimits/master/setup.sh
chmod +x setup.sh
source setup.sh
``` 

# Make Limit Plots
First, source all the required environments
```
cd CMSSW_10_2_13/src/
cmsenv
cd getLimits/HiggsAnalysis/CombinedLimit
source env_standalone.sh
```
Edit `getLimits.py` and `moduleStat/settings.py` in `limits_custom` (see sections below for how to edit these files), and then
```
cd $CMSSW_BASE/src/getLimits/limits_custom
python getLimits.py
```
The limit plots can be found in `limits_custom/plots/[dataDir]/`.

# How to Edit `getLimits.py`
- The variable `input_hists_path` is the path to the root file with all the histograms necessary for making the limit plots. An example is `/uscms_data/d3/keanet/SVJ/limitPlot/CMSSW_10_2_13/src/getLimits/stat_hist_MET_Keane_pT170_eta2p4_compFlorian.root`. If you look at this file using TBrowser, you will see how the histograms are organized and named. You should make sure the root files you are using to make the limit plots follow the same convention. Note that for this particular file, `data_obs`, `QCD`, and `Bkg` are the same.
- The variable `dataDir` is the name for the output folder that stores the results and plots.

# How to Edit `settings.py`
- Under `list of analysis channels`, you can specify the cuts that you want to use to make the histograms. By default, `SVJ0`, `SVJ1`, ..., `SVJ5P` are used. `SVJ0` means 0 tagged `SVJ` in the events, `SVJ1` means 1 tagged `SVJ` in the events, etc. 
- Under `list of signals`, you can specify the signals you want to use to make the limit plots. Make sure the histograms associated with those signals actually exist in the root file you use to make the limit plot (see section above).

# How to Get a Root File in the Right Format
As mentioned above, you will need to get the root file in the right format before you can use the code to make limit plots. `limits_custom/convertToFormat.py` can convert the histogram root files produced by https://github.com/cms-svj/t-channel_Analysis to the right format. 
