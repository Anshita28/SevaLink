package com.example.sevalink.domain.model

/**
 * Result of the AI inference Stage 2.
 */
data class FallClassificationResult(
    val isFall: Boolean,
    val confidence: Float
)
