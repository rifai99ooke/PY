import cv2
import mediapipe as mp

# Setup MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def count_fingers(hand_landmarks, handedness):
    """Menghitung jumlah jari yang terangkat"""
    fingers = []
    tips = [4, 8, 12, 16, 20]  # ID ujung jari
    
    # Cek jempol (berbeda untuk tangan kiri dan kanan)
    if handedness == "Right":
        if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if hand_landmarks.landmark[tips[0]].x > hand_landmarks.landmark[tips[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
    
    # Cek jari lainnya (telunjuk, tengah, manis, kelingking)
    for tip in tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers

def detect_gesture(fingers):
    """Mendeteksi gesture berdasarkan jari yang terangkat"""
    total = sum(fingers)
    
    if fingers == [0, 0, 0, 0, 0]:
        return "Kepalan Tangan ✊"
    elif fingers == [1, 1, 1, 1, 1]:
        return "Hallo ✋"
    elif fingers == [0, 1, 0, 0, 0]:
        return "Pointing ☝️"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Peace Sign ✌️"
    elif fingers == [1, 1, 1, 0, 0]:
        return "Tiga Jari"
    elif fingers == [1, 1, 1, 1, 0]:
        return "Empat Jari"
    elif fingers == [1, 1, 0, 0, 1]:
        return "Nama Saya Ahmad Rifa'i 🤘"
    elif fingers == [1, 1, 0, 0, 0]:
        return "Gun Sign 👉"
    elif fingers == [1, 0, 0, 0, 0]:
        return "Sip 👍"
    elif total == 1:
        return f"Satu Jari"
    elif total == 2:
        return f"Dua Jari"
    elif total == 3:
        return f"Tiga Jari"
    elif total == 4:
        return f"Empat Jari"
    else:
        return f"{total} Jari"

# Buka kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("=" * 50)
print("HAND SIGN DETECTION")
print("=" * 50)
print("Gesture yang bisa dideteksi:")
print("- Kepalan tangan")
print("- Telapak terbuka (5 jari)")
print("- Pointing (telunjuk)")
print("- Peace sign (2 jari)")
print("- Rock sign (jempol + kelingking)")
print("- Gun sign (jempol + telunjuk)")
print("- Dan lainnya...")
print("\nTekan 'q' untuk keluar")
print("=" * 50)

while True:
    success, frame = cap.read()
    if not success:
        print("Gagal membuka kamera!")
        break
    
    # Flip frame horizontal (efek cermin)
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    # Konversi ke RGB untuk MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Deteksi tangan
    results = hands.process(rgb_frame)
    
    # Gambar kotak info
    cv2.rectangle(frame, (10, 10), (400, 100), (0, 0, 0), -1)
    cv2.putText(frame, "Hand Sign Detection", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "Tekan 'q' untuk keluar", (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, (hand_landmarks, handedness) in enumerate(zip(results.multi_hand_landmarks, results.multi_handedness)):
            # Gambar landmark tangan
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            
            # Deteksi tangan kiri atau kanan
            hand_label = handedness.classification[0].label
            
            # Hitung jari yang terangkat
            fingers = count_fingers(hand_landmarks, hand_label)
            
            # Deteksi gesture
            gesture = detect_gesture(fingers)
            
            # Posisi teks
            y_position = 150 + (idx * 100)
            
            # Gambar background untuk teks
            cv2.rectangle(frame, (10, y_position - 40), (450, y_position + 30), (0, 0, 0), -1)
            
            # Tampilkan info tangan
            cv2.putText(frame, f"Tangan: {hand_label}", (20, y_position - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # Tampilkan gesture
            cv2.putText(frame, f"Gesture: {gesture}", (20, y_position + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    else:
        # Jika tidak ada tangan terdeteksi
        cv2.rectangle(frame, (10, 140), (450, 200), (0, 0, 0), -1)
        cv2.putText(frame, "Tidak ada tangan terdeteksi", (20, 175),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    # Tampilkan frame
    cv2.imshow('Hand Sign Detection - Tekan Q untuk keluar', frame)
    
    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()

print("\nProgram selesai. Terima kasih!")