import modi


class Human:
    """
    사람 역할의 차체 클래스

    """

    def __init__(self, default_speed: int, bundle):
        """
        초기값 설정 함수

        Args:
            default_speed (int): 주행 기본 속도
            bundle (_type_): 모디 사용을 위한 패키지
        """

        self.default_speed = default_speed
        self.bundle = bundle
        self.set_sensor_location()
        self.set_motor_location()

    # 모터 위치 고정
    def set_motor_location(self):
        """모터의 위치 설정
        모디 실행 시, 모터의 좌 우 할당이 연결된 모터의 순서에 따라 배정됨.
        이를 해결하고자 모듈의 id값이 "1420"인 모터를 왼 쪽으로 고정
        """
        if str(self.bundle.motors[0]._id) == "1013":
            self.motor_left = self.bundle.motors[0]  # 왼쪽 바퀴
            self.motor_right = self.bundle.motors[1]  # 오른쪽 바퀴
        else:
            self.motor_left = self.bundle.motors[1]  # 왼쪽 바퀴
            self.motor_right = self.bundle.motors[0]  # 오른쪽 바퀴

    # 적외선 위치 고정
    def set_sensor_location(self):
        """적외선 센서의 위치 고정
        모디 실행 시, 전방 2개의 적외선 센서 위치가 랜덤하게 연결된 적외선 센서의 순서에 따라 배정됨.
        이를 해결하고자 id값이 "1388"인 모듈을 왼 쪽 센서로 고정
        """
        if str(self.bundle.irs[0]._id) == "1388":
            self.ir_left = self.bundle.irs[0]  # 왼쪽 바퀴
            self.ir_right = self.bundle.irs[1]  # 오른쪽 바퀴
        else:
            self.ir_left = self.bundle.irs[1]  # 왼쪽 바퀴
            self.ir_right = self.bundle.irs[0]  # 오른쪽 바퀴

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

        '주기적인 속도 조절'
          while문의 사이클 횟수를 누적하는 cnt값에 따라,
          speed down변인은 0 <= cnt < 60인 구간에서 함께 누적되며 30 <= cnt <= 60인 구간 (30 <= speed down <= 60) 에서 속도가 감속
          speed down변인이 60이 되면 0으로 값을 초기화

          speed up변인은 60 <= cnt < 160인 구간에서 함게 누적되며 61 <= cnt <= 160인 구간에서 (1 <= speed up <= 100) 속도가 기본 주행 속도로 복귀
          speed up변인은 160이 되면 (cnt값이 160일 때) 0으로 값을 초기화
          이때(cnt값이 160인 사이클이 종료 될 때) cnt값도 0으로 초기화 후 다시 사이클 순환

        """
        # 모터에 속도 할당
        self.set_motor(self.default_speed)
        # 전방의 좌 센서의 감지량
        ir_left_value = self.ir_left.proximity
        # 전방의 우 센서의 감지량
        ir_right_value = self.ir_right.proximity
        # 전방의 좌우 센서의 감지량 차이
        diff = ir_left_value - ir_right_value
        # 주행 사이클(while문)의 누적 횟수
        cnt = 0

        # 회전 보정 계수
        MULTIPLIER_LR = 0.0057

        # 환경 요소 측정 및 주행 사이클
        speed_up = 0
        speed_down = 0
        cnt = 0
        while True:
            # 기본 속도 주행
            if speed_down < 30 and speed_up < 1:
                print("기본 속도 주행 중")
                self.motor_left.speed = (
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR)) - 0.1,
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR)) - 0.1,
                )
                self.motor_right.speed = int(
                    self.default_speed * (1 - diff * MULTIPLIER_LR)
                ), int(self.default_speed * (1 - diff * MULTIPLIER_LR))

            # 속도 감속 (사람이 뒤쳐지는 상황)
            if 30 <= speed_down <= 60:
                print("SPEED down 중")
                self.motor_left.speed = (
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR)) + 3.9,
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR)) + 3.9,
                )
                self.motor_right.speed = (
                    int(self.default_speed * (1 - diff * MULTIPLIER_LR)) - 4.0,
                    int(self.default_speed * (1 - diff * MULTIPLIER_LR)) - 4.0,
                )
                if speed_down == 60:
                    speed_down = 0

            # 속도 복귀 (사람이 다시 속도를 올린 상황))
            if 1 <= speed_up <= 100:
                print("기본 속도 주행 중")
                self.motor_left.speed = (
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR)) - 0.1,
                    -int(self.default_speed * (1 + diff * MULTIPLIER_LR)) - 0.1,
                )
                self.motor_right.speed = int(
                    self.default_speed * (1 - diff * MULTIPLIER_LR)
                ), int(self.default_speed * (1 - diff * MULTIPLIER_LR))
                if speed_up == 100:
                    speed_up = 0

            # 한 사이클 종료 시 측정 값 초기화(재측정)
            ir_left_value = self.ir_left.proximity
            ir_right_value = self.ir_right.proximity
            diff = ir_left_value - ir_right_value

            # 주기적인 속도 감속 및 복귀를 위한 변인
            if 0 <= cnt < 60:
                speed_down += 1
            elif 60 <= cnt <= 160:
                speed_up += 1

            if cnt == 160:
                cnt = 0

            cnt += 1

            print("cnt: ", cnt)
            print("현재 왼 쪽 모터 속도: ", self.motor_left.speed)
            print("현재 오른 쪽 모터 속도: ", self.motor_right.speed)

    # 주행 종료
    def stop(self):
        """주행 종료
        주행을 종료하는 함수
        """
        self.motor_left.speed = 0, 0
        self.motor_right.speed = 0, 0


if __name__ == "__main__":
    bundle = modi.MODI(conn_type="ble", network_uuid="567B17C8")
    car = PaceMakerCar(40, bundle)
    try:
        car.run()
    except KeyboardInterrupt:
        print("페이스메이커 작동을 멈춥니다.")
        car.stop()
