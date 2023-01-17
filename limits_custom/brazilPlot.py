import os
from array import array
import optparse

import ROOT

from moduleStat.limitsUtils import Limit
from moduleStat.samplesUtils import tch_cross_sections as SVJ_cross_sections

def set_root_options():
    ROOT.gROOT.Reset()
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch()        # don"t pop up canvases
    ROOT.TH1.AddDirectory(False)


def get_filename_and_channel(options):
    r_inv = ""

    if options.r_inv != "":
        r_inv = "_rinv{}".format(options.r_inv)

    if options.channel != "":
        filename = options.input_path+"/limit%s_%s_%s.txt" % (r_inv, options.channel, options.year)
        channel = "%s" % options.channel
    else:
        filename = options.input_path+"/limit%s_%s.txt" % (r_inv, options.year)
        channel = ""

    return filename, channel


def read_file(options):

    file_name, channel = get_filename_and_channel(options)
    reference_file_name = None

    if options.reference_path and options.reference_path != "":
        reference_file_name = file_name.replace(options.input_path, options.reference_path)

    if channel != "":
        channel = "_" + channel

    read_limits = []

    print("Reading ", file_name)
    with open(file_name) as input_file:

        first_line = True

        for line in input_file.readlines():

            if line.strip() == "":
                continue

            l_split = line.split()

            if first_line:
                read_limits = [Limit() for i in range(len(l_split)-1)]
                first_line = False

            for label, arg_name in Limit.label_to_attr_name.items():
                if line.startswith(label + channel):
                    for i in range(0, len(l_split)-1):
                        setattr(read_limits[i], arg_name, float(l_split[i+1]))

    if reference_file_name:
        with open(reference_file_name) as input_file:

            for line in input_file.readlines():

                if line.strip() == "":
                    continue

                l_split = line.split()

                label, arg_name = "y_vals", "reference"
                if line.startswith(label + channel):
                    for i in range(0, len(l_split) - 1):
                        setattr(read_limits[i], arg_name, float(l_split[i + 1]))

    return read_limits


def get_input_arguments():
    parser = optparse.OptionParser("usage: %prog --method method")
    parser.add_option("-r", "--ratio", dest="ratio", action="store_true", default=False)
    parser.add_option("-y", "--year", dest="year", type="string", default = "all", help="Run a single method (Run2, 2016, 2017, 2016_2017)")
    parser.add_option("-v", "--variable", dest="variable", type="string", default = "mZprime", help="Plot limit against variable v (mZPrime, mDark, rinv, alpha)")
    parser.add_option("-u", "--unblind", dest="unblind", action="store_true", default=False)
    parser.add_option("-c", "--channel", dest="channel", type="string", default="", help="Indicate channels of interest. Default is all")
    parser.add_option("-o", "--output_path", dest="output_path", type="string", help="Output path")
    parser.add_option("--reference_path", dest="reference_path", type="string", help="Reference limits path")
    parser.add_option("-i", "--input_path", dest="input_path", type="string", help="Input path")
    parser.add_option("", "--rInv", dest="r_inv", type="string", default="", help="For which r_inv should limits be drawn")
    (opt, args) = parser.parse_args()
    return opt


def draw_labels(year):
    lumi_per_year = {
        "2016": "35.92 fb^{-1} (13 TeV)",
        "2017": "41.53 fb^{-1} (13 TeV)",
        "2018": "59.8 fb^{-1} (13 TeV)",
        "Run2": "137.19 fb^{-1} (13 TeV)",
    }

    label_lumi = ROOT.TLatex()
    label_cms = ROOT.TLatex()
    label_preliminary = ROOT.TLatex()

    label_lumi.SetNDC()
    label_cms.SetNDC()
    label_preliminary.SetNDC()

    label_lumi.SetTextFont(42)
    label_preliminary.SetTextFont(52)

    label_lumi.SetTextAlign(31)  # align right
    label_cms.SetTextAlign(11)  # align left
    label_preliminary.SetTextAlign(11)  # align left

    top_margin = ROOT.gPad.GetTopMargin()
    right_margin = ROOT.gPad.GetRightMargin()

    label_lumi.SetTextSize(0.33 * top_margin)
    label_cms.SetTextSize(0.48 * top_margin)
    label_preliminary.SetTextSize(0.39 * top_margin)

    label_text_offset = 0.2

    label_lumi.DrawLatex(1 - right_margin, 1 - top_margin + label_text_offset * top_margin, lumi_per_year[year])
    # label_cms.DrawLatex(0.15, 0.83, "CMS")
    # label_preliminary.DrawLatex(0.17, 1 - top_margin + label_text_offset * top_margin, "Work in progress")


def get_graph(x, y):
    return ROOT.TGraph(len(x), array("f", x), array("f", y))


def get_graph_asymm_errors(x, y, x_up, x_down, y_up, y_down):
    return ROOT.TGraphAsymmErrors(len(x), array("f", x), array("f", y), array("f", x_up), array("f", x_down), array("f", y_up), array("f", y_down))


def main():

    plot_ref = False

    options = get_input_arguments()
    unblind = options.unblind
    theo = not options.ratio

    limits = read_file(options)

    print("Loaded limits:")
    for limit in limits:
        limit.Print()

    expected_values = []
    observed_values = []
    reference_values = []
    theory_xsec_values = []

    y_bars_u1 = []
    y_bars_u2 = []
    y_bars_d1 = []
    y_bars_d2 = []

    for limit in limits:
        expected_values.append(limit.value)
        observed_values.append(limit.observed)
        reference_values.append(limit.reference)

        theory_xsec_values.append(SVJ_cross_sections[limit.mass])

        y_bars_u1.append(limit.points_up_1_sigma - limit.value)
        y_bars_u2.append(limit.points_up_2_sigma - limit.value)
        y_bars_d1.append(limit.value - limit.points_down_1_sigma)
        y_bars_d2.append(limit.value - limit.points_down_2_sigma)

        if theo:
            expected_values[-1] = expected_values[-1] * SVJ_cross_sections[limit.mass]
            observed_values[-1] = observed_values[-1] * SVJ_cross_sections[limit.mass]
            reference_values[-1] = reference_values[-1] * SVJ_cross_sections[limit.mass]

            y_bars_u1[-1] = y_bars_u1[-1] * SVJ_cross_sections[limit.mass]
            y_bars_u2[-1] = y_bars_u2[-1] * SVJ_cross_sections[limit.mass]
            y_bars_d1[-1] = y_bars_d1[-1] * SVJ_cross_sections[limit.mass]
            y_bars_d2[-1] = y_bars_d2[-1] * SVJ_cross_sections[limit.mass]

    x_values = [l.mass for l in limits]
    x_bars_1 = [0 for l in limits]
    x_bars_2 = [0 for l in limits]

    median = get_graph(x_values, expected_values)
    median.SetLineWidth(2)
    median.SetLineStyle(2)
    median.SetLineColor(ROOT.kBlue)
    median.SetFillColor(0)
    median.GetXaxis().SetRangeUser(110, 150)

    reference = get_graph(x_values, reference_values)
    reference.SetLineWidth(2)
    reference.SetLineStyle(2)
    reference.SetLineColor(ROOT.kCyan+1)
    reference.SetFillColor(0)
    reference.GetXaxis().SetRangeUser(110, 150)

    obs = get_graph(x_values, observed_values)
    obs.SetLineWidth(2)
    obs.SetLineStyle(1)
    obs.SetLineColor(ROOT.kBlue)
    obs.SetFillColor(0)
    obs.GetXaxis().SetRangeUser(110, 150)

    theory = get_graph(x_values, theory_xsec_values)
    theory.SetLineWidth(2)
    theory.SetLineStyle(1)
    theory.SetLineColor(ROOT.kRed)
    theory.SetFillColor(ROOT.kWhite)

    band_1sigma = get_graph_asymm_errors(x_values, expected_values, x_bars_1, x_bars_2, y_bars_d1, y_bars_u1)
    band_1sigma.SetFillColor(ROOT.kGreen + 1)
    band_1sigma.SetLineColor(ROOT.kGreen + 1)
    band_1sigma.SetMarkerColor(ROOT.kGreen + 1)

    band_2sigma = get_graph_asymm_errors(x_values, expected_values, x_bars_1, x_bars_2, y_bars_d2, y_bars_u2)
    band_2sigma.SetTitle("")
    band_2sigma.SetFillColor(ROOT.kOrange)
    band_2sigma.SetLineColor(ROOT.kOrange)
    band_2sigma.SetMarkerColor(ROOT.kOrange)
    #band_2sigma.GetXaxis().SetTitle("#it{m}_{Z'} [GeV]")
    band_2sigma.GetXaxis().SetTitle("#it{m}_{Med} [GeV]")
    band_2sigma.GetXaxis().SetTitleOffset(0.80)
    band_2sigma.GetXaxis().SetLabelSize(0.037)
    band_2sigma.GetXaxis().SetTitleSize(0.049)

    band_2sigma.GetYaxis().SetTitle("#sigma #times BR [pb]")
    band_2sigma.GetYaxis().SetTitleOffset(0.75)
    band_2sigma.GetYaxis().SetTitleSize(0.054)
    band_2sigma.GetYaxis().SetLabelSize(0.041)
    band_2sigma.GetYaxis().SetTitleFont(42)

    legend = ROOT.TLegend(0.65, 0.56, 0.95, 0.90)
    legend.SetTextSize(0.039)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetHeader("95% CL upper limits")

    if unblind:
        legend.AddEntry(obs,"Median observed")

    legend.AddEntry(theory, "t-channel")
    if plot_ref: legend.AddEntry(reference, "Expected (without tagger)")
    legend.AddEntry(median,"Expected")
    legend.AddEntry(band_1sigma,"68% expected")
    legend.AddEntry(band_2sigma,"95% expected")


    legend.SetEntrySeparation(0.3)
    legend.SetFillColor(ROOT.kWhite)

    c1 = ROOT.TCanvas()
    ROOT.SetOwnership(c1, False)
    c1.cd()
    c1.SetGrid()
    c1.SetLogy()
    band_2sigma.GetXaxis().SetRangeUser(600, 4400)
    c1.Update()

    band_2sigma.Draw("A3")
    band_2sigma.SetMinimum(5e-3)
    band_2sigma.SetMaximum(50e0)

    band_1sigma.Draw("3")

    median.Draw("L")
    if unblind:
        obs.Draw("L")
    theory.Draw("L same")
    if plot_ref: reference.Draw("L same")
    legend.Draw("Same")

    draw_labels(options.year)

    c1.Update()

    if not os.path.isdir(options.output_path):
        os.system("mkdir "+options.output_path)

    c1.SaveAs("%s/limits_rinv%s_%s.pdf" % (options.output_path, options.r_inv.replace(".","p"), options.year))

    # ROOT.gApplication.Run()

if __name__ == "__main__":
    main()
