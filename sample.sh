# sample_script.sh - Sample script for the advanced Python shell

echo "Starting script..."
cd /
echo "Current dir: $(pwd)"
echo "Running two jobs in parallel..."
sleep 1 & echo "Job 2 done" & wait
echo "Last command: !!"
help 