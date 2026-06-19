def calculate_score(current_features, baseline):
    """
    現在の特徴量と基準値を比べてスコアを計算する
    スコアは0〜100点
    """
    if baseline is None:
        return None, "キャリブレーションが必要です"

    scores = []

    # 首の前傾角のスコア
    if current_features["neck_angle"]["valid"]:
        neck_diff = abs(current_features["neck_angle"]["value"] - baseline["neck_angle"])
        neck_score = max(0, 100 - neck_diff * 5)
        scores.append(neck_score)

    # 肩の傾きのスコア
    if current_features["shoulder_tilt"]["valid"]:
        shoulder_diff = abs(current_features["shoulder_tilt"]["value"] - baseline["shoulder_tilt"])
        shoulder_score = max(0, 100 - shoulder_diff * 5)
        scores.append(shoulder_score)

    if not scores:
        return None, "有効な特徴量がありません"

    # 平均スコア
    total_score = sum(scores) / len(scores)

    # 判定メッセージ
    if total_score >= 80:
        message = "Good posture!"
    elif total_score >= 60:
        message = "Posture slightly off. "
    else:
        message = "Fix your posture!"

    return total_score, message