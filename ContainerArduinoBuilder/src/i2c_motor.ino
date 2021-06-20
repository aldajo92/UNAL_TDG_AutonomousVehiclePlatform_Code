#include <Wire.h>

#define encoder0PinA 3

const boolean isDebug = true;

int encoder0Pos = 0;
unsigned int tmp_Pos = 1;

boolean A_set;
boolean flag = true;

const float Pi = 3.141593;
const float diameter = 12; // [mm]

const int steps = 10;

const float sampleTime = 100; // [ms]

double velocity = 0;

union Encoder
{
  int val;
  byte b[2]; // Array de bytes de tamaño igual al tamaño de la primera variable: int = 2 bytes, float = 4 bytes
} myEncoder;

void setup()
{
  Wire.begin(0x05);             // join i2c bus with address #2
  Wire.onRequest(requestEvent); // register event

  if (isDebug)
  {
    Serial.begin(115200);
  }

  pinMode(encoder0PinA, INPUT);
  pinMode(13, OUTPUT);

  attachInterrupt(0, doEncoderA, RISING);
}

void loop()
{
  myEncoder.val = encoder0Pos;

  if (isDebug)
  {
    velocity = (encoder0Pos * (Pi * diameter) / steps) / sampleTime;
    Serial.println(encoder0Pos);
    Serial.print("velocity: ");
    Serial.print(velocity);
    Serial.println(" m/s");
  }

  encoder0Pos = 0;
  flag = !flag;

  delay(sampleTime);
}

void doEncoderA()
{
  encoder0Pos = encoder0Pos + 1;
  Serial.println(encoder0Pos);
}

void requestEvent()
{
  Wire.write(myEncoder.b, sizeof(myEncoder.val));
  digitalWrite(13, flag);
}