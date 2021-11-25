/*
* 3S_Bearing_the_load.ino
* Description: A program running on Arduino DUE measuring acceleration, temperature and noise
* Author: Ken Yeh 475496
* Date: 25-11-2021
* Revision: 1.0 
*/
int temperature_raw, accelerometer, microphone;
float R1 = 10000;
float logR2, R2, temp, temp_C;
float c1 = 1.129252142e-03, c2 = 2.341083183e-04, c3 = 0.8773267909e-07;
boolean conversionCompleted;
//Configuration
int sample_frequency = 3000;
int prescaler_value = 32;
int TC_RC_val = 84000000 / prescaler_value / sample_frequency;

void setup()
{
  // open a serial connection
  Serial.begin(115200);
  // Timer config
  // Internel clock selection MCK/2 MCK/8 MCK/32 MCK/128
  PMC->PMC_PCER0 |= PMC_PCER0_PID29;                     // TC2 power ON : Timer Counter 0 channel 2 is TC2
  TC0->TC_CHANNEL[2].TC_CMR = TC_CMR_TCCLKS_TIMER_CLOCK3 // MCK/32, clk on rising edge
                              | TC_CMR_WAVE              // Waveform mode
                              | TC_CMR_WAVSEL_UP_RC      // UP mode with automatic trigger on RC Compare
                              | TC_CMR_ACPA_CLEAR        // Clear TIOA2 on RA compare match
                              | TC_CMR_ACPC_SET;         // Set TIOA2 on RC compare match

  TC0->TC_CHANNEL[2].TC_RC = TC_RC_val;     //Sample frequency(Hz) = (Mck/prescaler_value)/TC_RC
  TC0->TC_CHANNEL[2].TC_RA = TC_RC_val / 2; //Any Duty cycle

  TC0->TC_CHANNEL[2].TC_CCR |= TC_CCR_SWTRG | TC_CCR_CLKEN; // Software trigger TC2 counter and enable

  // ADC config
  PMC->PMC_PCER1 |= PMC_PCER1_PID37; // ADC power on

  ADC->ADC_CR = ADC_CR_SWRST; // Reset ADC
  //ADC_MR Datasheet page 1333
  ADC->ADC_MR |= ADC_MR_TRGEN_EN            // Hardware trigger select
                 | ADC_MR_LOWRES_BITS_10    // 10 Bits resolution
                 | ADC_MR_TRGSEL_ADC_TRIG3; // Trigger by TIOA2

  ADC->ADC_IER = ADC_IER_EOC7 | ADC_IER_EOC6 | ADC_IER_EOC5;  // Interrupt on End Of Conversions channel 7, 6 and 5
  NVIC_EnableIRQ(ADC_IRQn);                                   // Enable ADC interrupt
  ADC->ADC_CHER = ADC_CHER_CH7 | ADC_IER_EOC6 | ADC_IER_EOC5; // Enable Channels 7,6,5(A0,A1,A2)
}

void ADC_Handler()
{
  ADC->ADC_ISR;
  //Accelerometer
  accelerometer = ADC->ADC_CDR[7]; 
  //Temperature sensor
  //DataSheet https://www.farnell.com/datasheets/1756131.pdf
  temperature_raw = ADC->ADC_CDR[6]; 
  //Microphone
  microphone = ADC->ADC_CDR[5]; 
  conversionCompleted = true;
}

void loop()
{
  if (conversionCompleted)
  {
    //Steinhart–Hart equation Calculator https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html
    R2 = R1 * (1023.0 / (float)temperature_raw - 1.0);
    logR2 = log(R2);
    temp = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2));
    temp_C = temp - 273.15;
    //Test Output
    //Serial.println(accelerometer);
    //Serial.println(microphone);
    //Serial.print(temp_C);
    //CSV Output
    Serial.println(String(temp_C) + "," + String(microphone) + "," + String(accelerometer));
    conversionCompleted = false;
  }
}