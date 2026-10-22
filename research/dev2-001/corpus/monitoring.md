# Recursive Coherence Monitoring for Early Warning of Synthetic Control Degradation

Three sequential experiments with long run false alarm calibration

Matthew Chenoweth Wright  |  Monolithic LLC  |  12 October 2026

## Abstract

Three sequential experiments compared a recursive signed residual monitor with a conventional exponentially weighted moving average of absolute residuals on one synthetic control degradation benchmark. In the frozen confirmatory experiment, the recursive monitor improved median warning lead by 16.5 timesteps over 40 held out seeds; its bootstrap 95% interval was 3.5 to 18.5 timesteps. A follow up using the original thresholds found sustained alarms in 82.5% of recursive monitor runs and 97.5% of baseline runs during a 480 step no degradation horizon. A third experiment calibrated each method on separate no degradation traces to a 5% whole run false alarm target. On held out traces, whole run false alarm incidence was 2.5% for recursive coherence and 7.5% for residual EWMA; actionable warnings occurred in 96.25% and 81.25% of degradation runs, respectively. The median paired warning lead gain was 41.5 timesteps. These findings support a narrow conclusion: under this simulator, the recursive monitor retained an advantage after calibration to a long run false alarm budget. All three experiments reuse the same synthetic generator. They do not establish performance in energy infrastructure or any other field setting.

Keywords: anomaly detection; early warning; residual monitoring; synthetic control systems; false alarm calibration

## 1 Introduction

Early warning systems must do more than detect a change. They must signal useful changes early enough to matter without producing an unmanageable number of alarms during normal operation. EFMW EXP 001 compared a recursive coherence score with a residual EWMA on a synthetic control degradation task. Its frozen confirmatory result met the preregistered median lead gain criterion, but the reported false positive rate counted individual pre onset samples above threshold. That measure does not directly answer how often a sustained alarm occurs over a long operating window.

The work reported here reconciles that distinction through three sequential experiments. EXP 001 tests warning lead under its original frozen thresholds. EXP 002 applies those thresholds to no degradation traces and reveals high sustained alarm incidence. EXP 003 then calibrates each monitor on separate no degradation data to a common whole run alarm budget before testing on held out null and degradation traces. The central result is conditional: the recursive monitor performed better on this generator at the calibrated operating point, but the evidence remains simulator bound.

## 2 Benchmark and monitors

### 2.1 Synthetic control process

The benchmark contains 500 time steps per run. The simulator generates a latent state x and an observed state y, with control input u. In degradation runs, onset is drawn from steps 140 through 199 and a failure label is placed 120 steps later. A latent degradation variable rises gradually after onset. The update adds process noise, a degradation dependent bias, and a small oscillatory term; the observation adds independent measurement noise. Null runs disable degradation. This is a constructed toy process, not a model calibrated to a specific plant.

The simulator is summarized by the following discrete time definitions:

```text
d[t] = clip((t - onset) / 120, 0, 1.25)
u[t] = -0.45 * x[t]
x[t+1] = (0.82 + 0.08*d[t]) * x[t] + u[t] + process_noise + 0.05*d[t] + 0.012*d[t]*sin(0.18*t)
```

Process noise is sampled from a zero mean normal distribution with standard deviation 0.035; measurement noise has standard deviation 0.02. The controller and the monitor operate on observed values, while degradation and failure labels are available to the experiment scorer.

### 2.2 Monitor definitions

Both monitors receive the same one step residual. The baseline smooths its absolute magnitude. The recursive coherence monitor smooths the signed residual first and then takes its absolute value:

```text
r[t] = y[t] - (0.82*y[t-1] + u[t])
baseline[t] = 0.90*baseline[t-1] + 0.10*abs(r[t])
memory[t] = 0.97*memory[t-1] + 0.03*r[t]
coherence[t] = abs(memory[t])
```

An alert requires a score strictly above its threshold for three consecutive samples. Monitoring begins after a 20 step warmup. In EXP 001 and EXP 002, the thresholds are the values frozen in EXP 001. EXP 003 calibrates a new threshold for each monitor using only its own designated calibration traces.

## 3 Experimental sequence

### 3.1 EXP 001 confirmatory warning lead

EXP 001 froze its monitor equations, thresholds, seeds, and scoring plan before confirmatory execution. Threshold calibration used seeds 101 through 120; the held out confirmatory set used seeds 1001 through 1040. The baseline threshold was 0.0455502 and the recursive coherence threshold was 0.00834792. The primary criterion was a median paired warning lead gain of at least 10 timesteps. The analysis plan defined lead as time from first sustained alert to simulated failure, and assigned minus 999 when a post onset alert was absent. Raw pre onset false positive rate was defined as the fraction of individual score samples above threshold from warmup to onset. [1]

### 3.2 EXP 002 sustained false alarms under null conditions

EXP 002 reused the EXP 001 thresholds and monitor rules. It generated 80 no degradation traces using seeds 2001 through 2080. Each trace was scored in two paired conditions: an unmodified stable trace and a trace with an additive 0.05 observation offset at steps 220 through 231. The outcome was whether any three sample sustained alert occurred during the 480 step monitoring horizon. The frozen screen required recursive coherence false alarm incidence no greater than 10% and no more than five percentage points above baseline. [2]

### 3.3 EXP 003 matched whole run false alarm calibration

EXP 003 estimated thresholds separately for both monitors from 80 no degradation calibration traces, seeds 3001 through 3080. For each trace, it calculated the maximum over the run of the minimum score in every three sample window; the 76th ordered value among the 80 traces became that monitor's threshold. This set an empirical calibration false alarm incidence of 5% under the strict greater than alert rule. Thresholds were then fixed for disjoint held out null seeds 4001 through 4080 and degradation seeds 5001 through 5080. On degradation traces, an actionable warning had to be the monitor's first sustained alert and occur after degradation onset but before failure. A pre onset alert or a missed or late alert received a lead score of minus 999. The screen required median paired lead gain of at least 10 timesteps, held out null false alarm incidence no greater than 10% for each method, and recursive coherence actionable warning detection of at least 60%. [3]

## 4 Results

Table 1 summarizes the three experiments. EXP 001 reports pointwise pre onset rates; EXP 002 and EXP 003 report whole run sustained alarm incidence on null traces. These are different outcomes and should not be treated as interchangeable.

| Experiment | Null false alarms<br>EWMA / coherence | Actionable warnings<br>EWMA / coherence | Median paired lead gain | Screen result |
| --- | --- | --- | --- | --- |
| EXP 001 | Not measured<br>Pointwise: 5.13% / 6.15% | Median lead: 59 / 78 steps | +16.5 steps<br>95% interval: 3.5 to 18.5 | Passed frozen median gain rule |
| EXP 002 | 97.5% / 82.5%<br>Stable and pulse | Not applicable | Not applicable | Failed absolute 10% alarm limit |
| EXP 003 | 7.5% / 2.5% | 81.25% / 96.25% | +41.5 steps<br>95% interval: 37 to 47 | Passed all three screen rules |

Table 1. Results from the three sequential synthetic experiments. EXP 001 reports samplewise pre onset exceedance rates, not run level alarm incidence. EXP 002 used the original EXP 001 thresholds. EXP 003 recalibrated thresholds to a common whole run target.

In EXP 001, the median baseline warning lead was 59.0 timesteps and the recursive coherence median was 78.0. The median paired gain was 16.5 timesteps, exceeding the frozen 10 timestep point estimate criterion. The bootstrap 95% interval was 3.5 to 18.5 timesteps; the two sided Wilcoxon signed rank p value was 0.003923, and recursive coherence gave more lead on 30 of 40 seeds. The interval includes gains below 10. The p value supports a nonzero paired difference under the test assumptions; it does not establish that the underlying median gain exceeds 10. [1]

In EXP 002, sustained false alarms occurred in 66 of 80 recursive coherence runs (82.5%) and 78 of 80 baseline runs (97.5%) in both the stable and sensor offset conditions. The paired difference favored recursive coherence by 15 percentage points, with a bootstrap interval from minus 25.0 to minus 6.25 percentage points and exact McNemar p=0.00418. The experiment failed its absolute alarm limit because 82.5% was far above 10%. The equal aggregate counts in stable and pulse conditions mean the injected offset did not change the overall incidence in this sample. [2]

In EXP 003, calibration produced thresholds of 0.0542015 for residual EWMA and 0.0136070 for recursive coherence, each with 5.0% calibration false alarm incidence. On held out null traces, incidence was 6 of 80 (7.5%) for baseline and 2 of 80 (2.5%) for coherence. On degradation traces, actionable warnings occurred in 65 of 80 runs (81.25%) for baseline and 77 of 80 (96.25%) for coherence. Median lead across all runs, with missed actionable warnings scored minus 999, was 16.5 timesteps for baseline and 59.0 for coherence. The median paired gain was 41.5 timesteps (bootstrap 95% interval 37.0 to 47.0). The actionable detection comparison had 15 coherence only and 3 baseline only cases (exact McNemar p=0.00754). All three frozen screening conditions were met. [3]

## 5 Discussion

### 5.1 What the sequence establishes

The experiments establish three distinct findings on one generated system. First, the original frozen comparison favored recursive coherence on warning lead by its preregistered sample median criterion. Second, its original pointwise false positive measure did not predict the high frequency of sustained alarms over long null runs. Third, when each monitor was separately calibrated using null traces to the same whole run false alarm target, recursive coherence retained a higher actionable warning rate and greater median lead on new seeds from the same generator.

EXP 003 is a new operating point, not a correction to EXP 001 and not an independent replication. Its calibration approach was chosen after EXP 002 exposed the difference between pointwise exceedance and whole run alarm incidence, although its protocol, seed splits, and criteria were fixed before its run. The held out false alarm estimates are based on 80 null traces per monitor; the observed proportions are not guarantees of future false alarm rates. The result warrants a broader test, not a claim of operational readiness.

### 5.2 Relevance to energy control monitoring

The synthetic task resembles one possible maintenance question: whether a monitoring system can identify gradual control response degradation before a simulated failure. This makes energy control monitoring a reasonable candidate for further evaluation, but the present experiments contain no utility, power plant, grid operator, field sensor, historian, or customer data. No specific buyer problem has been validated. The results do not show physical validation, customer adoption, safety benefit, or regulatory certification.

A defensible next study would use a public or partner supplied operational time series with documented sensor definitions and reviewed degradation labels. It should separate calibration from evaluation by asset and time, establish a maximum alert burden with the data owner, compare against existing alarms and standard residual methods, report missed events and warning lead, and run initially in read only shadow mode. The test should be frozen before outcomes are examined. Any later proposal to connect to controls would require a separate engineering and safety review.

## 6 Limitations

- All three experiments reuse the same synthetic generator. New seeds do not create a new physical model or external replication.
- The simulated state, degradation path, noise distributions, controller, and failure label are specified by the experiment. They are not fitted to industrial data.
- The two monitors share a model residual. The comparison is narrow and does not establish superiority to a broad set of maintenance or anomaly detection methods.
- EXP 001 uses pointwise pre onset exceedance; EXP 002 and EXP 003 use run level sustained alarm incidence. Those endpoints answer different questions.
- EXP 003's thresholds are calibrated to this generator's null traces. Its 80 trace holdouts provide limited precision, and the 5% calibration target is a project design choice rather than an industry standard.
- No external benchmark, real operational data, hardware timing study, human alarm review, economic evaluation, or deployment test is included. The exploratory runtime measurements in an earlier report are not treated as confirmatory evidence.
## 7 Conclusion

Across three sequential experiments, recursive coherence provided earlier and more frequent actionable warnings than residual EWMA at the specified calibrated operating point on this synthetic control degradation generator. EXP 002 showed why long horizon false alarm incidence must be measured directly; EXP 003 showed that, after a separate null based calibration, the warning advantage remained on held out seeds from the same simulator. The result supports a testable monitoring hypothesis. It does not show that the method works in real energy infrastructure. The next evidentiary step is evaluation on independent operational data under a pre agreed alert budget.

Protocols, code, outputs, and checksums are available in the [EFMW EXP 001 repository](https://github.com/enuminous/EFMW-EXP-001), including the [EXP 002 screen](https://github.com/enuminous/EFMW-EXP-001/tree/main/EXP-002) and [EXP 003 screen](https://github.com/enuminous/EFMW-EXP-001/tree/main/EXP-003). The EXP 001 reconciliation also identifies exploratory timing claims that are not treated as confirmatory evidence.

## References

[1] Wright (2026), EFMW EXP 001, frozen benchmark and reconciliation, commit 048e263. [Repository record](https://github.com/enuminous/EFMW-EXP-001/tree/048e26372279de6da70e0db71033a883dba67b87)

[2] Wright (2026), EFMW EXP 002, benign transient specificity screen, commit 188b8c1. [Repository record](https://github.com/enuminous/EFMW-EXP-001/tree/188b8c13895510c513d186664cee0e739d6013ed/EXP-002)

[3] Wright (2026), EFMW EXP 003, matched whole run false alarm budget, commit aa7cc91. [Repository record](https://github.com/enuminous/EFMW-EXP-001/tree/aa7cc9183220df1eb39537107f38cbce8f51e515/EXP-003)

---

*Markdown edition of the formatted paper. The benchmark results are synthetic and do not establish field performance.*
