from __future__ import annotations

from app.core.schemas import PolicyResult, ValidationResult


class ValidationNode:
    def run(self, message: str, policy: PolicyResult) -> ValidationResult:
        text = message.lower()
        missing_information: list[str] = []

        for item in policy.required_information:
            lowered = item.lower()
            if lowered in text:
                continue
            if "last 4" in lowered and any(char.isdigit() for char in text):
                continue
            if "amount" in lowered and any(char.isdigit() for char in text):
                continue
            if "verification" in lowered and any(token in text for token in ("verify", "identity", "id")):
                continue
            missing_information.append(item)

        is_valid = len(missing_information) == 0
        notes = "All expected details are present." if is_valid else "Additional details are needed before a final action can be completed."
        return ValidationResult(is_valid=is_valid, missing_information=missing_information, notes=notes)