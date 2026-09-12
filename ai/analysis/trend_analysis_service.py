from typing import Dict, List


class TrendAnalysisService:

    def analyze(
        self,
        values: List[float]
    ) -> Dict:

        if not values:
            raise ValueError(
                "Values cannot be empty."
            )

        if len(values) < 2:
            raise ValueError(
                "At least two values are required "
                "for trend analysis."
            )

        # -----------------------------------------
        # Convert values to float
        # -----------------------------------------

        try:

            values = [
                float(value)
                for value in values
            ]

        except (TypeError, ValueError):

            raise ValueError(
                "All values must be numeric."
            )

        # -----------------------------------------
        # Basic statistics
        # -----------------------------------------

        average_value = (
            sum(values) / len(values)
        )

        highest_value = max(values)
        lowest_value = min(values)

        # -----------------------------------------
        # Change calculation
        # -----------------------------------------

        first_value = values[0]
        last_value = values[-1]

        absolute_change = (
            last_value - first_value
        )

        if first_value != 0:

            percentage_change = (
                absolute_change
                / abs(first_value)
            ) * 100

        else:

            percentage_change = None

        # -----------------------------------------
        # Determine trend direction
        # -----------------------------------------

        if last_value > first_value:

            trend_direction = "Increasing"

        elif last_value < first_value:

            trend_direction = "Decreasing"

        else:

            trend_direction = "Stable"

        # -----------------------------------------
        # Calculate trend strength
        # -----------------------------------------

        differences = []

        for i in range(1, len(values)):

            difference = (
                values[i] - values[i - 1]
            )

            differences.append(difference)

        positive_changes = sum(
            1
            for difference in differences
            if difference > 0
        )

        negative_changes = sum(
            1
            for difference in differences
            if difference < 0
        )

        total_changes = len(differences)

        if trend_direction == "Increasing":

            trend_strength = (
                positive_changes
                / total_changes
            )

        elif trend_direction == "Decreasing":

            trend_strength = (
                negative_changes
                / total_changes
            )

        else:

            trend_strength = 0.0

        trend_strength = round(
            trend_strength,
            2
        )

        # -----------------------------------------
        # Final result
        # -----------------------------------------

        return {

            "trend_direction": trend_direction,

            "trend_strength": trend_strength,

            "first_value": first_value,

            "last_value": last_value,

            "absolute_change": round(
                absolute_change,
                2
            ),

            "percentage_change": (
                round(
                    percentage_change,
                    2
                )
                if percentage_change is not None
                else None
            ),

            "average_value": round(
                average_value,
                2
            ),

            "highest_value": highest_value,

            "lowest_value": lowest_value,

            "data_points": len(values)
        }