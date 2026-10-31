package com.example.sevalink.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.sevalink.domain.model.Caretaker

@Entity(tableName = "caretakers")
data class CaretakerEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String,
    val phoneNumber: String,
    val relation: String,
    val isPrimary: Boolean
)

fun CaretakerEntity.toDomain() = Caretaker(
    id = id.toString(),
    name = name,
    phoneNumber = phoneNumber,
    relation = relation,
    isPrimary = isPrimary
)

fun Caretaker.toEntity() = CaretakerEntity(
    id = if (id.isEmpty()) 0 else id.toLong(),
    name = name,
    phoneNumber = phoneNumber,
    relation = relation,
    isPrimary = isPrimary
)
