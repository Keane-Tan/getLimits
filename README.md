# Introduction
This set of codes was modified from a set of codes that Jeremi Niedziela from ETH Zurich wrote.  

These scripts are meant to help produce Brazilian plots to show how much of the mediator mass we can exclude.

# Set up
We were using CMSSW_10_2_13 to run these codes.
```
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
```
If the CMSSW release above is not available, you may run `scram list CMSSW` to see which releases are available, and use the closest one.

Unfortunately, `CMSSW_10_2_13` were not available for slc7. So these codes may not work properly right out of the box.

While being in `src`, we also need to clone the `HiggsAnalysis-CombinedLimit` repository:
```
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
source env_standalone.sh 
make -j 8; make # second make fixes compilation error of first
```
Lastly, we clone the following repository into the `src` directory:
```
cd ../..
git clone git@github.com:Keane-Tan/getLimits.git
```

# 