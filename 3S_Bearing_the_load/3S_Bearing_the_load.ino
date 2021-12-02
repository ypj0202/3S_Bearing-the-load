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
<<<<<<< HEAD
int sample_frequency = 20000;
int prescaler_value = 2;
int TC_RC_val = 84000000 / prescaler_value / sample_frequency; //Warning!!!!
=======
int sample_frequency = 3000;
int prescaler_value = 32;
int TC_RC_val = 84000000 / prescaler_value / sample_frequency;
>>>>>>> 2f352f5e0c64ba8fd1b5c0e9e046a71fa5f190e2

void setup()
{
  // open a serial connection
<<<<<<< HEAD
  SerialUSB.begin(0);
=======
  Serial.begin(115200);
>>>>>>> 2f352f5e0c64ba8fd1b5c0e9e046a71fa5f190e2
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
<<<<<<< HEAD
    char buffer[50];
    // int toSend[] = {temperature_raw, microphone, accelerometer};
    // int array_size = sizeof(toSend)/sizeof(int);
    // // char toSend[30];
    // for (int i = 0; i < array_size; i++)
    // {
    //   sprintf(buffer + strlen(buffer), "%d", toSend[i]);
    //   strcat(buffer, ",");
    //   // sprintf(buffer + strlen(buffer), "%d", microphone);
    // }
    // strcat(buffer, "\n");
  
    // sprintf(buffer, "%d", temperature_raw);
    // strcat(buffer, ",");
    // sprintf(buffer + strlen(buffer), "%d", microphone);
    // strcat(buffer, ",");
    // sprintf(buffer + strlen(buffer), "%d", accelerometer);
    // strcat(buffer, "\n");
   

    // SerialUSB.print(String(temperature_raw) + ',' + String(microphone) + ',' + String(accelerometer) + ',' + String(counter) + '\n');
    // SerialUSB.print(buffer);

    // SerialUSB.write((uint8_t*)&buffer, 50);

    
    SerialUSB.print("456,1023,1023\n");
=======
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
>>>>>>> 2f352f5e0c64ba8fd1b5c0e9e046a71fa5f190e2
    conversionCompleted = false;
  }
}