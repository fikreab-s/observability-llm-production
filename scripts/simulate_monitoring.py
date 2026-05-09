"""LLM production monitoring simulation."""
import json, numpy as np, argparse
from pathlib import Path
np.random.seed(42)

def main():
    p = argparse.ArgumentParser(); p.add_argument("--output_dir", default="outputs"); a = p.parse_args()
    out = Path(a.output_dir); out.mkdir(parents=True, exist_ok=True)
    minutes = 120; records = []
    for t in range(minutes):
        latency_p50 = 80 + np.random.randn() * 15
        latency_p99 = 200 + np.random.randn() * 40 + (100 if t > 90 else 0)
        error_rate = 0.005 + np.random.exponential(0.003) + (0.02 if t > 95 else 0)
        tokens = int(np.random.poisson(150))
        cost = round(tokens * 0.00001, 5)
        records.append({"minute": t, "latency_p50": round(latency_p50, 1),
            "latency_p99": round(latency_p99, 1), "error_rate": round(error_rate, 5),
            "tokens": tokens, "cost_usd": cost,
            "sla_breach": latency_p99 > 500, "alert": error_rate > 0.01})
    breaches = sum(1 for r in records if r["sla_breach"])
    alerts = sum(1 for r in records if r["alert"])
    with open(out / "monitoring_log.json", "w") as f: json.dump(records, f, indent=2)
    print(f"\u2705 LLM Monitoring Simulation ({minutes} minutes)")
    print(f"   SLA breaches: {breaches}/{minutes} ({breaches/minutes*100:.1f}%)")
    print(f"   Error alerts: {alerts}/{minutes}")
    print(f"   Total cost: ${sum(r['cost_usd'] for r in records):.4f}")
    first_breach = next((r['minute'] for r in records if r['sla_breach']), None)
    if first_breach is not None:
        print(f"   Degradation detected at: minute {first_breach}")
    else:
        print("   No SLA breaches detected")

if __name__ == "__main__": main()
