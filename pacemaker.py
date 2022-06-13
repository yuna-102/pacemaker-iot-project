import time
from typing import Callable, List, Optional

import modi
import pandas as pd

from voice_synthesis import load_voice_model, text_to_speech

# 회전 보정 계수
MULTIPLIER_LR = 0.0060
# 감속 계수
MULTIPLIER_BACK = 0.8
# 칼로리 환산 계수
CALORIE_CONVERSION_FACTOR = 0.0175


class PaceMakerCar:
    """
    페이스 메이커의 클래스

    """

    def __init__(
        self,
        user_id: int,
        default_speed: int,
        bundle: Callable,
        user_data: Optional[pd.DataFrame] = None,
        user_weight: Optional[int] = None,
    ) -> None:
        """
        초기값 설정 함수로
        1. 주행 기본 속도를 설정한다.
        2. 번들 패키지를 불러온다.
        3. 적외선 센서와 모터의 위치를 할당하는 함수를 불러온다.

        Args:
            default_speed (int): 주행 기본 속도
            bundle (Callable): 모디 사용을 위한 패키지
            user_weight (Optional[int], optional): 사용자의 몸무게

        """
        self.user_id = user_id
        self.default_speed = default_speed
        self.bundle = bundle
        self.user_weight = user_weight if user_weight else 0
        self.user_data = (
            user_data
            if user_data
            else pd.DataFrame(
                columns=["id", "timd", "user_calories", "running_distance"]
            )
        )
        self.set_sensor_location()
        self.set_motor_location()
        self.processor, self.model, self.mb_melgan = load_voice_model()

    # 모디 키트와 연결
    @staticmethod
    async def load_modi() -> None or Callable:
        try:
            print("aa")
            bundle = modi.MODI()
            return bundle
        except:
            return None

    # 모터 위치 고정
    def set_motor_location(self):
        """모터의 위치 설정
        모디 실행 시, 모터의 좌 우 할당이 연결된 모터의 순서에 따라 배정됨.
        이를 해결하고자 모듈의 id값이 "1420"인 모터를 왼 쪽으로 고정
        """
        if str(self.bundle.motors[0]._id) == "1420":
            self.motor_left = self.bundle.motors[0]  # 왼쪽 바퀴
            self.motor_right = self.bundle.motors[1]  # 오른쪽 바퀴
        else:
            self.motor_left = self.bundle.motors[1]  # 왼쪽 바퀴
            self.motor_right = self.bundle.motors[0]  # 오른쪽 바퀴

    # 적외선 위치 고정
    def set_sensor_location(self):
        """적외선 센서의 위치 고정
        모디 실행 시, 전방 2개 후방 1개의 적외선 센서 위치가 랜덤하게 연결된 적외선 센서의 순서에 따라 배정됨.
        이를 해결하고자 id값이 "205"인 모듈을 후방 센서로 고정 후, 전방의 좌 우 센서는 id값의 대소 비교를 통해 고정
        """
        if str(self.bundle.irs[0]._id) == "205":
            self.back_cam = self.bundle.irs[0]
            if int(self.bundle.irs[1]._id) < int(self.bundle.irs[2]._id):
                self.ir_left = self.bundle.irs[1]
                self.ir_right = self.bundle.irs[2]
            else:
                self.ir_left = self.bundle.irs[2]
                self.ir_right = self.bundle.irs[1]

        elif str(self.bundle.irs[1]._id) == "205":
            self.back_cam = self.bundle.irs[1]
            if int(self.bundle.irs[0]._id) < int(self.bundle.irs[2]._id):
                self.ir_left = self.bundle.irs[0]
                self.ir_right = self.bundle.irs[2]
            else:
                self.ir_left = self.bundle.irs[2]
                self.ir_right = self.bundle.irs[0]

        elif str(self.bundle.irs[2]._id) == "205":
            self.back_cam = self.bundle.irs[2]
            if int(self.bundle.irs[0]._id) < int(self.bundle.irs[1]._id):
                self.ir_left = self.bundle.irs[0]
                self.ir_right = self.bundle.irs[1]
            else:
                self.ir_left = self.bundle.irs[1]
                self.ir_right = self.bundle.irs[0]

    # 모터 설정
    def set_motor(self, speed):
        """모터의 초기 속도 설정
        좌 우 모터의 degree값을 0으로 초기화 한 후
        주행 기본 속도 할당
        Args:
            speed (_type_): 주행 기본 속도
        """
        self.motor_left.degree = 0, 0
        self.motor_right.degree = 0, 0
        self.motor_left.speed = speed, speed
        self.motor_right.speed = speed, speed

    # 소모 칼로리 계산
    @staticmethod
    def calculate_calories(motor_speed, user_weight, run_time):
        return CALORIE_CONVERSION_FACTOR * motor_speed * user_weight * run_time

    # 텍스트를 음성으로 변환
    def text_to_speech_in_pacemaker(self, text):
        text_to_speech(
            text,
            self.processor,
            self.model,
            self.mb_melgan,
            language="ko",
            display_streamlit=False,
        )

    # 주행
    def run(self):
        """주행
        '기본 주행'(if distance_diff >= 15)
          전방 좌 우 적외선 센서가 바닥의 흰 색과 검정 선에 반사된 빛의 감지량 차이 diff값을 이용해 주행

          검정 선 인식값: 0 ~ 5 사이
          흰색 바닥 인식값: 90 ~ 100 사이
          diff = 좌 적외선 센서 인식값 - 우 적외선 센서 인식값

          diff < 0: 차체의 왼쪽 바퀴가 검정 선 위에 있음(오른 쪽으로 치우침)
          -> diff값을 사용해 왼 쪽 바퀴의 속도는 줄이고 오른 쪽 바퀴의 속도는 증가시킴(좌회전))
          diff > 0: 위와 반대의 경우

        '사람과의 거리 감지'(if distance_diff < 15)
          사람과의 거리를 감지하는 후방 센서의 값이 15이하가 되면 일정 거리를 벗어난 것으로 판단
          감지량이 15이상 즉, 사람이 다시 일정 거리 이내로 들어올 때 까지 속도 감속

        """
        # 모터에 속도 할당
        self.set_motor(self.default_speed)
        # 전방의 좌 센서의 감지량
        ir_left_value = self.ir_left.proximity
        # 전방의 우 센서의 감지량
        ir_right_value = self.ir_right.proximity
        # 전방의 좌우 센서의 감지량 차이
        diff = ir_left_value - ir_right_value
        # 후방 거리 감지 센서값
        distance_diff = self.back_cam.proximity

        motor_speed = 0
        run_time = 0

        # 환경 요소 측정 및 주행 사이클
        diff_count = 0
        while True:
            start_time = time.time()
            text_to_speech("운동을 시작합니다.")
            time.sleep(3)
            # 일정 거리 이내
            if distance_diff >= 15:
                diff_count = 0
                self.motor_left.speed = (
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR)) - 0.1,
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR)) - 0.1,
                )
                self.motor_right.speed = int(
                    self.default_speed * (1 - diff * MULTIPLIER_LR)
                ), int(self.default_speed * (1 - diff * MULTIPLIER_LR))

            # 일정 거리 이탈
            elif distance_diff < 15:
                if diff_count > 5:
                    text_to_speech("조금만 더 힘을 내세요!")
                    time.sleep(3)
                self.motor_left.speed = (
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR))
                    * MULTIPLIER_BACK
                ) - 0.1, (
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR))
                    * MULTIPLIER_BACK
                ) - 0.1
                self.motor_right.speed = (
                    int(self.default_speed * (1 - diff * MULTIPLIER_LR))
                    * MULTIPLIER_BACK
                ), (
                    int(self.default_speed * (1 - diff * MULTIPLIER_LR))
                    * MULTIPLIER_BACK
                )
                diff_count += 1

            end_time = time.time()

            # 1 사이클 종료 시 측정 값 초기화(재측정)
            ir_left_value = self.ir_left.proximity
            ir_right_value = self.ir_right.proximity
            diff = ir_left_value - ir_right_value
            distance_diff = self.back_cam.proximity

            motor_speed = (
                abs(self.motor_left.speed[0]) + abs(self.motor_right.speed[0])
            ) / 2
            run_time = end_time - start_time
            calories = self.calculate_calories(motor_speed, self.user_weight, run_time)

            # runtime을 분->시간 단위로 환산
            running_distance = motor_speed * (run_time / 60)

            self.user_data["user_calories"].append(calories)
            self.user_data["running_distance"].append(running_distance)

    # 주행 종료
    def stop(self):
        """주행 종료
        주행을 종료하는 함수
        """
        self.motor_left.speed = 0, 0
        self.motor_right.speed = 0, 0


if __name__ == "__main__":
    bundle = modi.MODI()
    car = PaceMakerCar(40, bundle)
    try:
        car.run()
    except KeyboardInterrupt:
        print("페이스메이커 작동을 멈춥니다.")
        car.stop()
