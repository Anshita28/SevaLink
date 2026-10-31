package com.example.sevalink.domain.repository

import com.example.sevalink.domain.model.FallClassificationResult
import com.example.sevalink.domain.model.SensorData

/**
 * Interface for on-device fall detection AI inference.
 */
interface FallClassifier {
    /**
     * Classifies a window of sensor data as a fall or not.
     * @param windowedSensorData The 100-sample snapshot from the ring buffer.
     */
    suspend fun classify(windowedSensorData: List<SensorData>): FallClassificationResult
}
