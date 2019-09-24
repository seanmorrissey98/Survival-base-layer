
/******************************************************************************
Flex_Sensor_Example.ino
Example sketch for SparkFun's flex sensors
  (https://www.sparkfun.com/products/10264)
Jim Lindblom @ SparkFun Electronics
April 28, 2016

Create a voltage divider circuit combining a flex sensor with a 47k resistor.
- The resistor should connect from A0 to GND.
- The flex sensor should connect from A0 to 3.3V
As the resistance of the flex sensor increases (meaning it's being bent), the
voltage at A0 should decrease.

Development environment specifics:
Arduino 1.6.7
******************************************************************************/
const int FLEX_PIN1 = A2; // Pin connected to voltage divider output
const int FLEX_PIN2 = A3;

// Measure the voltage at 5V and the actual resistance of your
// 47k resistor, and enter them below:
const float VCC = 4.98; // Measured voltage of Ardunio 5V line
const float R_DIV = 47500.0; // Measured resistance of 3.3k resistor

// Upload the code, then try to adjust these values to more
// accurately calculate bend degree.
const float STRAIGHT_RESISTANCE = 37300.0; // resistance when straight
const float BEND_RESISTANCE = 90000.0; // resistance at 90 deg
const int MAX_TIME = 10;
const int VARIANCE = 150;

float prevFlexR1 = 0;
float prevFlexR2 = 0;
float flexR1 = 0;
float flexR2 = 0;
float avgFlex = 0;
int timeCount = 0;
void setup() 
{
  Serial.begin(9600);
  pinMode(FLEX_PIN1, INPUT);
  pinMode(FLEX_PIN2, INPUT);
}

void printDouble( double val, unsigned int precision){
  Serial.print (int(val));
  Serial.print(".");
  unsigned int frac;
  if(val >=0)
    frac = (val - int(val)) * precision;
  else
    frac = (int(val) - val) * precision;
  int frac1 = frac;
  while(frac /=10)
    precision /=10;
  precision /=10;
  while( precision /=10)
    Serial.print("0");

  Serial.print(frac,DEC);
}

void loop() 
{
  // Read the ADC, and calculate voltage and resistance from it
  int flexADC1 = analogRead(FLEX_PIN1);
  int flexADC2 = analogRead(FLEX_PIN2);
  float flexV1 = flexADC1 * VCC / 1023.0;
  float flexV2 = flexADC2 * VCC / 1023.0;
  prevFlexR1 = flexR1;
  prevFlexR2 = flexR2;
  flexR1 = R_DIV * (VCC / flexV1 - 1.0);
  flexR2 = R_DIV * (VCC / flexV2 - 1.0);

  if(((prevFlexR1 <= flexR1+VARIANCE) || (prevFlexR1 >= flexR1-VARIANCE)) && ((prevFlexR2 <= flexR2+VARIANCE) || (prevFlexR2 >= flexR2-VARIANCE)))
    timeCount++;
  if(((prevFlexR1 >= (flexR1+VARIANCE)) || (prevFlexR1 <= (flexR1-VARIANCE))) || ((prevFlexR2 >= (flexR2+VARIANCE)) || (prevFlexR2 <= (flexR2-VARIANCE))))
    timeCount = 0;
  if((((prevFlexR1 <= (flexR1+VARIANCE)) && (prevFlexR1 >= (flexR1-VARIANCE))) && ((prevFlexR2 <= (flexR2+VARIANCE)) && (prevFlexR2 >= (flexR2-VARIANCE)))) && timeCount >= MAX_TIME)
    Serial.println("Move Around!!!!");
  
  Serial.print("Resistance: ");
  avgFlex = (flexR1 + flexR2)/2; 
  printDouble(avgFlex,100);
  Serial.print(" ohms" );
  Serial.print(" time:");
  Serial.print(timeCount);
  Serial.print("\n\n");

  delay(1000);
}
