package com.pyla.botbrawlstars

import android.app.Activity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView

class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val tvStatus = findViewById<TextView>(R.id.tv_status)
        val btnStart = findViewById<Button>(R.id.btn_start)
        val btnStop = findViewById<Button>(R.id.btn_stop)

        btnStart.setOnClickListener {
            tvStatus.text = "Estado: Iniciado"
        }

        btnStop.setOnClickListener {
            tvStatus.text = "Estado: Detenido"
        }
    }
}
