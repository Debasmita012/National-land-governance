from typing import Dict, List

import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyDetectionService:

    def __init__(
        self,
        contamination: float = 0.1,
        random_state: int = 42
    ):

        if not 0 < contamination < 0.5:
            raise ValueError(
                "contamination must be between 0 and 0.5."
            )

        self.contamination = contamination
        self.random_state = random_state

    def detect(
        self,
        values: List[float]
    ) -> Dict:

        if not values:
            raise ValueError(
                "Values cannot be empty."
            )

        if len(values) < 5:
            raise ValueError(
                "At least 5 values are required "
                "for anomaly detection."
            )

        try:

            numeric_values = [
                float(value)
                for value in values
            ]

        except (TypeError, ValueError):

            raise ValueError(
                "All values must be numeric."
            )

        data = np.array(
            numeric_values
        ).reshape(-1, 1)

        model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state
        )

        predictions = model.fit_predict(
            data
        )

        scores = model.decision_function(
            data
        )

        results = []

        anomaly_count = 0

        for index, value in enumerate(
            numeric_values
        ):

            is_anomaly = (
                predictions[index] == -1
            )

            if is_anomaly:
                anomaly_count += 1

            results.append(
                {
                    "index": index,
                    "value": value,
                    "is_anomaly": is_anomaly,
                    "anomaly_score": round(
                        float(scores[index]),
                        4
                    )
                }
            )

        normal_count = (
            len(numeric_values)
            - anomaly_count
        )

        return {

            "total_values": len(
                numeric_values
            ),

            "anomaly_count": anomaly_count,

            "normal_count": normal_count,

            "anomaly_percentage": round(
                (
                    anomaly_count
                    / len(numeric_values)
                ) * 100,
                2
            ),

            "results": results
        }
    