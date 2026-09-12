from typing import Dict


class ExplainabilityService:

    def explain_trend(
        self,
        trend_result: Dict
    ) -> Dict:

        if not trend_result:
            raise ValueError(
                "Trend result cannot be empty."
            )

        direction = trend_result.get(
            "trend_direction"
        )

        percentage_change = trend_result.get(
            "percentage_change"
        )

        first_value = trend_result.get(
            "first_value"
        )

        last_value = trend_result.get(
            "last_value"
        )

        strength = trend_result.get(
            "trend_strength"
        )

        if direction is None:
            raise ValueError(
                "Trend direction is missing."
            )

        # -----------------------------------------
        # Build finding
        # -----------------------------------------

        if direction == "Increasing":

            finding = (
                "The indicator shows an increasing trend."
            )

            risk_signal = (
                "The increasing trend may require "
                "policy attention depending on the "
                "indicator being measured."
            )

        elif direction == "Decreasing":

            finding = (
                "The indicator shows a decreasing trend."
            )

            risk_signal = (
                "The decreasing trend may require "
                "policy attention depending on the "
                "indicator being measured."
            )

        else:

            finding = (
                "The indicator is relatively stable "
                "over the observed period."
            )

            risk_signal = (
                "No clear directional trend was detected."
            )

        # -----------------------------------------
        # Build reasoning
        # -----------------------------------------

        if percentage_change is not None:

            reason = (
                f"The indicator changed from "
                f"{first_value} to {last_value}, "
                f"representing a "
                f"{percentage_change}% change."
            )

        else:

            reason = (
                f"The indicator changed from "
                f"{first_value} to {last_value}."
            )

        # -----------------------------------------
        # Determine pattern strength
        # -----------------------------------------

        if strength is not None:

            if strength >= 0.75:

                pattern_strength = "Strong"

            elif strength >= 0.50:

                pattern_strength = "Moderate"

            else:

                pattern_strength = "Weak"

        else:

            pattern_strength = "Unknown"

        return {

            "analysis_type": "Trend Analysis",

            "finding": finding,

            "reason": reason,

            "risk_signal": risk_signal,

            "pattern_strength": pattern_strength,

            "trend_direction": direction,

            "percentage_change": percentage_change
        }

    def explain_anomalies(
        self,
        anomaly_result: Dict
    ) -> Dict:

        if not anomaly_result:
            raise ValueError(
                "Anomaly result cannot be empty."
            )

        total_values = anomaly_result.get(
            "total_values",
            0
        )

        anomaly_count = anomaly_result.get(
            "anomaly_count",
            0
        )

        anomaly_percentage = anomaly_result.get(
            "anomaly_percentage",
            0
        )

        results = anomaly_result.get(
            "results",
            []
        )

        # -----------------------------------------
        # Extract detected anomaly values
        # -----------------------------------------

        anomaly_values = [
            item["value"]
            for item in results
            if item.get("is_anomaly")
        ]

        # -----------------------------------------
        # Build finding
        # -----------------------------------------

        if anomaly_count == 0:

            finding = (
                "No unusual values were detected "
                "in the analyzed data."
            )

            risk_signal = (
                "No anomaly-related risk signal "
                "was identified."
            )

        else:

            finding = (
                f"{anomaly_count} unusual value"
                f"{'s' if anomaly_count != 1 else ''} "
                f"{'was' if anomaly_count == 1 else 'were'} "
                "detected."
            )

            risk_signal = (
                "Detected anomalies should be reviewed "
                "to determine whether they represent "
                "real-world changes, data-quality issues, "
                "or exceptional events."
            )

        # -----------------------------------------
        # Build reasoning
        # -----------------------------------------

        if anomaly_count > 0:

            reason = (
                f"{anomaly_count} out of "
                f"{total_values} observations "
                f"({anomaly_percentage}%) were classified "
                f"as anomalous by the anomaly-detection "
                f"model."
            )

        else:

            reason = (
                f"All {total_values} observations were "
                "classified as normal."
            )

        return {

            "analysis_type": "Anomaly Detection",

            "finding": finding,

            "reason": reason,

            "risk_signal": risk_signal,

            "anomaly_count": anomaly_count,

            "anomaly_percentage": anomaly_percentage,

            "anomaly_values": anomaly_values
        }

    def build_analysis_summary(
        self,
        trend_result: Dict,
        anomaly_result: Dict
    ) -> Dict:

        trend_explanation = (
            self.explain_trend(
                trend_result
            )
        )

        anomaly_explanation = (
            self.explain_anomalies(
                anomaly_result
            )
        )

        return {

            "trend": trend_explanation,

            "anomalies": anomaly_explanation,

            "overall_finding": (
                "Analysis combines trend direction "
                "and anomaly detection results."
            )
        }