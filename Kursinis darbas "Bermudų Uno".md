# Kursinis darbas "Bermudų Uno"

Objektinio programavimo kursiniui darbui pasirinkau žaidimų temą. Bermudų Uno tikslas yra kaip ir standartinio Uno žaidimo - atsikratyti visų kortų iš savo rankų. Tačiau šis žaidimas išsiskiria nuo standartinio tuom, kad žaidėjas gali padėti kortas tik tada, kai turi tam pinigų. Tam, jog gautum pinigų žaidėjas privalo sužaisti klasikinį žaidimą "Minesweeper". Taigi norint laimėti "Uno" žaidėjas privalo laimėti "Minesweeper".


## Programos įjungimas

Tam jog įjungtumėte žaidimą **atsisiųskite** failus iš **GitHub** saugyklos, iškeltite failus ir paleiskite **Uno.exe** programą

## Žaidimo taisyklės

Žaidimo tikslas - **atsikratyti visų kortų**. Viduryje ekrano padėta dabartinė korta. Apačioje ekrano žaidėjo kortos. Viršuje ekrano priešininko/kompiuterio kortos. Kortą galima padėti, jeigu ji yra **tokios pat spalvos** arba turi **tokį patį skaičių** kaip ir viduryje ekrano esanti korta. Kad **padėtumėte** kortą spauskite **kairįjį pelės klavišą** and kortos. Žaidėjas gali padėti kortą tik tada kai turi **daugiau negu 0** Minesweeper pinigų (Minesweeper coins). Vienas kortos padėjimas kainuoją **vieną pinigą**. Paspaudus **juodą kortą**, kuri yra **viduryje ekrano** gaunama nauja korta. Kad **pimtumėtę** kortą spauskite **kairįjį pelės klavišą** and juodos kortos. Nauja korta kainuoja **vieną pinigą** Tam, jog gautum **Minesweeper pinigų** žaidėjas turi paspausti dėšinėje esantį mygtuką pavadinimu "Minesweeper". Už kiekvieną laimėta Minesweeper žaidimą žaidėjas gauna po **vieną pinigą**. Minesweeper žaidimo taisykles galite rasti [Minesweeper wiki](https://en.wikipedia.org/wiki/Minesweeper_(video_game)) puslapyje. Kad **atidarytumėte** kvadratą Minesweeper žaidime spauskite **kairįjį pelės mygtuką**. Kad **pažymėti** miną spauskite **dešinįjį pelės** mygtuką. Ėjimą pradeda žaidėjas.

# Objektinio programavimo implementacija

## Polymorphism
**Polimorfizmas (Polymorphism)** nurodo, kad per tą pačią sąsają galite pasiekti skirtingų tipų objektus.
```py
class Draw(ABC): # Line 113 Uno.py
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def draw_text(self):
        pass

class Text(Draw):
    def draw_text(self, text, size, color):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)
```
- Draw yra abstrakti bazinė klasė, apibrėžianti objektų, kuriuos galima piešti ekrane, sąsają.

- Text klasė yra konkretus Draw poklasis, kuriame pateikiamas konkretus draw_text įgyvendinimas.

- Text klasė nepaiso abstraktaus metodo draw_text apibrėžtas Draw klasėje su savo įgyvendinimu, pritaikytu tekstui piešti naudojant Pygame biblioteką.

- Nepaisant to, kad jie yra išreikšti kaip skirtingų klasių objektai (Draw ir Text), abu gali būti traktuojami vienodai, nes jie turi bendrą sąsają, kurią apibrėžia Draw klasė.
## Abstraction
**Abstrakcija (Abstraction)** naudojama norint paslėpti nereikalingą informaciją ir rodyti tik reikalingą informaciją sąveikaujantiems vartotojams.
```py
from abc import ABC, abstractmethod


class Draw(ABC): # Line 113 Uno.py
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod # <-
    def draw_text(self):
        pass
        
```
- Draw yra abstrakti bazinė klasė, apibrėžianti metodą draw_text.

- Text yra konkretus piešimo poklasis, įgyvendinantis draw_text metodą.

- Laikantis Draw sąsajos, Text gali būti naudojamas polimorfiškai su kitomis klasėmis, kurios paveldi iš Draw.
## Inheritance
**Paveldėjimas (Inheritance)** yra mechanizmas, leidžiantis klasei paveldėti savybes ir elgesį iš kitos klasės.
```py
class Text(Draw): # Line 124 Uno.py
	def draw_text(self, text, size, color): # <- 
	    font = pygame.font.Font(None, size)  
	    text_surface = font.render(text, True, color)  
	    text_rect = text_surface.get_rect(center=(self.x, self.y))  
	    screen.blit(text_surface, text_rect)
        
```
 - Text klasė paveldima iš Draw abstrakčios bazinės klasės.
 
 - Dėl paveldėjimo Text klasė gauna prieigą prie Draw klasės atributų ir metodų, tokių kaip "x" ir "y".
 
 - Text klasė pateikia savo abstrakčiojo metodo  draw_text, kuris yra apibrėžtas Draw abstrakčios bazės klasėje.
## Encapsulation
**Enkapsuliacija (Encapsulation)** Duomenų susiejimas su tais duomenimis veikiančiais metodais.
```py
class Button: #Line 78 Uno.py


    def __init__(self, text, x, y, width, height, color, text_color, action=None): # <-
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.font = pygame.font.Font(None, 30)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, self.text_rect)


    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
        
```
- Button klasės atributai (rect, text, color, text_color, action, font, text_surface, text_rect) yra įtraukti į klasės apibrėžimą. Jie pasiekiami ir modifikuojami tik naudojant klasės metodus.

- Metodas `__init__` inicijuoja Button objekto būseną nustatydamas jo atributus pagal pateiktus argumentus. Šie atributai saugo reikiamus duomenis mygtuko išvaizdai ir elgesiui.

- Draw metodas apima mygtuko atvaizdavimo ant tam tikro paviršiaus logiką. Jis naudoja Pygame biblioteką, kad nubrėžtų stačiakampį, vaizduojantį mygtuką, ir užfiksuotų tekstą ant jo.

- is_clicked metodas apima logiką, leidžiančią nustatyti, ar mygtukas spustelėtas, atsižvelgiant į pelės žymeklio padėtį. Jis patikrina, ar pateikta padėtis (pos) yra mygtuko stačiakampio (rect) ribose.
## Factory Method
**Gamyklinis metodas(Factory Method)**: kūrybinio dizaino modelis, suteikiantis sąsają objektams kurti superklasėje, tačiau leidžiantis poklasiams pakeisti kuriamų objektų tipą
```py
class Button: #Line 78 Uno.py
    def __init__(self, text, x, y, width, height, color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.font = pygame.font.Font(None, 30)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


```

 - Mygtukų klasė yra kaip produktas, vaizduojantis mygtukus, kuriuos galima sukurti.
 
 - Mygtukų klasės konstruktorius yra kaip gamyklinis metodas. Jis sukuria mygtukų egzempliorius su nurodytomis savybėmis, tokiomis kaip tekstas, padėtis, dydis, spalva ir veiksmas.
 
 - Kai reikia sukurti mygtuką, galima tiesiogiai sukurti mygtukų klasę su norimais parametrais.

## Template Method
**Šablono metodas(Template Method)**: elgesio dizaino modelis, leidžiantis apibrėžti algoritmo skeletą bazinėje klasėje ir leisti poklasiams nepaisyti žingsnių nekeičiant bendros algoritmo struktūros
```py
# Game loop 
clock = pygame.time.Clock()  # Line 220 Uno.py
running = True  
player_turn = True  
winner = None  
  
  
def check_points_from_minesweeper():  
    try:  
        with open("score_uno.txt", "r") as file:  
            score_uno = int(file.read())  
  
            return score_uno  
    except FileNotFoundError:  
        pass  
  
  
def update_points_from_minesweeper():  
    score_uno = check_points_from_minesweeper()  
    score_uno -= 1  
  with open("score_uno.txt", "w") as file:  
        file.write(str(score_uno))  
  
  
while running:  
    top_card = discard_pile[-1]  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
 elif event.type == pygame.MOUSEBUTTONUP:  
            if minesweeper_button.is_clicked(pygame.mouse.get_pos()) and event.button == 1:  
                spawn_program_and_die('.\\dist\\Minesweeper.exe')  # Due to shortage of ammunition it doesn't die  
  if winner and next_game_button.is_clicked(pygame.mouse.get_pos()) and event.button == 1:  
                reset_game()  
            elif player_turn:  
                top_card = discard_pile[-1]  
                if event.button == 1:  # Left mouse button  
  x, y = event.pos  
                    selected_card_index = card_clicked(x, y)  
                    if selected_card_index == 'random':  
                        # if len(deck) - 2 <= 0:  
 #     random.shuffle(deck) todo fix shuffle when out of cards  
  drawn_card = deck.pop()  
                        player_hand.append(drawn_card)  
                        player_turn = False  
  total_moves += 1  
  update_points_from_minesweeper()  
  
                    elif selected_card_index is not None:  
                        selected_card = player_hand[selected_card_index]  
                        if can_place_card(selected_card):  
                            player_hand.remove(selected_card)  
                            discard_pile.append(selected_card)  
                            player_turn = False  
  total_moves += 1  
  update_points_from_minesweeper()  
                            deck = [{'color': color, 'value': value} for color in colors for value in range(10)]  
                            random.shuffle(deck)  
  
    if not winner:  
        if not player_hand:  
            winner = "Player"  
  player_wins += 1  
  player_streak += 1  
  highest_streak = max(player_streak, highest_streak)  
  
        elif not computer_hand:  
            winner = "Computer"  
  computer_wins += 1  
  player_streak = 0  
  
  if not player_turn and not winner:  
        discarded_card = computer_play()  
        if discarded_card:  
            player_turn = True  
  
  check_points_from_minesweeper()  
    draw_game()  
  
save_highest_streak()  
  
pygame.quit()  
sys.exit()

```
- Įvykių tvarkymas: kilpa kartoja visus įvykius (pelės paspaudimus ir kt.) ir atitinkamai juos tvarko. Ši kilpos dalis yra atsakinga už vartotojo įvesties apdorojimą ir reagavimą į žaidimo įvykius.

- Žaidimo būsenos atnaujinimas: po įvykių tvarkymo kodas patikrina, ar yra nugalėtojas, ar atėjo kompiuterio eilė žaisti. Jei reikia, jis atnaujina žaidimo būseną, pvz., pakeičia nugalėtoją arba atnaujina žaidimo statistiką.

- Žaidimo piešimas: galiausiai kodas ekrane nubrėžia dabartinę žaidimo būseną. Tai apima kortelių, mygtukų ir teksto perteikimą, suteikiant vaizdinį grįžtamąjį ryšį.

## Observer pattern
**Stebėtojo modelis (Observer pattern)** yra elgesio dizaino modelis, leidžiantis kai kuriems objektams pranešti kitiems objektams apie jų būsenos pokyčius
```py
# Game loop
clock = pygame.time.Clock() # Line 220 Uno.py
running = True
player_turn = True
winner = None

while running:
    top_card = discard_pile[-1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            # Event handling
            if minesweeper_button.is_clicked(pygame.mouse.get_pos()) and event.button == 1:
                spawn_program_and_die('.\\dist\\Minesweeper.exe')
            if winner and next_game_button.is_clicked(pygame.mouse.get_pos()) and event.button == 1:
                reset_game()
            elif player_turn:
                top_card = discard_pile[-1]
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    selected_card_index = card_clicked(x, y)
                    # More event handling...
    # Updating the game state
    if not winner:
        if not player_hand:
            winner = "Player"
            player_wins += 1
            player_streak += 1
            highest_streak = max(player_streak, highest_streak)
        elif not computer_hand:
            winner = "Computer"
            computer_wins += 1
            player_streak = 0
    if not player_turn and not winner:
        discarded_card = computer_play()
        if discarded_card:
            player_turn = True
    # Drawing the game
    draw_game()

```

- pygame.event.get() nuskaito įvykių, įvykusių nuo paskutinio kvietimio į šią funkciją, sąrašą.

- Ciklas kartojasi per kiekvieną sąrašo įvykį.

- Kiekvienas įvykis stebimas ir apdorojamas pagal jo tipą (įvykis.tipas). Pavyzdžiui, kodas patikrina, ar įvykio pygame.QUIT, kai vartotojas uždaro žaidimo langą. Panašiai jis tikrina pygame.MOUSEBUTTONUP funkciją, kad apdorotu pelės paspaudimus.

- Atsižvelgiant į įvykio tipą ir kitas sąlygas, suaktyvinami atitinkami veiksmai. Pavyzdžiui, jei įvykis rodo pelės paspaudimą, kodas patikrina, ar paspaudžiami tam tikri mygtukai, ir atlieka atitinkamus veiksmus, pvz., pradeda naują žaidimą arba tvarko Minesweeper mygtuko paspaudimą.

## Command Pattern
**Komandų modelis(Command Pattern)** yra elgesio dizaino modelis, kuris užklausas ar paprastas operacijas paverčia objektais. Konversija leidžia atidėti arba nuotoliniu būdu vykdyti komandas.
```py
def spawn_program_and_die(program, exit_code=0): # Line 73 Uno.py
    os.startfile(program)  <-
    # sys.exit(exit_code)

while running: # Line 243 Uno.py
    top_card = discard_pile[-1]  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
 elif event.type == pygame.MOUSEBUTTONUP:  
            if minesweeper_button.is_clicked(pygame.mouse.get_pos()) and event.button == 1:  
                spawn_program_and_die('.\\dist\\Minesweeper.exe')  # Due to shortage of ammunition it doesn't die <-
  if winner and next_game_button.is_clicked(pygame.mouse.get_pos()) and event.button == 1:  
                reset_game()  
            elif player_turn:
            #Rest of the code
```
- "Minesweeper.exe" gali būti skaitomas kaip konkrečios komandos vykdymas, kai komanda (startfile Minesweeper.exe) yra įdėta į objektą.
# Iššūkiai, su kuriais susidurta implementuojant OP
- Python yra dinamiška kalba, o tai reiškia, kad kompiliavimo metu ji nevykdo griežto tipo tikrinimo. Nors ši funkcija suteikia lankstumo ir paprasto naudojimo, ji gali sukelti iššūkių dideliuose objektinio programavimo (OP) projektuose. Štai kodėl Python tam tikrais atvejais gali būti laikomas idealiu OP:
-- **Dinaminis rašymas**: Python dinaminis rašymass leidžia kintamiesiems keisti tipus vykdymo metu, todėl gali būti sunkiau išlaikyti ir suprasti sudėtingas objektų hierarchijas. Dideliuose projektuose šis lankstumas gali sukelti painiavą ir klaidas, jei nebus tinkamai valdomas.
--   **Enkapsuliavimas**: Python nevykdo enkapsuliavimo taip griežtai, kaip kai kurios kitos OP kalbos. Nors jis palaiko privačius, saugomus ir viešuosius narius per vardų suteikimo konvencijas, griežto vykdymo nėra, o tai gali sukelti atsitiktinę prieigą prie vidinių klasės narių.
-- **Įrankių ir IDE palaikymas**: nors Python labai pagerėjo ties OP įrankių ir IDE palaikymo požiūriu, jis vis tiek gali neatitikti palaikymo lygio tokioms kalboms kaip Java ar C++. Tai gali turėti įtakos kūrėjo patirčiai, ypač dirbant su sudėtingomis OP struktūromis ir pertvarkant kodą.
# Išvados
Python yra **nebloga** kalba žaidimų kūrimui atsižvelgiant į **bibliotekų įvairumą** ir **kalbos paprastumą**. Tačiau ši kalba limituoja žaidimų lankstumą iki **2D indie** žaidimų arba **Web** žaidimų.
 Šiam projektui sukūriau daugelį žaidimų mokymosi procese. Kiekvieno žaidimo **funkcijų implementacijos** kas kart darėsi vis lengvesnės ir rašant funckijas pradėjau galvoti apie implementacijas **ateities žaidimo versijoms**. Tik pradėjus projektą lankstumas buvo didelis kriterijus, nes kiekvienos funkcijos implementacija kode buvo itin **sudėtingas** ir **lėtas procesas**, kurio metu buvo sukurta dar daugiau **klaidų (bugs)**, kurios dar labiau sunkino darbą.
 
  Dėja, bet man **nepavyko** implementuoti **Testavimo**. Bandydamas implemenuoti testavimą redagavau kodą, tai sukėlė dar daugiau **klaidų (bugs)**, kurių taisymas pavėlino darbo įkėlimą (Pavėlavau 15min, nes GitHub nepatiko mano failai). Manau, kad jeigu būčiau  pasitreniravęs testuoti **mažas** ir **paprastas** funkcijas, sugebėčiau ištestuoti ir šį projektą, tačiau to nepadariau.
  
 Aš **nesu pilnai patenkintas** su **dabartine** projekto stadija. Pavadinčiau dabartinę versiją **Alpha testing** todėl toliau dirbu prie žaidimo versijos "**Bermudų Uno (Quality of depth)**", kurios tikslas yra implementuoti **daugiau žaidimų** ir pridėti **daugiau funkcionalumo** jau esantiems žaidimams (Leistis giliau į Bermudas). Pavyzdžiui: **visų Uno kortų** kaip: +2, +4, praleisti ėjimą, pakeisti spalvą, implementacija. Nauji žaidimai kaip **Space invaders**, kurio **taškai** naudojami Minesweeper žaidime.
 
 Įjungiant žaidimą iššoka **komandinė eilutė (Command prompt)**. Norėčiau, kad taip **nebūtų**, bet tam reikia programos **licencijos**. Šią problema planuojama išspręsti tolimesnėse Bermudų Uno iteracijose.
 
Šis projektas mane išmokė daug apie **žaidimų kūrimą** python kalba. **Paskaitų medžiagos išmokė OP funkcijas**, kurias galėjau naudoti žaidime. **Trivialias** žaidimams OP funkcijas teko mokytis **pačiam** iš kitų resursų, kaip GitHub, Stack Overflow, Reddit ir W3Schools. Man **labai patiko** šis projektas ir aš, **be abejonės**, toliau dirbsiu prie šio projekto. 

