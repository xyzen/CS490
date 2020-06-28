#import <SoftwareSerial.h>
SoftwareSerial hc05(2, 3); // RX | TX

// defines pins numbers
const int trigPin = 12;
const int echoPin = 11;
// defines variables
long duration;
int distance;

char flag;

void setup() 
{
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600);
  hc05.begin(9600);
  pinMode(8, OUTPUT);
}

void loop()
{
  if(hc05.available())  
  {
    flag = (char) hc05.read();
    Serial.println(flag);
    if(flag == '1') {
      digitalWrite(8, HIGH);
    } else if(flag == '0') {
      digitalWrite(8, LOW);
    }
  }
  get_dist();
  delay(250);           
}

void get_dist() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= (duration*0.034)/2;  //Speed of sound in air  at  standard condition = 0.034cm/µs
  // Prints the distance on the Serial Monitor
  Serial.println(distance);
  hc05.println(distance);       
}
