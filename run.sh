#!/bin/bash

# Black Box Challenge - Reimbursement Calculation Implementation
# This script takes three parameters and outputs the reimbursement amount
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

# Call our Python implementation
python3 calculate_reimbursement.py "$1" "$2" "$3" 