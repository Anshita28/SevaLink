package com.example.sevalink.di

import android.content.Context
import androidx.room.Room
import com.example.sevalink.data.local.FallDetectionDatabase
import com.example.sevalink.data.local.dao.CaretakerDao
import com.example.sevalink.data.local.dao.FallIncidentDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): FallDetectionDatabase {
        return Room.databaseBuilder(
            context,
            FallDetectionDatabase::class.java,
            "fall_detection_db"
        ).build()
    }

    @Provides
    fun provideCaretakerDao(database: FallDetectionDatabase): CaretakerDao {
        return database.caretakerDao()
    }

    @Provides
    fun provideFallIncidentDao(database: FallDetectionDatabase): FallIncidentDao {
        return database.fallIncidentDao()
    }
}
