import time
from typing import Callable, List, Optional

import pandas as pd
from abc import *

from voice_synthesis import load_voice_model, text_to_speech

# 회전 보정 계수
MULTIPLIER_LR = 0.0060
# 감속 계수
MULTIPLIER_BACK = 0.8


@abstractmethod
def connect_to_your_robot():
    return True


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
        self.user_id = user_id
        self.default_speed = default_speed
        self.bundle = bundle
        self.user_data = pd.DataFrame(
            columns=["id", "timd", "user_calories", "running_distance"]
        )

    @staticmethod
    async def load_modi() -> None or Callable:
        try:
            bundle = connect_to_your_robot()
            return bundle
        except:
            return None

    @abstractmethod
    def run(self):
        return None

    @abstractmethod
    def stop(self):
        return None


if __name__ == "__main__":
    bundle = connect_to_your_robot()
    car = PaceMakerCar(1, 40, bundle)
    try:
        car.run()
    except KeyboardInterrupt:
        print("페이스메이커 작동을 멈춥니다.")
        car.stop()
