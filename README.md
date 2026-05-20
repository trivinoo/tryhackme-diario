# Beginner Splunk Log Generator

This tiny project creates fake application logs that are easy to understand and easy to search in Splunk.

Each log line is JSON, so Splunk can automatically find fields like `level`, `service`, `user`, `status_code`, and `response_ms`.

## 1. Create Logs

Run this from the project folder:

```powershell
.\run_logs.bat
```

That creates:

```text
logs/app.log
```

Create more logs:

```powershell
.\run_logs.bat --count 100
```

Create logs slowly so you can watch them arrive:

```powershell
.\run_logs.bat --count 50 --interval 1
```

If you already have Python working in your terminal, this also works:

```powershell
python .\log_generator.py --count 25
```

## 2. Add the Log File to Splunk

In Splunk:

1. Go to **Settings > Add Data**.
2. Choose **Upload** if you want to upload `logs/app.log` once.
3. Choose **Monitor** if you want Splunk to keep watching the file as you run the Python script again.
4. Use these beginner-friendly settings:
   - Source type: `_json`
   - Index: `main` or whatever index your Splunk class/lab uses

## 3. Try These Splunk Searches

Show all events:

```spl
index=main sourcetype=_json
```

Show only errors:

```spl
index=main sourcetype=_json level=ERROR
```

Count events by log level:

```spl
index=main sourcetype=_json
| stats count by level
```

Find the slowest services:

```spl
index=main sourcetype=_json
| stats avg(response_ms) as avg_response_ms max(response_ms) as max_response_ms by service
| sort - avg_response_ms
```

Find failed requests:

```spl
index=main sourcetype=_json status_code>=400
| table _time level service user status_code response_ms message request_id
```

## 4. What to Notice

- `INFO` means normal activity.
- `WARN` means something might need attention.
- `ERROR` means something failed.
- `response_ms` is how long the fake request took.
- `request_id` helps you track one request through logs.

You can delete `logs/app.log` anytime and run the script again to start fresh.
