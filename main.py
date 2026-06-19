import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cv2
from core.capture import Camera
from core.pose import PoseEstimator
from core.features import extract_features
from core.calibration import collect_features, save_calibration, load_calibration
from core.scoring import calculate_score

def main():
    baseline = load_calibration()
    if baseline:
        print(f"基準値を読み込みました: 首={baseline['neck_angle']:.1f}度, 肩={baseline['shoulder_tilt']:.1f}度")
    else:
        print("キャリブレーションがまだです。'c'キーで登録してください")

    with Camera() as cam, PoseEstimator() as pose:
        print("'c'キーでキャリブレーション、'q'で終了")

        while cam.is_opened():
            ret, frame = cam.read_frame()
            if not ret:
                break

            landmarks = pose.estimate(frame)

            if landmarks:
                features = extract_features(landmarks)
                neck = features["neck_angle"]
                shoulder = features["shoulder_tilt"]

                # 角度表示
                if neck["valid"]:
                    cv2.putText(frame, f"Neck: {neck['value']:.1f}deg", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                if shoulder["valid"]:
                    cv2.putText(frame, f"Shoulder: {shoulder['value']:.1f}deg", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # スコア表示
                score, message = calculate_score(features, baseline)
                if score is not None:
                    color = (0, 255, 0) if score >= 80 else (0, 165, 255) if score >= 60 else (0, 0, 255)
                    cv2.putText(frame, f"Score: {score:.0f}", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    cv2.putText(frame, message, (10, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('c'):
                print("キャリブレーション開始！3秒間良い姿勢で静止してください")
                result = collect_features(pose, cam, seconds=3)
                if result:
                    save_calibration(result)
                    baseline = result
                    print(f"基準値: 首={result['neck_angle']:.1f}度, 肩={result['shoulder_tilt']:.1f}度")
                else:
                    print("失敗。もう一度試してください")

            elif key == ord('q'):
                break

            cv2.imshow("Pose", frame)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()