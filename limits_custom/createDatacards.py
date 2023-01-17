import argparse
import sys
import os

from ROOT import TFile, gDirectory

import moduleStat.settings as settings
import moduleStat.datacardUtils as datacardUtils

parser = argparse.ArgumentParser(description="Argument parser")
parser.add_argument('-i', '--input', dest='input_file_name', help='Path to the input file with histograms.')
parser.add_argument("-d", "--output_dir", dest="output_directory", help="Output directory to store data cards.")

args = parser.parse_args()
sys.argv.append('-b')

def mkdirp( path ):
    try:
        os.makedirs( path )
    except OSError:
        if not os.path.isdir( path ):
            raise

def get_years(input_file_name):

    print("Opening file ", input_file_name)
    input_file = TFile.Open(input_file_name)
    # input_file.cd("mt")

    years = [r.ReadObj().GetName()[-4:] for r in gDirectory.GetListOfKeys()]
    years = list(set(years))
    print(years)
    return years


def get_signals():
    signals = []

    for (m_z_prime, _, r_inv, _) in settings.signal_points:
        print("Creating datacards for m_z_prime = ", m_z_prime, "GeV, r_inv = ", r_inv)
        signal_name = "mZprime{}_rinv{}".format(m_z_prime, str(r_inv).replace(".", "p"))
        signals.append(signal_name)

    return signals


def main():
    signals = get_signals()

    input_file_name = args.input_file_name
    years = get_years(input_file_name)

    channels_names = settings.channels

    channel_and_year_names = []
    for year in years:
        ch_eff_years = [channel + '_' + year for channel in channels_names]
        channel_and_year_names = channel_and_year_names + ch_eff_years

    os.system("rm -fr "+args.output_directory)
    mkdirp(args.output_directory)
    for signal in signals:
        for channel in channel_and_year_names:
            datacardUtils.produce_and_save_card(signal, channel, input_file_name, args.output_directory)


if __name__ == "__main__":
    main()
