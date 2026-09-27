#!/usr/bin/env python3
"""Verify any Indian GSTIN against the official GST portal. Python, Node.js and cURL clients for the GST Number Search on Apify, pay per result.

Command-line client for the themineworks/gst-taxpayer-lookup actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/gst-taxpayer-lookup/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/gst-taxpayer-lookup"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--gstins", help="Comma-separated. One or more GSTINs to verify, standard 15-character format (for example 27ABQFM7569K1Z9)")
    ap.add_argument("--max-attempts", type=int, help="The portal returns a generic session error on a wrong CAPTCHA, so recovery means a fresh…")
    ap.add_argument("--concurrency", type=int, help="How many GSTINs to look up at once")
    ap.add_argument("--describe-business", action=argparse.BooleanOptionalAction, help="Writes a one-sentence description of what the supplier actually deals in, generated…")
    ap.add_argument("--cache-max-age-days", type=int, help="A GSTIN looked up within this many days is served from your own cache and is NOT charged…")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.gstins: run_input["gstins"] = [s.strip() for s in a.gstins.split(",") if s.strip()]
    if a.max_attempts is not None: run_input["maxAttempts"] = a.max_attempts
    if a.concurrency is not None: run_input["concurrency"] = a.concurrency
    if a.describe_business is not None: run_input["describeBusiness"] = a.describe_business
    if a.cache_max_age_days is not None: run_input["cacheMaxAgeDays"] = a.cache_max_age_days

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
