/*
* 3S_Bearing_the_load.ino
* Description: A program running on Arduino DUE measuring acceleration, temperature and noise
* Author: Ken Yeh 475496
* Date: 02-12-2021
* Revision: 2.0
* GNU LESSER GENERAL PUBLIC LICENSE
* Copyright (C) 2022 Ken Yeh (P.)

* This program is free software: you can redistribute it and/or modify it under
* the terms of the GNU General Public License as published by the Free Software
* Foundation, either version 3 of the License, or (at your option) any later
* version.

* This program is distributed in the hope that it will be useful, but WITHOUT ANY
* WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR
* A PARTICULAR PURPOSE. See the GNU General Public License for more details.
*/
#define A0 7
#define A1 6
#define A2 5
#define A3 4
#define A4 3
#define A5 2
uint16_t sensor_data[6];
boolean conversionCompleted;

//Configuration
int sample_frequency = 20000;
int prescaler_value = 2;
int TC_RC_val = 84000000 / prescaler_value / sample_frequency; //Do check if it is still int before upload

void setup()
{
  // open a serial connection
  SerialUSB.begin(0);
  // Timer config
  // Internel clock selection MCK/2 MCK/8 MCK/32 MCK/128
  // TIMER_CLOCK1 Clock selected: internal MCK/2 clock signal (from PMC)
  // TIMER_CLOCK2 Clock selected: internal MCK/8 clock signal (from PMC)
  // TIMER_CLOCK3 Clock selected: internal MCK/32 clock signal (from PMC)
  // TIMER_CLOCK4 Clock selected: internal MCK/128 clock signal (from PMC)
  // TIMER_CLOCK5 Clock selected: internal SLCK clock signal (from PMC)
  PMC->PMC_PCER0 |= PMC_PCER0_PID29;                     // TC2 power ON : Timer Counter 0 channel 2 is TC2
  TC0->TC_CHANNEL[2].TC_CMR = TC_CMR_TCCLKS_TIMER_CLOCK1 // MCK/2, clk on rising edge
                              | TC_CMR_WAVE              // Waveform mode
                              | TC_CMR_WAVSEL_UP_RC      // UP mode with automatic trigger on RC Compare
                              | TC_CMR_ACPA_CLEAR        // Clear TIOA2 on RA compare match
                              | TC_CMR_ACPC_SET;         // Set TIOA2 on RC compare match

  TC0->TC_CHANNEL[2].TC_RC = TC_RC_val; //Sample frequency(Hz) = (Mck/prescaler_value)/TC_RC
  TC0->TC_CHANNEL[2].TC_RA = 2000;      //Any Duty cycle DO MANUALLY

  TC0->TC_CHANNEL[2].TC_CCR |= TC_CCR_SWTRG | TC_CCR_CLKEN; // Software trigger TC2 counter and enable

  // ADC config
  PMC->PMC_PCER1 |= PMC_PCER1_PID37; // ADC power on

  ADC->ADC_CR = ADC_CR_SWRST; // Reset ADC
  //ADC_MR Datasheet page 1333
  ADC->ADC_MR |= ADC_MR_TRGEN_EN            // Hardware trigger select
                 | ADC_MR_LOWRES_BITS_10    // 10 Bits resolution
                 | ADC_MR_TRGSEL_ADC_TRIG3; // Trigger by TIOA2

  ADC->ADC_IER = ADC_IER_EOC7 | ADC_IER_EOC6 | ADC_IER_EOC5 | ADC_IER_EOC4 | ADC_IER_EOC3 | ADC_IER_EOC2;  // Interrupt on End Of Conversions channel 7, 6 and 5
  NVIC_EnableIRQ(ADC_IRQn);                                                                                // Enable ADC interrupt
  ADC->ADC_CHER = ADC_CHER_CH7 | ADC_IER_EOC6 | ADC_IER_EOC5 | ADC_IER_EOC4 | ADC_IER_EOC3 | ADC_IER_EOC2; // Enable Channels 7,6,5,4,3,2(A0,A1,A2,A3,A4,A5)
}

void ADC_Handler()
{
  ADC->ADC_ISR;
  //Temperature sensor
  //DataSheet https://www.farnell.com/datasheets/1756131.pdf
  sensor_data[0] = ADC->ADC_CDR[A0];

  //Accelerometer
  sensor_data[1] = ADC->ADC_CDR[A1];
  sensor_data[2] = ADC->ADC_CDR[A2];

  //Microphone
  sensor_data[3] = ADC->ADC_CDR[A3];
  sensor_data[4] = ADC->ADC_CDR[A4];
  sensor_data[5] = ADC->ADC_CDR[A5];
  conversionCompleted = true;
}

void loop()
{
  if (conversionCompleted)
  {
    SerialUSB.write((uint8_t *)&sensor_data, 2 * 6); //Write the array to seral interface (2 bytes data per sensor)
    conversionCompleted = false;
  }
}