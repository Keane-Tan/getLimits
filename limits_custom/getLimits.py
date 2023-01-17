import os
#import paramiko
#from getpass import getpass

from moduleStat import limitsUtils

input_hists_path = "../stat_hist_MET_Keane_pT170_eta2p4_compFlorian.root"

dataDir = "0to5AK8Jets_Keane_pT170_eta2p4_compFlorian"
data_cards_path = "results/{}".format(dataDir)
limits_path = "data/{}".format(dataDir)
plots_path = "plots/{}".format(dataDir)

#reference_path = "data/without_tagger/"
reference_path = ""

prepare_cards  = 1
prepare_limits = 1
plot_limits    = 1

# years = ["2016", "2017", "2018", "Run2"]
years = ["Run2"]
#r_invs = [0.3, 0.5, 0.7]
r_invs = [0.3]


def prepare_combine_cards():
    command = "python createDatacards.py "
    command += " -i " + input_hists_path
    command += " -d " + data_cards_path

    os.system(command)

def run():
    #
    command = "cd /uscms/home/keanet/nobackup/SVJ/CMSSW_10_2_13/src;"
    command += "eval `scramv1 runtime -sh`;"
    command += "cd limits_custom;"

    #hist_name = input_hists_path.split("/")[-1]
    hist_name = input_hists_path

    print("copying the MET histograms")
    print("cp -f "+hist_name+" stat_hists.root;")
    command = "cp -f "+hist_name+" stat_hists.root;"
    command += "python3 runCombine.py -d " + data_cards_path + ";"

    os.system(command)


def collect_limits_data():
    os.system("mkdir -p data")

    for year in years:
        limitsUtils.get_limits(data_cards_path, "", year, limits_path)


def save_limits_plots():
    command_base = "python brazilPlot.py -y {} --rInv {}"
    command_base += " -i " + limits_path + " -o " + plots_path

    if reference_path != "":
        command_base += " --reference_path " + reference_path

    command_base += ";"
    command = ""

    for year in years:
        for r_inv in r_invs:
            command += command_base.format(year, r_inv)

    os.system(command)


def main():
    if prepare_cards:
        print("Preparing combine cards")
        prepare_combine_cards()

    if prepare_limits:
        print("Running commands (be patient, this will take a while...)")
        run()

        print("Collecting limits data")
        collect_limits_data()

    if plot_limits:
        print("Creating limits plots")
        save_limits_plots()


if __name__ == "__main__":
    main()
