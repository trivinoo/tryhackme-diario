import argparse
import csv
import json
import random
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path


LOG_DIR = Path("banking_lab/logs")
LOOKUP_DIR = Path("banking_lab/lookups")

CUSTOMERS = [
    {
        "customer_id": "cust_1001",
        "name": "Ava Brooks",
        "home_country": "US",
        "home_city": "Miami",
        "vip": "false",
        "usual_device": "dev_ava_phone",
        "usual_ip": "73.21.44.10",
    },
    {
        "customer_id": "cust_1002",
        "name": "Noah Carter",
        "home_country": "US",
        "home_city": "Atlanta",
        "vip": "false",
        "usual_device": "dev_noah_laptop",
        "usual_ip": "98.14.11.24",
    },
    {
        "customer_id": "cust_1042",
        "name": "Mia Rivera",
        "home_country": "US",
        "home_city": "Orlando",
        "vip": "true",
        "usual_device": "dev_mia_phone",
        "usual_ip": "66.88.42.19",
    },
    {
        "customer_id": "cust_1077",
        "name": "Liam Patel",
        "home_country": "US",
        "home_city": "Tampa",
        "vip": "false",
        "usual_device": "dev_liam_tablet",
        "usual_ip": "47.18.90.77",
    },
]

EMPLOYEES = [
    {"employee_id": "emp_2001", "name": "Grace Allen", "role": "teller"},
    {"employee_id": "emp_2002", "name": "Ivan Kim", "role": "fraud_analyst"},
    {"employee_id": "emp_2040", "name": "Riley Stone", "role": "branch_manager"},
]

BAD_IPS = [
    {
        "src_ip": "185.22.10.9",
        "threat_name": "credential_stuffing_node",
        "risk": "high",
        "country": "RU",
    },
    {
        "src_ip": "45.155.205.11",
        "threat_name": "fraud_proxy_exit",
        "risk": "high",
        "country": "NL",
    },
    {
        "src_ip": "102.129.143.88",
        "threat_name": "anonymous_vpn",
        "risk": "medium",
        "country": "BR",
    },
]


def iso(event_time: datetime) -> str:
    return event_time.astimezone(timezone.utc).isoformat()


def write_event(log_name: str, event: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    path = LOG_DIR / f"{log_name}.log"
    with path.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(event, sort_keys=True) + "\n")


def base_event(event_time: datetime, source: str, event_type: str) -> dict:
    return {
        "timestamp": iso(event_time),
        "source": source,
        "event_type": event_type,
    }


def create_lookup_files() -> None:
    LOOKUP_DIR.mkdir(parents=True, exist_ok=True)

    write_csv(
        LOOKUP_DIR / "vip_customers.csv",
        ["customer_id", "customer_name", "vip", "home_country", "home_city"],
        [
            [
                customer["customer_id"],
                customer["name"],
                customer["vip"],
                customer["home_country"],
                customer["home_city"],
            ]
            for customer in CUSTOMERS
        ],
    )
    write_csv(
        LOOKUP_DIR / "known_bad_ips.csv",
        ["src_ip", "threat_name", "risk", "country"],
        [
            [item["src_ip"], item["threat_name"], item["risk"], item["country"]]
            for item in BAD_IPS
        ],
    )
    write_csv(
        LOOKUP_DIR / "employee_roles.csv",
        ["employee_id", "employee_name", "role"],
        [[employee["employee_id"], employee["name"], employee["role"]] for employee in EMPLOYEES],
    )
    write_csv(
        LOOKUP_DIR / "high_risk_countries.csv",
        ["country", "reason"],
        [
            ["RU", "high fraud volume in this lab"],
            ["NL", "proxy infrastructure in this lab"],
            ["BR", "anonymous VPN exit in this lab"],
        ],
    )


def write_csv(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(rows)


def reset_lab() -> None:
    if LOG_DIR.exists():
        shutil.rmtree(LOG_DIR)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def normal_banking_day(start: datetime, event_count: int) -> None:
    for index in range(event_count):
        customer = random.choice(CUSTOMERS)
        event_time = start + timedelta(minutes=index * random.randint(2, 6))
        session_id = f"sess_normal_{index:04d}"

        write_auth_success(event_time, customer, customer["usual_ip"], "US", customer["usual_device"], session_id)

        if random.random() < 0.55:
            amount = round(random.uniform(15, 450), 2)
            write_transaction(
                event_time + timedelta(minutes=random.randint(1, 4)),
                customer,
                session_id,
                "card_purchase",
                amount,
                "approved",
                random.choice(["GroceryTown", "FuelStop", "BookHub", "PharmacyPlus"]),
                "normal_customer_activity",
            )

        if random.random() < 0.18:
            write_auth_failure(
                event_time + timedelta(minutes=1),
                customer,
                customer["usual_ip"],
                "US",
                "bad_password",
                session_id,
            )


def account_takeover(start: datetime) -> str:
    customer = next(item for item in CUSTOMERS if item["customer_id"] == "cust_1042")
    attacker_ip = "185.22.10.9"
    attacker_country = "RU"
    session_id = "sess_ato_9001"
    device_id = "dev_unknown_881"
    transaction_id = "txn_wire_9001"

    for minute in [0, 1, 2, 3, 4, 5]:
        write_auth_failure(
            start + timedelta(minutes=minute),
            customer,
            attacker_ip,
            attacker_country,
            "bad_password",
            f"{session_id}_fail_{minute}",
        )

    write_account_change(
        start + timedelta(minutes=7),
        customer,
        session_id,
        "password_reset",
        "self_service",
        "password reset completed from new location",
        attacker_ip,
        attacker_country,
    )
    write_auth_success(start + timedelta(minutes=9), customer, attacker_ip, attacker_country, device_id, session_id)
    write_auth_event(
        start + timedelta(minutes=10),
        "mfa_success",
        customer,
        attacker_ip,
        attacker_country,
        device_id,
        session_id,
        {"mfa_method": "sms", "trusted_device": False},
    )
    write_account_change(
        start + timedelta(minutes=14),
        customer,
        session_id,
        "payee_added",
        "self_service",
        "new external payee added",
        attacker_ip,
        attacker_country,
        {"payee_id": "payee_ext_7781"},
    )
    write_transaction(
        start + timedelta(minutes=19),
        customer,
        session_id,
        "wire_transfer",
        9500.00,
        "approved",
        "payee_ext_7781",
        "new_payee_high_value_transfer",
        transaction_id,
    )
    write_fraud_score(
        start + timedelta(minutes=20),
        customer,
        session_id,
        transaction_id,
        92,
        "new_device_new_payee_high_value_transfer",
    )
    write_case_event(
        start + timedelta(minutes=22),
        "CASE-7001",
        customer,
        "high",
        "open",
        "account takeover suspected after high-risk wire transfer",
    )
    return customer["customer_id"]


def card_testing(start: datetime) -> str:
    customer = next(item for item in CUSTOMERS if item["customer_id"] == "cust_1002")
    session_id = "sess_cardtest_4001"
    merchants = ["GameKeys", "StreamBox", "MobileTopUp", "GiftCardWorld", "OnlineMarket"]

    for index in range(12):
        write_transaction(
            start + timedelta(seconds=index * 22),
            customer,
            session_id,
            "card_purchase",
            round(random.uniform(3, 25), 2),
            random.choice(["approved", "declined"]),
            random.choice(merchants),
            "rapid_small_card_transactions",
            f"txn_cardtest_{index:04d}",
        )

    write_fraud_score(
        start + timedelta(minutes=5),
        customer,
        session_id,
        "txn_cardtest_batch",
        88,
        "card_velocity_many_small_purchases",
    )
    return customer["customer_id"]


def insider_abuse(start: datetime) -> str:
    employee = next(item for item in EMPLOYEES if item["employee_id"] == "emp_2040")
    viewed_customers = [customer["customer_id"] for customer in CUSTOMERS]

    for index in range(18):
        customer_id = random.choice(viewed_customers)
        write_employee_access(
            start + timedelta(minutes=index),
            employee,
            customer_id,
            "employee_account_view",
            random.randint(80000, 650000),
            "viewed customer profile",
        )

    write_employee_access(
        start + timedelta(minutes=21),
        employee,
        "cust_1042",
        "fraud_hold_override",
        240000,
        "manual override of fraud hold",
    )
    return employee["employee_id"]


def write_auth_success(
    event_time: datetime,
    customer: dict,
    src_ip: str,
    country: str,
    device_id: str,
    session_id: str,
) -> None:
    write_auth_event(
        event_time,
        "login_success",
        customer,
        src_ip,
        country,
        device_id,
        session_id,
        {"trusted_device": device_id == customer["usual_device"], "status": "success"},
    )


def write_auth_failure(
    event_time: datetime,
    customer: dict,
    src_ip: str,
    country: str,
    reason: str,
    session_id: str,
) -> None:
    write_auth_event(
        event_time,
        "login_failure",
        customer,
        src_ip,
        country,
        "unknown",
        session_id,
        {"reason": reason, "trusted_device": False, "status": "failure"},
    )


def write_auth_event(
    event_time: datetime,
    event_type: str,
    customer: dict,
    src_ip: str,
    country: str,
    device_id: str,
    session_id: str,
    extra: dict,
) -> None:
    event = base_event(event_time, "customer_auth", event_type)
    event.update(
        {
            "customer_id": customer["customer_id"],
            "customer_name": customer["name"],
            "src_ip": src_ip,
            "country": country,
            "device_id": device_id,
            "session_id": session_id,
        }
    )
    event.update(extra)
    write_event("auth", event)


def write_account_change(
    event_time: datetime,
    customer: dict,
    session_id: str,
    event_type: str,
    channel: str,
    message: str,
    src_ip: str,
    country: str,
    extra: dict | None = None,
) -> None:
    event = base_event(event_time, "account_service", event_type)
    event.update(
        {
            "customer_id": customer["customer_id"],
            "customer_name": customer["name"],
            "session_id": session_id,
            "channel": channel,
            "message": message,
            "src_ip": src_ip,
            "country": country,
        }
    )
    if extra:
        event.update(extra)
    write_event("account_changes", event)


def write_transaction(
    event_time: datetime,
    customer: dict,
    session_id: str,
    transaction_type: str,
    amount: float,
    status: str,
    destination: str,
    reason: str,
    transaction_id: str | None = None,
) -> None:
    event = base_event(event_time, "transaction_service", transaction_type)
    event.update(
        {
            "customer_id": customer["customer_id"],
            "customer_name": customer["name"],
            "session_id": session_id,
            "transaction_id": transaction_id or f"txn_{random.randint(100000, 999999)}",
            "amount": amount,
            "currency": "USD",
            "status": status,
            "destination": destination,
            "reason": reason,
        }
    )
    write_event("transactions", event)


def write_fraud_score(
    event_time: datetime,
    customer: dict,
    session_id: str,
    transaction_id: str,
    score: int,
    rule: str,
) -> None:
    event = base_event(event_time, "fraud_engine", "risk_score")
    event.update(
        {
            "customer_id": customer["customer_id"],
            "customer_name": customer["name"],
            "session_id": session_id,
            "transaction_id": transaction_id,
            "risk_score": score,
            "risk_level": "high" if score >= 80 else "medium",
            "fraud_rule": rule,
        }
    )
    write_event("fraud", event)


def write_case_event(
    event_time: datetime,
    case_id: str,
    customer: dict,
    priority: str,
    status: str,
    message: str,
) -> None:
    event = base_event(event_time, "fraud_case_system", "case_created")
    event.update(
        {
            "case_id": case_id,
            "customer_id": customer["customer_id"],
            "customer_name": customer["name"],
            "priority": priority,
            "status": status,
            "message": message,
        }
    )
    write_event("cases", event)


def write_employee_access(
    event_time: datetime,
    employee: dict,
    customer_id: str,
    event_type: str,
    account_balance: int,
    message: str,
) -> None:
    event = base_event(event_time, "employee_portal", event_type)
    event.update(
        {
            "employee_id": employee["employee_id"],
            "employee_name": employee["name"],
            "role": employee["role"],
            "customer_id": customer_id,
            "account_balance": account_balance,
            "message": message,
        }
    )
    write_event("employee_access", event)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a banking SOC lab for Splunk.")
    parser.add_argument(
        "--scenario",
        choices=["account_takeover", "card_testing", "insider_abuse", "full_banking_day"],
        default="full_banking_day",
        help="Scenario to generate. Default: full_banking_day",
    )
    parser.add_argument(
        "--normal-events",
        type=int,
        default=40,
        help="Number of normal customer sessions to generate. Default: 40",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete old banking lab logs before generating new ones.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    random.seed(42)

    if args.reset:
        reset_lab()

    create_lookup_files()
    start = datetime.now(timezone.utc) - timedelta(hours=3)
    normal_banking_day(start, args.normal_events)

    findings = []
    scenario_start = start + timedelta(hours=2)
    if args.scenario in ["account_takeover", "full_banking_day"]:
        findings.append(("account_takeover_customer", account_takeover(scenario_start)))
    if args.scenario in ["card_testing", "full_banking_day"]:
        findings.append(("card_testing_customer", card_testing(scenario_start + timedelta(minutes=35))))
    if args.scenario in ["insider_abuse", "full_banking_day"]:
        findings.append(("insider_employee", insider_abuse(scenario_start + timedelta(minutes=70))))

    print("Banking SOC lab generated.")
    print(f"Logs:    {LOG_DIR}")
    print(f"Lookups: {LOOKUP_DIR}")
    print("\nKnown answers for validation:")
    for name, value in findings:
        print(f"- {name}: {value}")


if __name__ == "__main__":
    main()
