# Weather ETL Pipeline - Scheduling Setup

## Overview

This document provides instructions for setting up the weather ETL pipeline to run automatically every day at noon (12:00 PM) local time.

## Files

- `weather_etl.py` - Main ETL pipeline script
- `run_weather_etl.sh` - Shell wrapper script for cron execution
- `setup_scheduler.md` - This setup guide

## Prerequisites

1. **Python Dependencies**: Ensure you have the required Python packages installed:
   ```bash
   # Using conda (recommended)
   conda install requests pandas

   # Or using pip
   pip install requests pandas
   ```

2. **File Permissions**: The shell script should be executable:
   ```bash
   chmod +x run_weather_etl.sh
   ```

## Setting up the Cron Job

### Step 1: Get the Full Path

First, get the full path to your weather ETL directory:

```bash
cd /path/to/your/weather_etl
pwd
```

Copy this path - you'll need it for the cron job.

### Step 2: Edit Crontab

Open the cron table for editing:

```bash
crontab -e
```

### Step 3: Add the Cron Job

Add the following line to run the pipeline daily at noon (12:00 PM):

```cron
# Weather ETL Pipeline - Daily at noon
0 12 * * * /path/to/your/weather_etl/run_weather_etl.sh
```

**Replace `/path/to/your/weather_etl/` with the actual path from Step 1.**

For example, if your path is `/Users/zhouhuan/IBM_Data_engineer_professional_Certificate/weather_etl`, the cron entry would be:

```cron
0 12 * * * /Users/zhouhuan/IBM_Data_engineer_professional_Certificate/weather_etl/run_weather_etl.sh
```

### Step 4: Save and Exit

Save the crontab file and exit the editor:
- In **vim**: Press `Esc`, then type `:wq` and press `Enter`
- In **nano**: Press `Ctrl+X`, then `Y`, then `Enter`

### Step 5: Verify the Cron Job

Check that your cron job was added successfully:

```bash
crontab -l
```

You should see your weather ETL cron job listed.

## Cron Schedule Explanation

The cron expression `0 12 * * *` means:
- `0` - At minute 0
- `12` - At hour 12 (noon)
- `*` - Every day of the month
- `*` - Every month
- `*` - Every day of the week

## Alternative Scheduling Options

If you want to run at a different time, modify the cron expression:

```cron
# Daily at 6:00 AM
0 6 * * * /path/to/your/weather_etl/run_weather_etl.sh

# Daily at 11:30 AM
30 11 * * * /path/to/your/weather_etl/run_weather_etl.sh

# Twice daily (6 AM and 6 PM)
0 6,18 * * * /path/to/your/weather_etl/run_weather_etl.sh

# Every 6 hours
0 */6 * * * /path/to/your/weather_etl/run_weather_etl.sh
```

## Testing the Setup

### Manual Test

Test the shell script manually before setting up the cron job:

```bash
cd /path/to/your/weather_etl
./run_weather_etl.sh
```

Check for any errors in the output.

### Test with Cron

For testing purposes, you can temporarily set a cron job to run every minute:

```cron
# Temporary test - runs every minute
* * * * * /path/to/your/weather_etl/run_weather_etl.sh
```

After confirming it works, remember to change it back to the daily schedule!

## Monitoring and Logs

### Log Files Created

The pipeline creates several log files:

1. **`cron_runner.log`** - Cron execution log with timestamps
2. **`weather_etl.log`** - Detailed ETL pipeline logs
3. **`weather_data.log`** - Weather data in tabular format
4. **`weather_data.csv`** - Weather data in CSV format
5. **`weather_data.db`** - SQLite database with weather data

### Checking Logs

Monitor the cron execution:

```bash
# Check cron runner log
tail -f cron_runner.log

# Check ETL pipeline log
tail -f weather_etl.log

# View recent weather data
tail -10 weather_data.log
```

### System Cron Logs

Check system-wide cron logs (varies by OS):

```bash
# macOS
log show --predicate 'eventMessage contains "cron"' --info --last 1d

# Linux
grep CRON /var/log/syslog
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x run_weather_etl.sh
   ```

2. **Python Not Found**
   - Ensure Python is in your PATH
   - Use full path to Python in the shell script if needed

3. **Module Not Found**
   - Install required packages: `pip install requests pandas`
   - Check if cron is using the correct Python environment

4. **Path Issues**
   - Use absolute paths in cron jobs
   - Verify the script path is correct

### Environment Variables

If you need specific environment variables, add them to the shell script:

```bash
# Add at the top of run_weather_etl.sh
export PATH="/usr/local/bin:/usr/bin:/bin"
export PYTHONPATH="/path/to/your/python/packages"
```

## Data Output Format

The weather data is saved in the exact format requested:

```
year    month   day     obs_tmp fc_temp
2025    7       28      27      26
2025    7       29      28      25
...
```

- **year**: Current year (YYYY)
- **month**: Current month (1-12)
- **day**: Current day (1-31)
- **obs_tmp**: Observed temperature in Celsius
- **fc_temp**: Forecasted temperature for tomorrow at noon in Celsius

## Security Considerations

1. **File Permissions**: Ensure log files are not world-readable if they contain sensitive data
2. **API Rate Limits**: wttr.in is free but consider rate limiting if running frequently
3. **Network Access**: Ensure the system has internet access for API calls

## Support

For issues with the weather ETL pipeline:
1. Check the log files for error messages
2. Verify internet connectivity
3. Test the wttr.in API manually: `curl "wttr.in/casablanca?format=j1"`
4. Ensure all Python dependencies are installed 