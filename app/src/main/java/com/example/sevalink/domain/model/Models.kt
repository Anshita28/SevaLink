package com.example.sevalink.domain.model

/**
 * Domain model representing a caretaker to be notified in case of a fall.
 */
data class Caretaker(
    val id: String = "",
    val name: String,
    val phoneNumber: String,
    val relation: String,
    val isPrimary: Boolean
)

/**
 * Domain model representing a detected fall incident.
 */
data class FallIncident(
    val id: String = "",
    val timestamp: Long,
    val severity: String,
    val isFalsePositive: Boolean
)

/**
 * Snapshot of sensor data at a specific point in time.
 */
data class SensorData(
    val ax: Float, val ay: Float, val az: Float,
    val gx: Float, val gy: Float, val gz: Float,
    val timestamp: Long
)

/**
 * Represents the current status of the fall detection system.
 */
enum class SystemStatus { IDLE, MONITORING, TRIGGERED, FALL_DETECTED }

/**
 * Combined UI state for the application.
 */
data class AppUiState(
    val systemStatus: SystemStatus = SystemStatus.IDLE,
    val liveSensorData: SensorData? = null,
    val caretakers: List<Caretaker> = emptyList(),
    val incidentHistory: List<FallIncident> = emptyList(),
    val countdownTimer: Int = 10,
    val smsAlertsEnabled: Boolean = true,
    val autoCallEnabled: Boolean = false,
    val loudSirenEnabled: Boolean = true,
    val sensitivityLevel: Int = 1 // 0=Low,1=Medium,2=High
)
