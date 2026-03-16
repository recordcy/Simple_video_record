import cv2
import datetime

source = "rtsp://210.99.70.120:1935/live/cctv006.stream"

window_name = "Video Recorder"

# 녹화 설정
fps = 20.0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# 밝기 조절 값
brightness = 0          # 기본값
brightness_step = 20    # 한 번 누를 때 증가/감소량
min_brightness = -100
max_brightness = 100

# =========================
# 카메라 열기
# =========================
cap = cv2.VideoCapture(source)

if not cap.isOpened():
    print("카메라(또는 영상 소스)를 열 수 없습니다.")
    exit()

# 첫 프레임을 읽어서 크기 확인
ret, frame = cap.read()
if not ret:
    print("프레임을 읽을 수 없습니다.")
    cap.release()
    exit()

height, width = frame.shape[:2]

recording = False
out = None

print("실행 성공")
print("조작키 안내:")
print("  SPACE : 녹화 시작/종료")
print("  U     : 밝기 증가")
print("  D     : 밝기 감소")
print("  R     : 밝기 초기화")
print("  ESC   : 종료")

# =========================
# 메인 루프
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 더 이상 읽을 수 없습니다. 프로그램을 종료합니다.")
        break

    # 밝기 조절 적용
    # beta 값을 통해 전체 밝기를 조절
    adjusted_frame = cv2.convertScaleAbs(frame, alpha=1.0, beta=brightness)

    # 현재 상태를 화면에 표시
    cv2.putText(
        adjusted_frame,
        f"Brightness: {brightness}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    if recording:
        # 녹화 중 표시
        cv2.circle(adjusted_frame, (30, 70), 10, (0, 0, 255), -1)
        cv2.putText(
            adjusted_frame,
            "REC",
            (50, 78),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        # 저장도 밝기 적용된 화면으로 저장
        out.write(adjusted_frame)

    cv2.imshow(window_name, adjusted_frame)

    key = cv2.waitKey(1) & 0xFF

    # ESC 키: 종료
    if key == 27:
        break

    # Space 키: Preview / Record 전환
    elif key == 32:
        recording = not recording

        if recording:
            filename = datetime.datetime.now().strftime("record_%Y%m%d_%H%M%S.mp4")
            out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

            if not out.isOpened():
                print("동영상 파일을 생성할 수 없습니다.")
                recording = False
                out = None
            else:
                print(f"녹화 시작: {filename}")

        else:
            if out is not None:
                out.release()
                out = None
            print("녹화 종료")

    # U 키: 밝기 증가
    elif key == ord('u') or key == ord('U'):
        brightness = min(brightness + brightness_step, max_brightness)
        print(f"밝기 증가: {brightness}")

    # D 키: 밝기 감소
    elif key == ord('d') or key == ord('D'):
        brightness = max(brightness - brightness_step, min_brightness)
        print(f"밝기 감소: {brightness}")

    # R 키: 밝기 초기화
    elif key == ord('r') or key == ord('R'):
        brightness = 0
        print("밝기 초기화")

# =========================
# 종료 처리
# =========================
cap.release()

if out is not None:
    out.release()

cv2.destroyAllWindows()