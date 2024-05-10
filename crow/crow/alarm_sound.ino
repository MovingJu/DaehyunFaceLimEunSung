#include <Arduino.h>
#include <DFPlayerMini_Fast.h>
#include <SoftwareSerial.h>

char c;
SoftwareSerial mp3Serial(10, 11);
DFPlayerMini_Fast DFPlayer;

void setup() {
  mp3Serial.begin(9600);
  Serial.begin(9600);
  DFPlayer.begin(mp3Serial, true);
  DFPlayer.volume(30);
}

void loop() {
  if(Serial.available()){
    c = Serial.read();
    if(c == '1'){
      DFPlayer.play(1);
      delay(5000);
    }
    else if(c == '2'){
      DFPlayer.play(2);
      delay(5000);
    }
  }
}
