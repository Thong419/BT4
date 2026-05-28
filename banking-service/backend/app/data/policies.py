from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyRecord:
    intent: str
    title: str
    content: str
    required_information: tuple[str, ...]
    next_action: str
    routing_queue: str


POLICIES: dict[str, PolicyRecord] = {
    "lost_card": PolicyRecord(
        intent="lost_card",
        title="Lost Card / Emergency Card Freeze",
        content="Immediately freeze the card, confirm recent transactions, and advise the customer to review account activity.",
        required_information=("card last 4 digits", "approximate time noticed", "recent suspicious activity"),
        next_action="Freeze the card and open a card replacement request.",
        routing_queue="card-services",
    ),
    "block_card": PolicyRecord(
        intent="block_card",
        title="Card Block Request",
        content="Block the card immediately, verify the account holder, and provide replacement guidance if requested.",
        required_information=("card last 4 digits", "customer verification", "replacement preference"),
        next_action="Block the card and confirm replacement options.",
        routing_queue="card-services",
    ),
    "fraud_report": PolicyRecord(
        intent="fraud_report",
        title="Fraud Investigation Intake",
        content="Collect incident details, secure the account, and escalate to the fraud operations queue.",
        required_information=("transaction amount", "transaction date", "merchant name"),
        next_action="Open fraud case and secure the account.",
        routing_queue="fraud-investigation",
    ),
    "loan_inquiry": PolicyRecord(
        intent="loan_inquiry",
        title="Loan Information Request",
        content="Provide basic loan information and route the customer to the lending team for eligibility review.",
        required_information=("loan amount", "loan purpose", "income range"),
        next_action="Collect the loan details and forward to lending support.",
        routing_queue="lending-support",
    ),
    "balance_check": PolicyRecord(
        intent="balance_check",
        title="Balance and Account Summary",
        content="Guide the customer to the secure balance summary flow after identity verification.",
        required_information=("account identifier", "verification method"),
        next_action="Verify identity and provide the account balance summary.",
        routing_queue="self-service",
    ),
    "money_transfer": PolicyRecord(
        intent="money_transfer",
        title="Money Transfer Support",
        content="Confirm the transfer amount, destination, and timing before submission.",
        required_information=("recipient name", "transfer amount", "source account"),
        next_action="Confirm transfer details and route to payment services.",
        routing_queue="payments-operations",
    ),
    "account_update": PolicyRecord(
        intent="account_update",
        title="Account Profile Update",
        content="Collect the requested profile changes and verify the customer identity before making updates.",
        required_information=("field to update", "identity verification"),
        next_action="Verify identity and process the account update.",
        routing_queue="account-maintenance",
    ),
    "general_support": PolicyRecord(
        intent="general_support",
        title="General Banking Support",
        content="Provide a helpful response and route the request to the general assistance queue if required.",
        required_information=(),
        next_action="Answer the question or route to general support.",
        routing_queue="general-support",
    ),
}


INTENT_ALIASES: dict[str, str] = {
    "lost_or_stolen_card": "lost_card",
    "stolen_card": "lost_card",
    "freeze_card": "block_card",
    "card_block": "block_card",
    "card_blocking": "block_card",
    "transfer_money": "money_transfer",
    "send_money": "money_transfer",
    "balance": "balance_check",
    "check_balance": "balance_check",
    "update_account": "account_update",
    "support": "general_support",
}


def get_policy(intent: str) -> PolicyRecord:
    normalized = INTENT_ALIASES.get(intent, intent)
    return POLICIES.get(normalized, POLICIES["general_support"])


def list_policy_titles() -> list[str]:
    return [policy.title for policy in POLICIES.values()]