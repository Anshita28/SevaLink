package com.example.sevalink.service

import android.app.*
import android.content.Context
import android.content.Intent
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.IBinder
import android.os.PowerManager
import android.util.Log
import androidx.core.app.NotificationCompat
import com.example.sevalink.R
import com.example.sevalink.domain.model.SensorData
import com.example.sevalink.domain.repository.FallClassifier
import com.example.sevalink.domain.repository.SettingsRepository
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.first
import java.util.concurrent.ConcurrentLinkedQueue
import javax.inject.Inject
import kotlin.math.sqrt

/**
 * Foreground service that monitors sensors for fall detection.
 * Uses a two-stage detection pipeline:
 * 1. Rule-based trigger (Stage 1)
 * 2. AI inference (Stage 2)
 */
@AndroidEntryPoint
class FallDetectionService : Service(), SensorEventListener {

    @Inject lateinit var settingsRepository: SettingsRepository
    @Inject lateinit var fallClassifier: FallClassifier

    private lateinit var sensorManager: SensorManager
    private var accelerometer: Sensor? = null
    private var gyroscope: Sensor? = null
    private var wakeLock: PowerManager.WakeLock? = null

    private val serviceScope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    // 100-sample circular buffer (~2s at 50Hz)
    private val bufferSize = 100
    private val sensorBuffer = ConcurrentLinkedQueue<SensorData>()

    private var currentAccel: FloatArray = floatArrayOf(0f, 0f, 0f)
    private var currentGyro: FloatArray = floatArrayOf(0f, 0f, 0f)

    private val NOTIFICATION_ID = 1
    private val CHANNEL_ID = "fall_detection_channel"

    // Stage 1 thresholds (will be loaded from settings)
    private var freefallThreshold = 5.0f
    private var impactThreshold = 18.0f

    override fun onCreate() {
        super.onCreate()
        sensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)

        val powerManager = getSystemService(Context.POWER_SERVICE) as PowerManager
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "FallDetection::WakeLock")
        
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        startForeground(NOTIFICATION_ID, createNotification())
        wakeLock?.acquire(10 * 60 * 1000L /*10 minutes*/)

        serviceScope.launch {
            settingsRepository.sensitivityLevel.collect { level ->
                updateThresholds(level)
            }
        }
        
        registerSensors()

        return START_STICKY
    }

    private fun registerSensors() {
        accelerometer?.let {
            sensorManager.registerListener(this, it, 20000) // 50Hz = 20ms
        }
        gyroscope?.let {
            sensorManager.registerListener(this, it, 20000)
        }
    }

    private fun updateThresholds(sensitivity: Int) {
        when (sensitivity) {
            0 -> { // Low
                freefallThreshold = 4.0f
                impactThreshold = 22.0f
            }
            1 -> { // Medium
                freefallThreshold = 5.0f
                impactThreshold = 18.0f
            }
            2 -> { // High
                freefallThreshold = 6.0f
                impactThreshold = 15.0f
            }
        }
    }

    override fun onSensorChanged(event: SensorEvent) {
        if (event.sensor.type == Sensor.TYPE_ACCELEROMETER) {
            currentAccel = event.values.clone()
            processSamples()
        } else if (event.sensor.type == Sensor.TYPE_GYROSCOPE) {
            currentGyro = event.values.clone()
        }
    }

    private fun processSamples() {
        val data = SensorData(
            ax = currentAccel[0], ay = currentAccel[1], az = currentAccel[2],
            gx = currentGyro[0], gy = currentGyro[1], gz = currentGyro[2],
            timestamp = System.currentTimeMillis()
        )

        sensorBuffer.add(data)
        if (sensorBuffer.size > bufferSize) {
            sensorBuffer.poll()
        }

        checkStage1(data)
    }

    private var inFreefall = false
    private var freefallStartTime = 0L

    private fun checkStage1(data: SensorData) {
        val magnitude = sqrt(data.ax * data.ax + data.ay * data.ay + data.az * data.az)

        if (!inFreefall && magnitude < freefallThreshold) {
            inFreefall = true
            freefallStartTime = data.timestamp
        } else if (inFreefall) {
            if (magnitude > impactThreshold) {
                val duration = data.timestamp - freefallStartTime
                if (duration in 200..1000) {
                    Log.d("FallDetection", "Stage 1 Triggered! Duration: $duration ms")
                    triggerStage2()
                }
                inFreefall = false
            } else if (data.timestamp - freefallStartTime > 1000) {
                // Freefall lasted too long, probably not a fall impact
                inFreefall = false
            }
        }
    }

    private fun triggerStage2() {
        val snapshot = sensorBuffer.toList()
        serviceScope.launch {
            val result = fallClassifier.classify(snapshot)
            if (result.isFall) {
                launchAlertOverlay()
            }
        }
    }

    private fun launchAlertOverlay() {
        // Implementation of alert overlay launch
        Log.i("FallDetection", "Fall Confirmed by Stage 2! Launching UI...")
        // In a real app, send broadcast or start activity with full screen intent
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        sensorManager.unregisterListener(this)
        wakeLock?.release()
        serviceScope.cancel()
    }

    private fun createNotificationChannel() {
        val serviceChannel = NotificationChannel(
            CHANNEL_ID,
            "Fall Detection Service Channel",
            NotificationManager.IMPORTANCE_LOW
        )
        val manager = getSystemService(NotificationManager::class.java)
        manager.createNotificationChannel(serviceChannel)
    }

    private fun createNotification(): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Fall Detection Active")
            .setContentText("Monitoring for falls in the background...")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .build()
    }
}
