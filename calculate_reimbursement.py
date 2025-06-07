#!/usr/bin/env python3
import sys

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Optimized Precision System - Version 19.0
    Based on most successful patterns from conversation history
    Target: Score < 5,000 through balanced corrections
    """
    days = trip_duration_days
    miles = miles_traveled
    receipts = total_receipts_amount
    
    base = _base_reimbursement(days, miles)
    receipt_add = _progressive_receipt_addition(receipts)

    miles_per_day = miles / days if days > 0 else 0.0

    bonuses = _day_bonus(days) + _efficiency_bonus(miles_per_day)
    penalties = _long_trip_penalty(days) + _aggregate_pattern_penalties(
        days, miles, receipts, miles_per_day
    )

    reimbursement = base + receipt_add + bonuses - penalties
    return round(reimbursement, 2)

def _base_reimbursement(days: int, miles: float) -> float:
    """Base reimbursement from days and miles (Version 13.1)."""
    return days * 83.5 + miles * 0.355 + 8

def _progressive_receipt_addition(receipts: float) -> float:
    """Progressive addition for receipts using the proven tiered schedule."""
    if receipts <= 500:
        return receipts * 0.82
    if receipts <= 1000:
        return 500 * 0.82 + (receipts - 500) * 0.46
    if receipts <= 1500:
        return 500 * 0.82 + 500 * 0.46 + (receipts - 1000) * 0.22
    if receipts <= 2000:
        return 500 * 0.82 + 500 * 0.46 + 500 * 0.22 + (receipts - 1500) * 0.1
    # receipts > 2000
    return (
        500 * 0.82
        + 500 * 0.46
        + 500 * 0.22
        + 500 * 0.1
        + (receipts - 2000) * 0.05
    )

def _day_bonus(days: int) -> float:
    """Fixed bonuses keyed by trip duration in days."""
    bonuses = {1: 80, 2: 80, 3: 98, 4: 114, 5: 140, 6: 152, 7: 147, 13: 66, 14: 43}
    return bonuses.get(days, 0.0)

def _efficiency_bonus(miles_per_day: float) -> float:
    """Bonus for high daily mileage efficiency."""
    if miles_per_day > 470:
        return 65
    if miles_per_day > 200:
        return 45
    return 0.0

def _long_trip_penalty(days: int) -> float:
    """Penalty applied for trips longer than 8 days."""
    return max(0, days - 8) * 60

# --- Penalty helpers ---------------------------------------------------------

def _penalty_high_receipt_eight_day(days: int, receipts: float) -> float:
    # High-receipt 8-day trips
    if days == 8 and receipts > 1400:
        return min(800, (receipts - 1400) * 0.4)
    return 0.0

def _penalty_single_day_extreme_receipts(days: int, receipts: float) -> float:
    # Single-day extreme receipts
    if days == 1 and receipts > 1500:
        return min(600, (receipts - 1500) * 0.3)
    return 0.0

def _penalty_low_efficiency_high_spend(days: int, miles_per_day: float, receipts: float) -> float:
    # Low-efficiency high-spend
    if miles_per_day < 60 and receipts > 1200 and days >= 4:
        return min(400, (receipts - 1200) * 0.2 + (60 - miles_per_day) * 4)
    return 0.0

def _penalty_very_high_receipts_global(receipts: float) -> float:
    # Very high receipts universal reduction
    if receipts > 2200:
        return min(300, (receipts - 2200) * 0.08)
    return 0.0

def _penalty_long_trip_moderate_receipts(days: int, receipts: float) -> float:
    # Long trip, moderate receipts
    if days >= 12 and 900 <= receipts <= 1300:
        return min(300, (days - 12) * 30 + (receipts - 900) * 0.1)
    return 0.0

def _penalty_medium_trip_high_receipts(days: int, receipts: float) -> float:
    # Medium trips with high receipts
    if 4 <= days <= 6 and receipts > 1600:
        return min(500, (receipts - 1600) * 0.25)
    return 0.0

def _penalty_high_mileage_single_day_high_receipts(days: int, miles: float, receipts: float) -> float:
    # High mileage single-day with very high receipts
    if days == 1 and miles > 800 and receipts > 1400:
        return min(600, (receipts - 1400) * 0.35 + (miles - 800) * 0.1)
    return 0.0

def _penalty_medium_days_low_mileage_high_receipts(days: int, miles: float, receipts: float) -> float:
    # Medium days with low mileage and high receipts
    if 3 <= days <= 5 and miles < days * 80 and receipts > 1000:
        under_efficiency = (days * 80 - miles) / (days * 80)
        return min(400, under_efficiency * receipts * 0.3)
    return 0.0

def _aggregate_pattern_penalties(
    days: int, miles: float, receipts: float, miles_per_day: float
) -> float:
    """Sum of all pattern-based penalties for the given trip."""

    return sum(
        (
            _penalty_high_receipt_eight_day(days, receipts),
            _penalty_single_day_extreme_receipts(days, receipts),
            _penalty_low_efficiency_high_spend(days, miles_per_day, receipts),
            _penalty_very_high_receipts_global(receipts),
            _penalty_long_trip_moderate_receipts(days, receipts),
            _penalty_medium_trip_high_receipts(days, receipts),
            _penalty_high_mileage_single_day_high_receipts(days, miles, receipts),
            _penalty_medium_days_low_mileage_high_receipts(days, miles, receipts),
        )
    )

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python calculate_reimbursement.py <days> <miles> <receipts>")
        sys.exit(1)
    
    days = int(sys.argv[1])
    miles = float(sys.argv[2])
    receipts = float(sys.argv[3])
    
    result = calculate_reimbursement(days, miles, receipts)
    print(f"{result:.2f}") 