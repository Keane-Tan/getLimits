import os
import copy

from ROOT import TFile

import moduleStat.settings as settings

def mkdirp( path ):
    try:
        os.makedirs( path )
    except OSError:
        if not os.path.isdir( path ):
            raise

def produce_and_save_card(signal, channel, input_file_name, output_dir):
    card_output_directory = __get_output_directory(output_dir, signal)

    mkdirp(card_output_directory + "plots/")
    mkdirp(card_output_directory + "Fisher/")

    input_file_working_name = "stat_hists.root"
    os.system("cp -f {} {}".format(input_file_name, input_file_working_name))

    print("Opening file ", input_file_working_name)
    input_file = TFile.Open(input_file_working_name)
    input_file.cd()

    card = __initialize_card(input_file_working_name, input_file, channel, signal)
    hist = __get_histogram(channel, signal, input_file)

    for syst_name, syst_values in settings.syst.items():

        syst_type, processes, syst_range = syst_values

        if syst_type == "lnN":
            card = __add_log_normal_section(card, input_file, channel, signal, syst_name, processes,
                                            len(syst_values), syst_range)
        elif syst_type == "lnU":
            card = __add_log_uniform_section(card, syst_name, syst_range)
        elif syst_type == "shape":
            card = __add_shape_section(card, hist, channel, signal, syst_name, processes)

        card += "\n"

    card_output_path = "%s%s_%s.txt" % (card_output_directory, signal.replace(".", "p"), channel)
    card_file = open(card_output_path, 'w')
    card_file.write(card)
    card_file.close()


def __get_rate(channel, process, input_file):
    hist = __get_histogram(channel, process, input_file)
    n_passing_events = hist.Integral(1, hist.GetXaxis().GetNbins() - 1)
    return n_passing_events


def __get_histogram(channel, process, input_file):
    hist_name = channel + "/" + process
    print("Reading histogram: ", hist_name)
    hist = input_file.Get(hist_name)
    hist.SetDirectory(0)
    return hist


def __get_params(input_file, channel, signal):
    rates = {}
    proc_line = ""
    proc_number_line = ""
    rate_line = ""
    bin_string = ""

    for i, process in enumerate(settings.processes):
        rates[process] = __get_rate(channel, process, input_file)
        background_rate = rates[process]
        proc_number_line += "%-43s" % (i + 1)
        proc_line += "%-43s" % process
        rate_line += "%-43.10f" % background_rate

    bin_string += ("%-43s" % channel) * (len(settings.processes) + 1)

    rates["data_obs"] = __get_rate(channel, "data_obs", input_file)
    rates[signal] = __get_rate(channel, signal, input_file)

    return rates, bin_string, proc_line, proc_number_line, rate_line


def __initialize_card(input_file_name, input_file, channel, signal):

    rates, bin_string, proc_line, proc_number_line, rate_line = __get_params(input_file, channel, signal)

    print("hist_filename: ", input_file_name)
    print("===> Observed data: ", rates["data_obs"])

    card = "imax 1 number of channels \n"
    card += "jmax * number of backgrounds \n"
    card += "kmax * number of nuisance parameters\n"
    card += "-----------------------------------------------------------------------------------\n"
    card += "shapes   *      *   %s    $CHANNEL/$PROCESS    $CHANNEL/$PROCESS_$SYSTEMATIC\n" % input_file_name
    card += "shapes   data_obs      *   %s    $CHANNEL/$PROCESS\n" % input_file_name
    card += "-----------------------------------------------------------------------------------\n"
    card += "bin               %s\n" % channel
    card += "observation       %.6f\n" % (rates["data_obs"])
    card += "-----------------------------------------------------------------------------------\n"
    card += "bin                                     %-43s\n" % bin_string
    card += "process                                 %-43s%-43s\n" % (signal, proc_line)
    card += "process                                 %-43s%-43s\n" % ("0", proc_number_line)
    card += "rate                                    %-43.10f%-43s\n" % (rates[signal], rate_line)
    card += "-----------------------------------------------------------------------------------\n"

    return card


def __get_output_directory(base_path, signal_name):
    print("Output directory: ", base_path)

    card_output_directory = base_path + "/" + signal_name + "/"
    card_output_directory = card_output_directory.replace(",", "_").replace(".", "p").replace(" ", "")
    print("Card output directory: ", card_output_directory)

    return card_output_directory


def __add_log_normal_section(card, input_file, channel, signal, syst_name, processes, n_values, syst_range):

    card += "%-20s%-20s" % (syst_name, "lnN")

    if processes == "all" and n_values > 2:
        card += "%-20s" % syst_range * (len(settings.processes) + 1)
        return card

    if processes == "all":
        processes = copy.deepcopy(settings.processes)
        processes.append(signal)

    syst_name_up = "_" + syst_name + "UP"
    syst_name_down = "_" + syst_name + "DOWN"

    all_processes = settings.processes.extend("sig")

    for process in all_processes:
        if process in processes:

            rate = __get_rate(channel, process, input_file)

            if rate != 0.:
                rate_up = __get_rate(channel, process + syst_name_up, input_file)
                rate_down = __get_rate(channel, process + syst_name_down, input_file)
                syst_value = abs((rate_up - rate_down) / (2 * rate))
            else:
                syst_value = 1

            if 1. > syst_value > 0.:
                syst_value = syst_value + 1

            card += "{.10f}-20s".format(syst_value)
        else:
            card += "%-20s" % "-"

    return card


def __add_shape_section(card, input_hist, channel, signal, syst_name, processes):

    if "mcstat" not in syst_name:
        card += "%-20s     shape     " % syst_name

        all_processes = settings.processes.extend("sig")
        for p in all_processes:
            card += "1-20s" if p in processes else "--20s"

    else:
        for process in processes:
            if process.lower() == "sig":
                line = "1-20s"
                line += "--20s" * (len(settings.processes))
                process_name = signal
            else:
                line = "--20s"
                line_process = ["--20s" for _ in range(len(settings.processes))]

                if process in settings.processes:
                    index = settings.processes.index(process)
                    line_process[index] = "1"

                line_process = "         ".join(line_process)
                line += line_process
                process_name = process

            for i in range(input_hist.GetNbinsX()):
                syst_name = "mcstat_%s_%s_bin%d      " % (channel, process_name, i + 1)
                card += "%-20s   shape   " % syst_name
                card += line
                card += "\n"

    return card


def __add_log_uniform_section(card, syst_name, syst_range):
    card += "%-20s%-20s%-20s%-20s" % (syst_name, "lnU", "-", syst_range)
    return card
