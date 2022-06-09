import datetime
from typing import Callable, List, Optional

import modi
import pandas as pd


class PaceMakerCar:
    def __init__(
        self,
        default_speed: int,
        bundle: Callable,
        user_data: Optional[pd.DataFrame] = None,
        user_weight: Optional[int] = None,
    ):
        self.default_speed = default_speed
        self.bundle = bundle
        self.user_weight = user_weight if user_weight else 0
        # self.user_data = user_data if user_data else pd.DataFrame()
        self.user_data = user_data if user_data else pd.DataFrame()
        # # 모터 위치 고정
        # if len(bundle.motors) >= 1:
        #     if str(self.bundle.motors[0]._id) == "1420":
        #         self.motor_left = self.bundle.motors[0]  # 왼쪽 바퀴
        #         self.motor_right = self.bundle.motors[1]  # 오른쪽 바퀴
        #     else:
        #         self.motor_left = self.bundle.motors[1]  # 왼쪽 바퀴
        #         self.motor_right = self.bundle.motors[0]  # 오른쪽 바퀴

        # # 적외선 위치 고정
        # if len(bundle.irs) >= 1:
        #     if str(self.bundle.irs[0]._id) == "205":
        #         self.back_cam = self.bundle.irs[0]
        #         if int(self.bundle.irs[1]._id) < int(self.bundle.irs[2]._id):
        #             self.ir_left = self.bundle.irs[1]
        #             self.ir_right = self.bundle.irs[2]
        #         else:
        #             self.ir_left = self.bundle.irs[2]
        #             self.ir_right = self.bundle.irs[1]

        #     elif str(self.bundle.irs[1]._id) == "205":
        #         self.back_cam = self.bundle.irs[1]
        #         if int(self.bundle.irs[0]._id) < int(self.bundle.irs[2]._id):
        #             self.ir_left = self.bundle.irs[0]
        #             self.ir_right = self.bundle.irs[2]
        #         else:
        #             self.ir_left = self.bundle.irs[2]
        #             self.ir_right = self.bundle.irs[0]

        #     elif str(self.bundle.irs[2]._id) == "205":
        #         self.back_cam = self.bundle.irs[2]
        #         if int(self.bundle.irs[0]._id) < int(self.bundle.irs[1]._id):
        #             self.ir_left = self.bundle.irs[0]
        #             self.ir_right = self.bundle.irs[1]
        #         else:
        #             self.ir_left = self.bundle.irs[1]
        #             self.ir_right = self.bundle.irs[0]

    @staticmethod
    async def load_modi() -> None or Callable:
        try:
            bundle = 1
            return bundle

        except:
            return None

    # 모터 설정
    def set_motor(self, speed: int) -> None:
        self.motor_left.degree = 0, 0
        self.motor_right.degree = 0, 0
        self.motor_left.speed = speed, speed
        self.motor_right.speed = speed, speed

    # # 거리 차이에 따른 속도 조절
    #   def feedback(self):
    #     distance_diff = self.back_cam.proximity

    #     ir_left_value = self.ir_left.proximity
    #     ir_right_value = self.ir_right.proximity
    #     multiplier_LR = 0.0065
    #     multiplier_Back = 0.3
    #     diff = ir_left_value - ir_right_value

    #     # 이슈: 타임 슬립과 곡선주로 사이
    #     if distance_diff < 50:
    #       self.motor_left.speed = ( -int(self.default_speed * (1+ diff*multiplier_LR)) * (1-multiplier_Back) ), ( -int(self.default_speed * (1+ diff*multiplier_LR)) * (1-multiplier_Back) )
    #       self.motor_right.speed = ( int(self.default_speed * (1+ diff*multiplier_LR)) * (1-multiplier_Back) ), ( int(self.default_speed * (1+ diff*multiplier_LR)) * (1-multiplier_Back) )

    #     else:
    @staticmethod
    def calculate_calories(
        motor_speed: int, user_weight: int, run_time: float
    ) -> float:
        return 0.0000291667 * motor_speed * user_weight * run_time

    # 주행
    def run(self):
        #     self.set_motor(self.default_speed)

        #     ir_left_value = self.ir_left.proximity
        #     ir_right_value = self.ir_right.proximity
        #     diff = ir_left_value - ir_right_value
        #     distance_diff = self.back_cam.proximity

        #     motor_speed = 0
        #     run_time = 0

        #     while True:
        #         start_time = datetime.datetime.now()
        #         # print("left_ir:", ir_left_value)
        #         # print("right_ir:", ir_right_value)
        #         multiplier_LR = 0.0065
        #         multiplier_Back = 0.8

        #         if distance_diff >= 15:
        #             print("정상 작동 중")
        #             print("back_cam:", self.back_cam.proximity)
        #             print("left_ir:", ir_left_value)
        #             print("right_ir:", ir_right_value)
        #             self.motor_left.speed = -int(
        #                 self.default_speed * (1 + diff * multiplier_LR)
        #             ), -int(self.default_speed * (1 + diff * multiplier_LR))
        #             self.motor_right.speed = int(
        #                 self.default_speed * (1 - diff * multiplier_LR)
        #             ), int(self.default_speed * (1 - diff * multiplier_LR))

        #         elif distance_diff < 15:
        #             print("일정 거리 이상 벌어졌습니다. 속도를 줄입니다.")
        #             print("back_cam:", self.back_cam.proximity)
        #             print("left_ir:", ir_left_value)
        #             print("right_ir:", ir_right_value)
        #             self.motor_left.speed = (
        #                 -int(self.default_speed * (1 + diff * multiplier_LR))
        #                 * multiplier_Back
        #             ), (
        #                 -int(self.default_speed * (1 + diff * multiplier_LR))
        #                 * multiplier_Back
        #             )
        #             self.motor_right.speed = (
        #                 int(self.default_speed * (1 - diff * multiplier_LR))
        #                 * multiplier_Back
        #             ), (
        #                 int(self.default_speed * (1 - diff * multiplier_LR))
        #                 * multiplier_Back
        #             )

        #         end_time = datetime.datetime.now()
        #         print("left_motor:", self.motor_left.speed)
        #         print("right_motor:", self.motor_right.speed)

        #         ir_left_value = self.ir_left.proximity
        #         ir_right_value = self.ir_right.proximity
        #         diff = ir_left_value - ir_right_value
        #         distance_diff = self.back_cam.proximity
        #         motor_speed = (
        #             abs(self.motor_left.speed[0]) + abs(self.motor_right.speed[0])
        #         ) / 2
        #         run_time = end_time - start_time
        #         cal = self.calculate_calories(motor_speed, self.user_weight, run_time)
        #         running_distance = motor_speed * run_time
        #         self.user_data.append(
        #     {
        #         "id": id,
        #         "date": end_time,
        #         "comsumed_calories": cal,
        #         "running_distance": running_distance,
        #     },
        #     ignore_index=True,
        # )
        return None

    def stop(self):
        # self.motor_left.speed = 0, 0
        # self.motor_right.speed = 0, 0
        return None


if __name__ == "__main__":
    bundle = modi.MODI()  # (conn_type="ble", network_uuid="E87B3B00")
    car = PaceMakerCar(60, bundle)
    car.run()
    car.stop()
