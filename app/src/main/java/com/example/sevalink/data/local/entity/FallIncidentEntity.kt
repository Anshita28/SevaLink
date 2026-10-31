package com.example.sevalink.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.sevalink.domain.model.FallIncident

@Entity(tableName = "fall_incidents")
data class FallIncidentEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val timestamp: Long,
    val severity: String,
    val isFalsePositive: Boolean
)

fun FallIncidentEntity.toDomain() = FallIncident(
    id = id.toString(),
    timestamp = timestamp,
    severity = severity,
    isFalsePositive = isFalsePositive
)

fun FallIncident.toEntity() = FallIncidentEntity(
    id = if (id.isEmpty()) 0 else id.toLong(),
    timestamp = timestamp,
    severity = severity,
    isFalsePositive = isFalsePositive
)
