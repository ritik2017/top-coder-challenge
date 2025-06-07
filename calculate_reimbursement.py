#!/usr/bin/env python3
import sys

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Fixed Efficiency System - Version 19.3-FIXED
    Original successful structure with efficiency bonus fix and minimal targeted adjustments
    Target: Score < 13,000 through minimal changes to proven system
    """
    days = trip_duration_days
    miles = miles_traveled
    receipts = total_receipts_amount
    
    base = _base_reimbursement(days, miles)
    receipt_add = _progressive_receipt_addition(receipts, days)

    miles_per_day = miles / days if days > 0 else 0.0

    bonuses = _day_bonus(days) + _efficiency_bonus(miles_per_day)
    penalties = _long_trip_penalty(days) + _aggregate_pattern_penalties(
        days, miles, receipts, miles_per_day
    )

    reimbursement = base + receipt_add + bonuses - penalties
    return round(reimbursement, 2)

def _base_reimbursement(days: int, miles: float) -> float:
    """Base reimbursement from days and miles (Version 19.3)."""
    return days * 83.5 + miles * 0.355 + 8

def _progressive_receipt_addition(receipts: float, days: int) -> float:
    """Progressive addition for receipts using the proven tiered schedule."""
    # Base tiers
    if receipts <= 500:
        return receipts * 0.82
    if receipts <= 1000:
        base = 500 * 0.82 + (receipts - 500) * 0.46
    elif receipts <= 1500:
        base = 500 * 0.82 + 500 * 0.46 + (receipts - 1000) * 0.22
    elif receipts <= 2000:
        base = 500 * 0.82 + 500 * 0.46 + 500 * 0.22 + (receipts - 1500) * 0.1
    else:  # receipts > 2000
        base = (
            500 * 0.82
            + 500 * 0.46
            + 500 * 0.22
            + 500 * 0.1
            + (receipts - 2000) * 0.05
        )
    
    # Slightly reduced additional compensation for high receipts (MINIMAL CHANGE)
    if receipts > 2000 and days <= 5:
        extra = min(600, (receipts - 2000) * 0.35)  # Reduced from 0.4
        return base + extra
    
    if receipts > 2000 and 6 <= days <= 10:
        extra = min(500, (receipts - 2000) * 0.25)  # Reduced from 0.3
        return base + extra
    
    if receipts > 2000 and days > 10:
        extra = min(400, (receipts - 2000) * 0.15)  # Reduced from 0.2
        return base + extra
    
    return base

def _day_bonus(days: int) -> float:
    """Fixed bonuses keyed by trip duration in days."""
    bonuses = {1: 80, 2: 80, 3: 98, 4: 114, 5: 140, 6: 152, 7: 147, 13: 66, 14: 43}
    return bonuses.get(days, 0.0)

def _efficiency_bonus(miles_per_day: float) -> float:
    """FIXED: Bonus for high daily mileage efficiency."""
    if miles_per_day > 470:
        return 65
    if miles_per_day > 200:
        return 35  # FIXED: Added missing return value
    return 0.0

def _long_trip_penalty(days: int) -> float:
    """Penalty applied for trips longer than 7 days."""
    if days <= 7:
        return 0.0
    return max(0, days - 7) * 60

def _penalty_high_receipt_eight_day(days: int, receipts: float) -> float:
    """High-receipt 8-day trips get special treatment."""
    if days == 8:
        if receipts > 2000:
            return min(800, (receipts - 2000) * 0.4)
        if receipts > 1500:
            return min(600, (receipts - 1500) * 0.3)
        if receipts > 1000:
            return min(300, (receipts - 1000) * 0.15)
    return 0.0

def _penalty_single_day_extreme_receipts(days: int, receipts: float, miles: float) -> float:
    """Single-day extreme receipts and high mileage penalties."""
    if days == 1:
        penalty = 0.0
        if receipts > 2000:
            penalty += min(600, (receipts - 2000) * 0.3)
        elif receipts > 1500:
            penalty += min(300, (receipts - 1500) * 0.2)
        
        if miles > 1000:
            penalty += min(300, (miles - 1000) * 0.2)
        elif miles > 800:
            penalty += min(150, (miles - 800) * 0.15)
        
        return penalty
    return 0.0

def _penalty_low_efficiency_high_spend(days: int, miles_per_day: float, receipts: float) -> float:
    """Low-efficiency high-spend penalty."""
    if miles_per_day < 60 and receipts > 1200 and days >= 4:
        return min(300, (receipts - 1200) * 0.15 + (60 - miles_per_day) * 3)
    return 0.0

def _penalty_very_high_receipts_global(receipts: float) -> float:
    """Very high receipts universal reduction."""
    if receipts > 2200:
        return min(200, (receipts - 2200) * 0.06)
    return 0.0

def _penalty_long_trip_moderate_receipts(days: int, receipts: float) -> float:
    """Long trip receipt penalties."""
    if days >= 11:
        if receipts > 2000:
            return min(600, (receipts - 2000) * 0.3 + (days - 11) * 30)
        if receipts > 1500:
            return min(400, (receipts - 1500) * 0.2 + (days - 11) * 20)
        if receipts > 1000:
            return min(200, (receipts - 1000) * 0.1 + (days - 11) * 10)
    return 0.0

def _penalty_medium_trip_high_receipts(days: int, receipts: float) -> float:
    """Medium trips with high receipts penalty."""
    if 4 <= days <= 6:
        if receipts > 2000:
            return min(400, (receipts - 2000) * 0.25)
        if receipts > 1500:
            return min(300, (receipts - 1500) * 0.2)
    return 0.0

def _penalty_high_mileage_single_day_high_receipts(days: int, miles: float, receipts: float) -> float:
    """High mileage single-day with very high receipts penalty."""
    if days == 1 and miles > 800:
        if receipts > 2000:
            return min(600, (receipts - 2000) * 0.35 + (miles - 800) * 0.1)
        if receipts > 1500:
            return min(400, (receipts - 1500) * 0.25 + (miles - 800) * 0.08)
    return 0.0

def _penalty_medium_days_low_mileage_high_receipts(days: int, miles: float, receipts: float) -> float:
    """Medium days with low mileage and high receipts penalty."""
    if 3 <= days <= 5 and miles < days * 80:
        if receipts > 2000:
            return min(400, (receipts - 2000) * 0.25 + (days * 80 - miles) * 0.3)
        if receipts > 1500:
            return min(300, (receipts - 1500) * 0.2 + (days * 80 - miles) * 0.2)
    return 0.0

def _aggregate_pattern_penalties(
    days: int, miles: float, receipts: float, miles_per_day: float
) -> float:
    """Sum of all pattern-based penalties for the given trip."""
    return sum(
        (
            _penalty_high_receipt_eight_day(days, receipts),
            _penalty_single_day_extreme_receipts(days, receipts, miles),
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
        print("Usage: python3 calculate_reimbursement.py <trip_duration_days> <miles_traveled> <total_receipts_amount>")
        sys.exit(1)
    
    try:
        trip_duration_days = int(sys.argv[1])
        miles_traveled = float(sys.argv[2])
        total_receipts_amount = float(sys.argv[3])
        
        result = calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount)
        print(result)
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
        sys.exit(1) 