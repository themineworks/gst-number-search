# GST Number Search: Verify GSTIN & Nature of Business

Verify Indian GSTINs against the official GST portal: legal name, trade name, registration status, constitution, registration and cancellation dates, jurisdiction, principal address, and declared HSN/SAC codes with a plain-English line of business. Solves the portal's CAPTCHA with a vision model, no manual step, no third-party GSTIN database. No result, no charge.

**Run it on Apify:** [apify.com/themineworks/gst-taxpayer-lookup](https://apify.com/themineworks/gst-taxpayer-lookup)
**Docs, FAQ and pricing:** [themineworks.com/actors/gst-taxpayer-lookup](https://themineworks.com/actors/gst-taxpayer-lookup/)

**Price:** $0.004 per GSTIN on Apify's free plan, down to $0.003 on higher plans, plus a $0.02 start fee per run. Failed and empty results are never charged.

## What it returns

* Legal name, trade name, status, and constitution per GSTIN
* Registration and cancellation dates, jurisdiction, and address
* Declared HSN/SAC codes with a plain-English business summary
* Solves the GST portal CAPTCHA automatically via vision model
* Short-term cache avoids re-billing repeat lookups
* Zero charge on a failed lookup

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/gst-taxpayer-lookup").call(run_input={
    "gstins": [
        "27ABQFM7569K1Z9",
        "24AAWFA8982B1Z3"
    ],
    "maxAttempts": 6,
    "concurrency": 5,
    "describeBusiness": true
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/gst-taxpayer-lookup').call({
    "gstins": [
        "27ABQFM7569K1Z9",
        "24AAWFA8982B1Z3"
    ],
    "maxAttempts": 6,
    "concurrency": 5,
    "describeBusiness": true
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~gst-taxpayer-lookup/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"gstins": ["27ABQFM7569K1Z9", "24AAWFA8982B1Z3"], "maxAttempts": 6, "concurrency": 5, "describeBusiness": true}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 gst_number_search.py --token YOUR_APIFY_TOKEN --gstins "27ABQFM7569K1Z9,24AAWFA8982B1Z3" --max-attempts "6" --concurrency "5" --describe-business
node gst_number_search.mjs --token YOUR_APIFY_TOKEN --gstins "27ABQFM7569K1Z9,24AAWFA8982B1Z3" --max-attempts "6" --concurrency "5" --describe-business
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `gstins` (required) | array |  | One or more GSTINs to verify, standard 15-character format (for example 27ABQFM7569K1Z9) |
| `maxAttempts` | integer | `6` | The portal returns a generic session error on a wrong CAPTCHA, so recovery means a fresh session and a fresh… |
| `concurrency` | integer | `5` | How many GSTINs to look up at once |
| `describeBusiness` | boolean | `true` | Writes a one-sentence description of what the supplier actually deals in, generated strictly from the HSN and… |
| `cacheMaxAgeDays` | integer | `7` | A GSTIN looked up within this many days is served from your own cache and is NOT charged again |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `gstin` | string | The 15-character GSTIN looked up |
| `found` | boolean | Whether a real taxpayer record was found |
| `legalName` | string | Registered legal name |
| `tradeName` | string | Trade name, if different from legal name |
| `status` | string | Registration status (Active, Cancelled, etc) |
| `constitutionOfBusiness` | string | Business constitution (Proprietorship, Private Limited, etc) |
| `taxpayerType` | string | Taxpayer type (Regular, Composition, etc) |
| `registrationDate` | string | GST registration date |
| `principalAddress` | string | Principal place of business address |
| `natureOfBusinessActivities` | array | Declared business activities |
| `goodsHsn` | array | HSN codes and descriptions for goods dealt in |
| `servicesSac` | array | SAC codes and descriptions for services offered |
| `error` | string | Error reason when found is false |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/gst-taxpayer-lookup
```

## FAQ

### What is a GSTIN?

A 15-character Goods and Services Tax Identification Number assigned to every business registered under India's GST regime. It encodes the state code and PAN, and is required on every B2B invoice.

### Does this hit the official GST portal, or a third-party database?

The official GST portal (services.gst.gov.in), not a resold or cached third-party dataset. The portal's own CAPTCHA is solved automatically with a vision model, so there is no manual step and no stale data.

### What does the "nature of business" field actually tell me?

It synthesizes the declared HSN (goods) and SAC (services) codes into a one-sentence, plain-English description of what the business actually does, useful when a company name alone does not tell you.

### Can I use this to check if a supplier is still registered?

Yes. Status, registration date, and cancellation date (if applicable) come back per GSTIN, which is the standard first check before onboarding a new vendor or reconciling an old invoice.

### What does it cost?

Pay-per-event at $4 per 1,000 GSTINs verified ($0.004 each). A failed lookup, including one blocked by the portal, is never charged, and repeat lookups within the cache window are not re-billed.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [World Bank Trade Scraper](https://themineworks.com/actors/global-trade-data/): Imports and exports by country and product, from World Bank WITS
* [SEC EDGAR Filings](https://themineworks.com/actors/sec-edgar-filings/): Structured SEC filings ready for AI and RAG pipelines
* [EU VAT Validator](https://themineworks.com/actors/eu-vat-vies-validator/): Bulk EU VAT number verification via official VIES

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
