"""Analytic planning approximations, NOT experimental observations or guaranteed power."""
import json
import math


def planning():
    normal = __import__("statistics").NormalDist()
    out = []
    for mix in ((160,160,160), (120,240,120), (60,360,60)):
        n = mix[1]
        for true_gain in (.10, .20, .30):
            discordance = .50
            se = math.sqrt((discordance-true_gain**2)/n)
            cutoff = max(.20, 1.96*se)
            out.append({"counts_A_B_C": mix, "absent_independent_families": n,
                        "assumed_gain": true_gain, "assumed_pair_discordance": discordance,
                        "approx_ci95_half_width": 1.96*se,
                        "approx_probability_meeting_20pp_and_positive_CI": 1-normal.cdf((cutoff-true_gain)/se)})
    return {"status": "PLANNING_ONLY", "assumptions": "one independent question per family; normal approximation; excludes budget, utility and replication gates", "rows": out}


if __name__ == "__main__":
    print(json.dumps(planning(), indent=2))
