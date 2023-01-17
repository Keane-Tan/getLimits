import argparse
import os

import moduleStat.settings as settings

dry_run = False

parser = argparse.ArgumentParser(description="Argument parser")
parser.add_argument('-d', '--dir', dest='cards_dir', help='Data-cards directory')

args = parser.parse_args()


def run_combine(command, log_file_name):
    command = command + " 2>&1 | tee " + log_file_name
    
    print("Running combine: ")
    print(command)
    
    if not dry_run:
        os.system(command)


def combine_cards(mass_z_prime, r_inv, year):
    input_path = "mZprime%s_rinv%s_*%s.txt" % (mass_z_prime, r_inv.replace(".", "p"), year)
    output_path = "combined_mZprime%s_rinv%s_%s.txt" % (mass_z_prime, r_inv.replace(".", "p"), year)
    cmd = "combineCards.py %s > %s" % (input_path, output_path)
    
    print("Running combineCards:")
    print(cmd)
    
    if not dry_run:
        os.system(cmd)


def run_single_point(m_z_prime, r_inv, base_path, year):
    print("Evaluate limit for mZprime = ", m_z_prime, " GeV, rinv = ", r_inv)

    starting_path = os.getcwd()
    
    working_path = "%s/mZprime%s_rinv%s" % (base_path, m_z_prime, r_inv.replace(".", "p"))
    os.chdir(working_path)

    input_file_name = "stat_hists.root"
    os.system("ln -s {} {}".format(starting_path + "/" + input_file_name, input_file_name))
    
    combine_cards(m_z_prime, r_inv, year)
    
    r_inv = r_inv.replace(".", "p")
    
    command = "combine -M AsymptoticLimits"
    command += " -n combined_mZprime" + m_z_prime + "_rinv" + r_inv + "_" + year
    command += " -m " + m_z_prime + " combined_mZprime" + m_z_prime + "_rinv" + r_inv + "_" + year
    command += ".txt"
    
    log_file_name = "asymptotic_mZprime" + m_z_prime + "_rinv" + r_inv + "_" + year + ".log"
    
    run_combine(command, log_file_name)
    
    os.chdir(starting_path)


def main():
    for (mass_z_prime, _, r_inv, _) in settings.signal_points:
        #for year in ["2016", "2017", "2018", "Run2"]:
        for year in ["Run2"]:
            run_single_point(mass_z_prime, r_inv, args.cards_dir, year)


if __name__ == "__main__":
    main()
