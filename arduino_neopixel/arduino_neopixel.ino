// Skateboard Neopixel Program
// Controls 2*26 sets of neopixels on the bottom of my DIY electric skateboard
// Used an Arduino Nano to control the lights to save logic level conversion on the Pi Zero and worrying about task management
// Wiimote 'A' button triggers Pi that then triggers Arduino inputs that then turn on the lights

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6
#define BUTTON 7
#define INTERRUPT_PIN 2

Adafruit_NeoPixel strip = Adafruit_NeoPixel(26, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();
  pinMode(BUTTON, INPUT);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), ISRturn_off, RISING);
  }

void loop() {
  int value = 0;
  int but_val = 0;
  blank();
  while (true){
    but_val = digitalRead(BUTTON);
    if (but_val == 1){    
        sequence();
      }
    if (but_val == 0){
        blank();
      }
    }
  }

void ISRturn_off(){
  blank();
  }

void colorWipe(uint32_t c, uint8_t wait) {
  for(int i = (strip.numPixels()-1); i >= 0; i = i - 1) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
    }
  }

void sequence(){
  colorWipe(strip.Color(255, 0, 0), 25);
  colorWipe(strip.Color(0, 255, 0), 25); 
  colorWipe(strip.Color(0, 0, 255), 25);
  }

void blank(){
  colorWipe(strip.Color(0, 0, 0), 25);
  }
