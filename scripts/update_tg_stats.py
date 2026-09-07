import os
import re
import json
import urllib.request

token = os.environ.get("TELEGRAM_BOT_TOKEN")
if not token:
    print("TELEGRAM_BOT_TOKEN not provided in environment.")
    exit(0)

targets = {
    "main_channel": "@lusufer127",
    "pvt_channel": "-1003930789453",
    "main_group": "-1003998413486"
}

counts = {}
for key, chat_id in targets.items():
    url = f"https://api.telegram.org/bot{token}/getChatMemberCount?chat_id={chat_id}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=10)
        data = json.loads(res.read().decode())
        if data.get("ok"):
            counts[key] = data.get("result")
    except Exception as e:
        print(f"Error fetching {key} ({chat_id}): {e}")

if not counts:
    print("Could not fetch any counts.")
    exit(0)

print(f"Fetched counts: {counts}")
total = sum(counts.values())
print(f"Total community reach: {total}")

# Format numbers with commas (e.g. 4,792+)
def fmt(num):
    return f"{num:,}+"

readme_path = "README.md"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update total audience badge if total >= 1000
    if total > 0:
        total_k = f"{round(total / 1000)}K+"
        content = re.sub(r'Total_Community-[0-9,]+%2B_Members', f'Total_Community-{total:,}%2B_Members', content)
        content = re.sub(r'Telegram_Reach-[0-9,]+%2B_Audience', f'Telegram_Reach-{total:,}%2B_Audience', content)

    if "main_channel" in counts:
        content = re.sub(r'Subscribers-[0-9,]+%2B', f'Subscribers-{counts["main_channel"]:,}%2B', content)
    if "pvt_channel" in counts:
        content = re.sub(r'VIP_Members-[0-9,]+%2B', f'VIP_Members-{counts["pvt_channel"]:,}%2B', content)
    if "main_group" in counts:
        content = re.sub(r'Members-[0-9,]+%2B-00c647', f'Members-{counts["main_group"]:,}%2B-00c647', content)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("README.md updated with live counts!")