import os
import collections

import moduleStat.settings as settings


class Limit(object):
    combine_label_to_arg_name = {
        "Expected 50.0%": "value",
        "Observed": "observed",
        "Reference": "reference",
        "Expected 84.0%": "points_up_1_sigma",
        "Expected 97.5%": "points_up_2_sigma",
        "Expected 16.0%": "points_down_1_sigma",
        "Expected  2.5%": "points_down_2_sigma",
    }

    label_to_attr_name = {
        "mass": "mass",
        "y_vals": "value",
        "y_observed": "observed",
        "y_reference": "reference",
        "y_up_points1": "points_up_1_sigma",
        "y_up_points2": "points_up_2_sigma",
        "y_down_points1": "points_down_1_sigma",
        "y_down_points2": "points_down_2_sigma",
    }

    def __init__(self):
        self.mass = 0.
        self.value = 0.
        self.observed = 0.
        self.reference = 0.
        self.points_up_1_sigma = 0.
        self.points_up_2_sigma = 0.
        self.points_down_1_sigma = 0.
        self.points_down_2_sigma = 0.

    def Print(self):
        print("\n\nLimits:")
        print("Mass: ", self.mass)
        print("Values: ", self.value)
        print("Observed: ", self.observed)
        print("Reference: ", self.reference)


def __get_limit_from_combine_log(log_path):
    input_file = open(log_path)
    print("Reading ", log_path)

    limit = Limit()

    for line in input_file.readlines():
        if line.strip() == "":
            continue

        l_split = line.split()

        for label, arg_name in limit.combine_label_to_arg_name.items():
            if line.startswith(label):
                setattr(limit, arg_name, l_split[4])

    return limit


def __write_file(limits, suffix, output_file_name):

    lines = {}

    for label, attr_name in Limit.label_to_attr_name.items():
        lines[label] = "{}{}\t".format(label, suffix)

    limits_ordered_by_mass = collections.OrderedDict(sorted(limits.items()))

    for mass, limit in limits_ordered_by_mass.items():
        for label, attr_name in Limit.label_to_attr_name.items():
            lines[label] += "{}\t".format(getattr(limit, attr_name))

    output_string = ""

    for line in lines.values():
        output_string += "{}\n".format(line)

    print("\n", output_string)

    limits_file = open(output_file_name, 'w')
    limits_file.write(output_string)
    limits_file.close()


def get_limits(base_path, suffix, year, output_path):
    limits = {}

    if not os.path.isdir(output_path):
        os.system("mkdir -p "+output_path)

    r_invs = set()

    for (m_z_prime, _, r_inv, _) in settings.signal_points:

        sample_base_name = "mZprime{}_rinv{}".format(m_z_prime, r_inv.replace(".", "p"))

        file_name = "{}/".format(base_path)
        file_name += "{}/".format(sample_base_name)
        file_name += "asymptotic_{}_{}.log".format(sample_base_name, year)

        r_invs.add(r_inv)

        print("r_inv: ", r_inv, "\tmZ: ", m_z_prime, "\tyear: ", year)

        if r_inv not in limits:
            limits[r_inv] = {}

        limits[r_inv][float(m_z_prime)] = __get_limit_from_combine_log(file_name)
        limits[r_inv][float(m_z_prime)].mass = float(m_z_prime)

    for r_inv in r_invs:
        __write_file(limits[r_inv], suffix, output_path+"/limit_rinv" + r_inv + "_" + year + suffix + ".txt")
