#include <WiFi.h>
#include <HttpClient.h>
#include <Arduino.h>

#define PIN_ANALOG_IN 33
#define light_sensor 32
#define blue_led 13

char ssid[] = "UCInet Mobile Access";    // your network SSID (name) 
char pass[] = ""; // your network password (use for WPA, or use as key for WEP)

//char ssid[] = "kapi Residences";    // your network SSID (name) 
//char pass[] = "Kapiresidences000"; // your network password (use for WPA, or use as key for WEP)

// Name of the server we want to connect to
const char kHostname[] = "34.203.214.33";

// Number of milliseconds to wait without receiving any data before we give up
const int kNetworkTimeout = 30*1000;
// Number of milliseconds to wait if no data is available before trying again
const int kNetworkDelay = 1000;

int quiet = 0;
int initial_light = 0;
int initial_sound = 0;
int i;

void postInfo(HttpClient, char*);
int aboutLLight(int);

void setup() {
  Serial.begin(115200);

  i=0;

  pinMode(blue_led, OUTPUT);
  digitalWrite(blue_led, HIGH);

  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
}

void loop() {
  WiFiClient c;
  HttpClient http(c);
  int sound;
  int light;

  sound = analogRead(PIN_ANALOG_IN);
  light = analogRead(light_sensor);

  if(sound>=300 && initial_sound>=300)
  {
    digitalWrite(blue_led,LOW);
  }

  if(i!=0)
  {
    initial_sound = sound;
  }
  i =1;

  

  Serial.println(sound);
  Serial.println(light);
  
  if(!aboutLLight(light) || quiet!=sound)
  {
    char path[50];
    sprintf(path,"/data?light=%i&sound=%i", light, sound);
    initial_light = light;
    postInfo(http, path);
  }

  http.stop();
  
}

void postInfo(HttpClient http, char *path)
{
  int err = 0;
  err = http.post(kHostname,5000, path);
  if (err == 0)
  {
    Serial.println("startedRequest ok");

    err = http.responseStatusCode();
    if (err >= 0)
    {
      Serial.print("Got status code: ");
      Serial.println(err);
    }
    else
    {    
      Serial.print("Getting response failed: ");
      Serial.println(err);
    }
  }
  else
  {
    Serial.print("Connect failed: ");
    Serial.println(err);
  }
}

int aboutLLight(int focus)
{
  int value = focus - initial_light;
  int buffer = 100;
  if(value >= -buffer  || value <= buffer)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}

