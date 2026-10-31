package com.example.sevalink.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.example.sevalink.data.local.dao.CaretakerDao
import com.example.sevalink.data.local.dao.FallIncidentDao
import com.example.sevalink.data.local.entity.CaretakerEntity
import com.example.sevalink.data.local.entity.FallIncidentEntity

@Database(
    entities = [CaretakerEntity::class, FallIncidentEntity::class],
    version = 1,
    exportSchema = false
)
abstract class FallDetectionDatabase : RoomDatabase() {
    abstract fun caretakerDao(): CaretakerDao
    abstract fun fallIncidentDao(): FallIncidentDao
}
