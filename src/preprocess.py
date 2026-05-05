import pandas as pd

def load_messages(csv_path):
    df = pd.read_csv(csv_path, header=None)            
    messages = []
    for convo in df.iloc[:,0].dropna():
        for msg in str(convo).splitlines():
            msg = msg.strip()
            if not msg:
                continue
            # Remove speaker labels like "User 1:" if present
            if ':' in msg:
                parts = msg.split(":", 1)
                if len(parts) > 1:
                    msg = parts[1].strip()
            messages.append(msg)
    return messages
