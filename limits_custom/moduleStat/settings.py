import collections

# list of systematics
syst = collections.OrderedDict()
syst["lumi"] = ("lnN", "all", 1.10)
syst["trigger"] = ("lnN", "all", 1.02)
# syst["BkgRate"] = ("lnU", "Bkg", 4.)
# syst["mcstat"] = ("shape", ("QCD", "TT", "WJets", "ZJets", "sig"))
# syst["mcstat"] = ("shape", ["sig"])
# syst["trig"] = ("shape", ["sig"])
# syst["JER"] = ("shape", ["sig"])
# syst["JEC"] = ("shape", ["sig"])


# list of backgrounds
processes = ["QCD"]

# list of analysis channels
# channels = ["SVJ0", "SVJ1", "SVJ2"]
# channels = ["SVJ0"]
# channels = ["SVJ1"]
# channels = ["SVJ2"]
# channels = ["SVJ3"]
# channels = ["SVJ4"]
# channels = ["SVJ5P"]
channels = ["SVJ0","SVJ1","SVJ2","SVJ3","SVJ4","SVJ5P"]

# list of signals
signal_points = [
    ("500", "20", "0.3", "peak"),
    # ("600", "20", "0.3", "peak"), # only in Keane's samples
    # ("800", "20", "0.3", "peak"), # only in Keane's samples
    ("1000", "20", "0.3", "peak"),
    ("1500", "20", "0.3", "peak"),
    ("2000", "20", "0.3", "peak"),
    ("3000", "20", "0.3", "peak"),
    # ("4000", "20", "0.3", "peak"), # only in Keane's samples
]
