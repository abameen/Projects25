def generate_fake_logs(num_entries=1000):
  import random
  import string
  import datetime
  logs = []
  actions = ["LOGIN_SUCCESS", "LOGIN_FAILURE", "FILE_ACCESS", "FILE_DELETE", "PASSWORD_CHANGE"]
  for _ in range(num_entries):
        timestamp = datetime.datetime.now() - datetime.timedelta(seconds=random.randint(0, 86400))
        ip = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
        action = random.choice(actions)
        logs.append({"timestamp": timestamp, "ip": ip, "action": action})
    
  return logs

def suspicious_logs(logs, bad_ip_list):
  suspicious_logs = []
  for log in logs:
    if log["ip"] in bad_ip_list:
      suspicious_logs.append(log)
  return suspicious_logs

def detect_activity(logs, threshold):
  activity_count = {}
  for log in logs:
    if log["action"] in activity_count:
      activity_count[log["action"]] += 1
    else:
      activity_count[log["action"]] = 1

    if activity_count[log["action"]] >= threshold:
      return log["action"]

  return None

def main():
    # Step 1: Generate logs
    logs = generate_fake_logs(200)  # Increased the number of logs
    print("Generated Logs:")
    for log in logs[:5]:  # show only first 5 to avoid clutter
        print(log)

    # Step 2: Check for suspicious IPs
    # Update bad_ip_list to include some IPs from the generated logs
    bad_ip_list = [logs[0]["ip"], logs[2]["ip"], "192.168.1.1", "192.168.1.2"]
    flagged_logs = suspicious_logs(logs, bad_ip_list)
    print("\nSuspicious Logs Found:")
    for log in flagged_logs:
        print(log)

    # Step 3: Detect activity spikes
    threshold = 10
    spike_action = detect_activity(logs, threshold)
    if spike_action:
        print(f"\n⚠ Activity spike detected for: {spike_action}")
    else:
        print("\nNo activity spikes detected.")
        
if __name__ == "__main__":
    main()
    