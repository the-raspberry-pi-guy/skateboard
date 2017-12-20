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

  for(int i = 0; i <=4; i++){
    theaterChase(strip.Color(127, 127, 127), 25); // White
    theaterChase(strip.Color(127, 0, 0), 25); // Red
    theaterChase(strip.Color(0, 0, 127), 25); // Blue
  }
  rainbow(20);
  rainbowCycle(20);
  theaterChaseRainbow(25);
  
  }

void blank(){
  colorWipe(strip.Color(0, 0, 0), 25);
  }

/////// ADAFRUIT PRESET PATTERNS BELOW//////////


void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint8_t wait) {
  for (int j=0; j < 256; j++) {     // cycle all 256 colors in the wheel
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}
