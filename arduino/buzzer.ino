const int botao1 = 3;
const int led1 = 2;
const int botao2 = 13;
const int led2 = 12;

bool portaTrancada = false;
int vencedor = 0;
unsigned long tempoAcendeu = 0;

void setup() {
  pinMode(botao1, INPUT_PULLUP);
  pinMode(led1, OUTPUT);
  pinMode(botao2, INPUT_PULLUP);
  pinMode(led2, OUTPUT);
}

void loop() {
  bool b1 = digitalRead(botao1) == LOW;
  bool b2 = digitalRead(botao2) == LOW;

  if (!portaTrancada) {
    if (b1) {
      vencedor = 1;
      portaTrancada = true;
      tempoAcendeu = millis();
      digitalWrite(led1, HIGH);
    } else if (b2) {
      vencedor = 2;
      portaTrancada = true;
      tempoAcendeu = millis();
      digitalWrite(led2, HIGH);
    }
  }

  if (portaTrancada && millis() - tempoAcendeu >= 5000) {
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
    portaTrancada = false;
    vencedor = 0;
  }
}