#!/bin/bash -e


# The setup instructions below are based on http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/

export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone git@github.com:Keane-Tan/getLimits.git
cd getLimits
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.2.0
scramv1 b clean; scramv1 b # always make a clean build
. env_standalone.sh
make -j 4
cd ../..
