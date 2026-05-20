# Banking SOC Lab for Splunk

This lab simulates a small bank with normal customer activity plus suspicious scenarios that a SOC, fraud team, or SIEM analyst would investigate.

You are not just searching logs. You are practicing the full Splunk workflow:

1. Ingest banking logs.
2. Enrich events with lookups.
3. Build detections.
4. Create alerts.
5. Investigate timelines.
6. Tune false positives.
7. Build dashboards and reports.

## 1. Generate the Banking Scenario

From this folder, run:

```powershell
.\run_bank_lab.bat --reset --scenario full_banking_day
```

That creates:

```text
banking_lab/logs/auth.log
banking_lab/logs/account_changes.log
banking_lab/logs/transactions.log
banking_lab/logs/fraud.log
banking_lab/logs/employee_access.log
banking_lab/logs/cases.log
```

It also creates lookup files:

```text
banking_lab/lookups/vip_customers.csv
banking_lab/lookups/known_bad_ips.csv
banking_lab/lookups/employee_roles.csv
banking_lab/lookups/high_risk_countries.csv
```

You can also generate one scenario at a time:

```powershell
.\run_bank_lab.bat --reset --scenario account_takeover
.\run_bank_lab.bat --reset --scenario card_testing
.\run_bank_lab.bat --reset --scenario insider_abuse
```

## 2. Ingest the Logs in Splunk

In Splunk:

1. Go to **Settings > Add Data**.
2. Choose **Upload** or **Monitor**.
3. Add the files in `banking_lab/logs`.
4. Use source type `_json`.
5. Use index `bank` if you have one, or `main` if you are using a simple lab.

The searches below use:

```spl
index=bank
```

If you use `main`, replace `index=bank` with `index=main`.

## 3. Add the Lookup Files

In Splunk:

1. Go to **Settings > Lookups**.
2. Open **Lookup table files**.
3. Add each CSV from `banking_lab/lookups`.
4. Keep the same file names:
   - `vip_customers.csv`
   - `known_bad_ips.csv`
   - `employee_roles.csv`
   - `high_risk_countries.csv`

## 4. First Analyst View

Start with all banking activity:

```spl
index=bank
| table _time source event_type customer_id customer_name src_ip country device_id session_id amount status risk_score fraud_rule employee_id message
| sort _time
```

Pick one customer and build a timeline:

```spl
index=bank customer_id=cust_1042
| table _time source event_type customer_id src_ip country device_id session_id amount destination risk_score fraud_rule message
| sort _time
```

Your goal is to explain the story in plain English.

## 5. Lookup Enrichment

### Known Bad IP Enrichment

```spl
index=bank src_ip=*
| lookup known_bad_ips.csv src_ip OUTPUT threat_name risk as ip_risk
| where isnotnull(threat_name)
| table _time event_type customer_id src_ip country threat_name ip_risk
```

### VIP Customer Enrichment

```spl
index=bank customer_id=*
| lookup vip_customers.csv customer_id OUTPUT vip home_country home_city
| table _time event_type customer_id customer_name vip home_country home_city amount risk_score
```

### Employee Role Enrichment

```spl
index=bank employee_id=*
| lookup employee_roles.csv employee_id OUTPUT employee_name role
| stats count dc(customer_id) as unique_customers values(role) as role by employee_id employee_name
```

## 6. Detection 1: Account Takeover

Scenario logic:

Password reset + MFA success + new payee + high-value wire transfer.

```spl
index=bank
event_type IN ("password_reset","mfa_success","payee_added","wire_transfer")
| stats values(event_type) as events max(amount) as max_amount values(src_ip) as src_ips values(country) as countries values(device_id) as devices by customer_id session_id
| where mvfind(events, "password_reset")>=0
  AND mvfind(events, "mfa_success")>=0
  AND mvfind(events, "payee_added")>=0
  AND mvfind(events, "wire_transfer")>=0
  AND max_amount >= 5000
```

What to do with this:

- Save as a report named `Banking - Possible Account Takeover`.
- Then save it as an alert.
- Run it every 5 minutes.
- Trigger when number of results is greater than 0.

## 7. Detection 2: Brute Force Followed by Success

```spl
index=bank event_type IN ("login_failure","login_success")
| stats count(eval(event_type="login_failure")) as failures count(eval(event_type="login_success")) as successes values(country) as countries by customer_id src_ip
| where failures >= 5 AND successes >= 1
```

This is stronger than only searching for failed logins.

## 8. Detection 3: Card Testing Velocity

```spl
index=bank event_type=card_purchase
| bin _time span=5m
| stats count as purchase_count sum(amount) as total_amount dc(destination) as merchant_count values(status) as statuses by customer_id session_id _time
| where purchase_count >= 8 OR merchant_count >= 4
```

This catches many small card transactions in a short time.

## 9. Detection 4: Insider Abuse

```spl
index=bank source=employee_portal
| stats count as access_count dc(customer_id) as unique_customers max(account_balance) as highest_balance values(event_type) as actions by employee_id employee_name role
| where unique_customers >= 4 OR mvfind(actions, "fraud_hold_override")>=0
```

This catches broad account viewing and fraud hold overrides.

## 10. Risk Scoring Search

This is how you move from basic detection to SIEM-style thinking.

```spl
index=bank
| eval risk_points=case(
    event_type="login_failure", 5,
    event_type="password_reset", 25,
    event_type="mfa_success" AND (trusted_device=false OR trusted_device="false"), 25,
    event_type="payee_added", 30,
    event_type="wire_transfer" AND amount>=5000, 40,
    event_type="risk_score" AND risk_score>=80, 50,
    event_type="fraud_hold_override", 60,
    true(), 0
)
| stats sum(risk_points) as total_risk values(event_type) as events values(src_ip) as src_ips values(country) as countries max(amount) as max_amount max(risk_score) as max_fraud_score by customer_id session_id
| where total_risk >= 80
| sort - total_risk
```

This is a better real-world mindset than one alert per event.

## 11. Alert Ideas

Create these as saved searches or alerts:

- **High Risk Account Takeover Chain**
  - Use Detection 1.
  - Trigger when result count is greater than 0.
  - Severity: high.

- **Credential Attack Followed by Success**
  - Use Detection 2.
  - Trigger when result count is greater than 0.
  - Severity: medium/high.

- **Card Testing Velocity**
  - Use Detection 3.
  - Trigger when result count is greater than 0.
  - Severity: medium.

- **Employee Fraud Hold Override**
  - Search for `event_type=fraud_hold_override`.
  - Severity: high.

## 12. Dashboard Panels

Build a dashboard with these panels:

### Events by Source

```spl
index=bank
| stats count by source
```

### Top Risky Customers

```spl
index=bank
| stats max(risk_score) as max_risk sum(amount) as total_amount count by customer_id customer_name
| sort - max_risk
```

### Login Failures by Country

```spl
index=bank event_type=login_failure
| stats count by country
| sort - count
```

### High Value Transfers

```spl
index=bank event_type=wire_transfer amount>=5000
| table _time customer_id customer_name amount destination status session_id
```

### Employee Account Access

```spl
index=bank source=employee_portal
| stats count dc(customer_id) as unique_customers by employee_id employee_name role
| sort - unique_customers
```

## 13. Investigation Checklist

When an alert fires, answer:

1. Which customer or employee is involved?
2. What happened first?
3. What IP and country were used?
4. Was the device trusted?
5. Was there a password reset?
6. Was a new payee added?
7. Was money moved?
8. Did the fraud engine score it?
9. Did a case get created?
10. Does a lookup add context, like known bad IP or VIP customer?

## 14. Expected Lab Answers

If you run the full scenario, these are the intentional bad patterns:

- Account takeover customer: `cust_1042`
- Card testing customer: `cust_1002`
- Insider employee: `emp_2040`
- Known bad IP used in takeover: `185.22.10.9`
- High-risk wire transfer: `txn_wire_9001`
- Fraud case: `CASE-7001`

Use these only to check your work after investigating.
