package com.example.sevalink.data.ml

import com.example.sevalink.domain.model.FallClassificationResult
import com.example.sevalink.domain.model.SensorData
import com.example.sevalink.domain.repository.FallClassifier
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.sqrt

/**
 * Heuristic stand-in for fall classification used until TFLite model is integrated.
 */
@Singleton
class MockFallClassifier @Inject constructor() : FallClassifier {
    override suspend fun classify(windowedSensorData: List<SensorData>): FallClassificationResult {
        // Simple heuristic: if peak magnitude in the window exceeds a high threshold
        val maxMagnitude = windowedSensorData.maxOfOrNull { data ->
            sqrt(data.ax * data.ax + data.ay * data.ay + data.az * data.az)
        } ?: 0f

        val isFall = maxMagnitude > 25.0f // Arbitrary high threshold for mock
        return FallClassificationResult(
            isFall = isFall,
            confidence = if (isFall) 0.85f else 0.1f
        )
    }
}
