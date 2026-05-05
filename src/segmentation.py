def segment_messages(messages):
    segments = []
    start = 0

    for i in range(1, len(messages)):
        if len(messages[i]) < 5:  # simple heuristic break
            segments.append((start, i-1))
            start = i

    segments.append((start, len(messages)-1))
    return segments