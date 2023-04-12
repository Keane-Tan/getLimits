#!/bin/bash -e

source /cvmfs/cms.cern.ch/cmsset_default.sh  
export SCRAM_ARCH=slc7_amd64_gcc700
eval `scramv1 project CMSSW CMSSW_10_2_13`
cd CMSSW_10_2_13/src/
git clone git@github.com:Keane-Tan/getLimits.git
cd getLimits
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
source env_standalone.sh 
make -j 8; make
cd ../..
