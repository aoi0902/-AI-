import time
import sqlite3
from core.features import extract_features

def collect_features(pose, cam, seconds=3):
    """数秒間特徴量を収集して平均を返す"""
    collected = []
    start = time.time()

    while time.time() - start < seconds:
        ret, frame = cam.read_frame()
        if not ret:
            break
        landmarks = pose.estimate(frame)
        if landmarks:
            features = extract_features(landmarks)
            if features["neck_angle"]["valid"] and features["shoulder_tilt"]["valid"]:
                collected.append({
                    "neck_angle": features["neck_angle"]["value"],
                    "shoulder_tilt": features["shoulder_tilt"]["value"]
                })

    if not collected:
        return None

    # 平均化
    avg_neck = sum(f["neck_angle"] for f in collected) / len(collected)
    avg_shoulder = sum(f["shoulder_tilt"] for f in collected) / len(collected)

    return {
        "neck_angle": avg_neck,
        "shoulder_tilt": avg_shoulder
    }

def save_calibration(features, db_path="data/calibration.db"):
    """基準値をSQLiteに保存"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calibration (
            id INTEGER PRIMARY KEY,
            neck_angle REAL,
            shoulder_tilt REAL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    cursor.execute("DELETE FROM calibration")
    cursor.execute(
        "INSERT INTO calibration (neck_angle, shoulder_tilt) VALUES (?, ?)",
        (features["neck_angle"], features["shoulder_tilt"])
    )
    conn.commit()
    conn.close()
    print("基準値を保存しました")

def load_calibration(db_path="data/calibration.db"):
    """基準値をSQLiteから読み込む"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT neck_angle, shoulder_tilt FROM calibration ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"neck_angle": row[0], "shoulder_tilt": row[1]}
    return None