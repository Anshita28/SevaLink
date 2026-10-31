package com.example.sevalink.di

import com.example.sevalink.data.ml.MockFallClassifier
import com.example.sevalink.data.repository.CaretakerRepositoryImpl
import com.example.sevalink.data.repository.FallIncidentRepositoryImpl
import com.example.sevalink.data.repository.SettingsRepositoryImpl
import com.example.sevalink.domain.repository.CaretakerRepository
import com.example.sevalink.domain.repository.FallClassifier
import com.example.sevalink.domain.repository.FallIncidentRepository
import com.example.sevalink.domain.repository.SettingsRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindCaretakerRepository(impl: CaretakerRepositoryImpl): CaretakerRepository

    @Binds
    @Singleton
    abstract fun bindFallIncidentRepository(impl: FallIncidentRepositoryImpl): FallIncidentRepository

    @Binds
    @Singleton
    abstract fun bindSettingsRepository(impl: SettingsRepositoryImpl): SettingsRepository

    @Binds
    @Singleton
    abstract fun bindFallClassifier(impl: MockFallClassifier): FallClassifier
    // Swap the above line with the one below to use the real TFLite classifier
    // abstract fun bindFallClassifier(impl: TfliteFallClassifier): FallClassifier
}
