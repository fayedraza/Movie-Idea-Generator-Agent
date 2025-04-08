#!/bin/bash
# Combined script to format code and run pylint in one go

set -e  # Exit on error

echo "===== STEP 1: Running the formatter script ====="
# Run the formatting script
./format_and_fix.sh

echo "===== STEP 2: Running pylint check ====="
# Create pylint reports directory if it doesn't exist
mkdir -p movie_idea_generator/pylint_reports

# Run pylint on the entire codebase
echo "Running pylint on the entire codebase..."
cd movie_idea_generator && python -m pylint src tests run.py --output-format=text | tee pylint_reports/complete_pylint_report.txt

# Get the score and display it
score=$(grep -oP "Your code has been rated at \K[0-9\.]+/10" pylint_reports/complete_pylint_report.txt)
if [ -n "$score" ]; then
  echo ""
  echo "===== Final pylint score: $score ====="
  
  # Extract just the number part
  numeric_score=$(echo $score | cut -d'/' -f1)
  
  # Check if we reached the target score of 8.0
  if (( $(echo "$numeric_score >= 8.0" | bc -l) )); then
    echo "✅ Great job! You've reached your target score of 8.0 or higher!"
  elif (( $(echo "$numeric_score < 3.0" | bc -l) )); then
    echo "❌ ERROR: Score is less than 3.0. This is below the minimum acceptable threshold."
    echo "Check pylint_reports/complete_pylint_report.txt for details on critical issues."
    exit 1  # Exit with error code
  else
    echo "⚠️ The score is below 8.0 but above the minimum threshold of 3.0."
    echo "Check pylint_reports/complete_pylint_report.txt for details on remaining issues."
  fi
else
  echo "⚠️ Could not determine the final pylint score."
  echo "Check pylint_reports/complete_pylint_report.txt for details."
  exit 1  # Exit with error code as we couldn't determine the score
fi

echo ""
echo "===== All done! =====" 