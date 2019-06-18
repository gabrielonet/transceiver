#include "si5351.h"
#include "Wire.h"

  int input = 0;   
  int temp_input = 0 ;
#define PLLB_FREQ    87600000000ULL

Si5351 si5351;

void setup()
{
  // Start serial and initialize the Si5351
  Serial.begin(57600);
  si5351.init(SI5351_CRYSTAL_LOAD_8PF, 0, 0);

  // Set VCXO osc to 876 MHz (146 MHz x 6), 40 ppm pull
  si5351.set_vcxo(PLLB_FREQ, 40);

  // Set CLK0 to be locked to VCXO
  si5351.set_ms_source(SI5351_CLK1, SI5351_PLLB);

  // Tune to 146 MHz center frequency
  si5351.set_freq_manual(900000000ULL, PLLB_FREQ, SI5351_CLK1);

  si5351.update_status();
  delay(500);
  pinMode(7, INPUT);

}

void loop()
{
  input = digitalRead(7);
  if ( input == 1 && temp_input == 0) { si5351.set_freq_manual(900070000ULL, PLLB_FREQ, SI5351_CLK1); temp_input = 1 ;   }
  if ( input == 0 && temp_input == 1) { si5351.set_freq_manual(900000000ULL, PLLB_FREQ, SI5351_CLK1); temp_input = 0 ;   }



  
}
