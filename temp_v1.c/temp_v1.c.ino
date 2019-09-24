
void setup()
{
  Serial.begin(9600);
}

void loop() {
  float temp1;
  float temp2;
  float avg_temp;
  String temp = "Temperature: ";
  String degree = "*C";
  String output;
  temp1 = analogRead(A0);
  temp1 = temp1 * 0.48828125;
  temp2 = analogRead(A1);
  temp2 = temp2 * 0.48828125;
  avg_temp = (temp1 + temp2) / 2;
  output = temp + avg_temp + degree;
  Serial.println(output);
  
  delay(1000);
}
