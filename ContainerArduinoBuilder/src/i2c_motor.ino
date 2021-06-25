#include <Wire.h>

#define encoder0PinA 2

const boolean isDebug = false;

int encoder0Pos = 0;
unsigned int tmp_Pos = 1;

int number = 0;
boolean state = 0;

const float Pi = 3.141593;
const float diameter = 120; // [mm]

const int steps = 16;
double velocity = 0;

const float sampleTime = 200; // [ms]
union Encoder
{
  int val;
  byte b[2]; // Array de bytes de tamaño igual al tamaño de la primera variable: int = 2 bytes, float = 4 bytes
} myEncoder;

void toggleLed()
{
  if (state == 0){
    digitalWrite(13, HIGH); // set the LED on
    state = 1;
   } else {
    digitalWrite(13, LOW); // set the LED off
    state = 0;
   }
}

void doEncoderA()
{
  encoder0Pos = encoder0Pos + 1;
  // if (isDebug) Serial.println(encoder0Pos);
}

void receiveData(int byteCount)
{
  while(Wire.available())
  {
    number = Wire.read();
    Serial.print("number = ");
    Serial.println(number);

    if (number == 1) toggleLed();
  }
}

void requestEvent()
{
  Wire.write(myEncoder.b, sizeof(myEncoder.val));
}

void setup()
{
  Wire.begin(0x04);             // join i2c bus with address #2
  Wire.onReceive(receiveData); // register event
  Wire.onRequest(requestEvent); // register event

  if (isDebug) Serial.begin(115200);
  pinMode(13, OUTPUT);

  pinMode(encoder0PinA, INPUT_PULLUP);
  // FALLING
  // CHANGE
  attachInterrupt(0, doEncoderA, CHANGE);
  Serial.println("start");
}

void loop()
{
  myEncoder.val = encoder0Pos;

  if (isDebug)
  {
    // velocity = (encoder0Pos * (Pi * diameter) / steps) / sampleTime;
    Serial.println(encoder0Pos);
    // Serial.print("velocity: ");
    // Serial.print(velocity);
    // Serial.println(" m/s");
  }

  encoder0Pos = 0;
  delay(sampleTime);
}