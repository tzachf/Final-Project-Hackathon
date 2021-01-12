const int buttonPin = 2;     // the number of the pushbutton pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
char userInput;
int isPress = 0;

void setup() {

  Serial.begin(9600); // Initialize Serial communications with the PC
  while (!Serial);    // Do nothing if no Serial port is opened (added for Arduinos based on ATMEGA32U4)
  while (Serial.available()>=0){    
      userInput=Serial.read();
     if (userInput=='o'){ // pushbutton
       buttonState = 0;
       analogWrite(buttonPin, LOW); 
       pinMode(buttonPin, INPUT);
       break;
        }
      }
      ReadLines();
 // initialize the pushbutton pin as an input:
 pinMode(buttonPin, INPUT);
}

void loop() {}
void ReadLines(){ 
    //buttonState = digitalRead(buttonPin);
    while (buttonState == LOW && isPress==0){
      //delay(500);
      buttonState = digitalRead(buttonPin);
    }
    //Serial.println("");
   if (buttonState == HIGH){
        isPress=1;
        pinMode(buttonPin, OUTPUT);
        digitalWrite(buttonPin, HIGH);
        delay(500);
        digitalWrite(buttonPin, LOW);
        pinMode(buttonPin, INPUT);
        }         
    
    Serial.end();    // Ends the Serial communication once all data is received
   Serial.begin(9600);  // Re-establishes Serial communication , this causes deletion of anything previously stored in
}
 // read the state of the pushbutton value:
// buttonState = digitalRead(buttonPin);

 // check if the pushbutton is pressed.
 // if it is, the buttonState is HIGH:
// if (buttonState == HIGH) {
//   // turn LED on:
//   digitalWrite(ledPin, HIGH);
// } else {
//   // turn LED off:
//   digitalWrite(ledPin, LOW);
// }
//}
