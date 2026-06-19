import math

def extract_features(landmarks, min_visibility=0.5):
    def valid(lm):
        return lm.visibility >= min_visibility

    # 必要な点を取得
    nose = landmarks[0]
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]

    # 肩の中点
    shoulder_mid_x = (left_shoulder.x + right_shoulder.x) / 2
    shoulder_mid_y = (left_shoulder.y + right_shoulder.y) / 2

    # ① 首の前傾角（neck_angle）
    if valid(nose) and valid(left_shoulder) and valid(right_shoulder):
        dx = nose.x - shoulder_mid_x
        dy = nose.y - shoulder_mid_y
        neck_angle = math.degrees(math.atan2(abs(dx), abs(dy)))
        neck_valid = True
    else:
        neck_angle = None
        neck_valid = False

    # ② 肩の傾き（shoulder_tilt）
    if valid(left_shoulder) and valid(right_shoulder):
        dx = right_shoulder.x - left_shoulder.x
        dy = right_shoulder.y - left_shoulder.y
        shoulder_tilt = math.degrees(math.atan2(abs(dy), abs(dx)))
        shoulder_valid = True
    else:
        shoulder_tilt = None
        shoulder_valid = False

    return {
        "neck_angle":     {"value": neck_angle,     "valid": neck_valid},
        "shoulder_tilt":  {"value": shoulder_tilt,  "valid": shoulder_valid},
    }