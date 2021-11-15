import os
import codecs
import string

class Preprocessor:
    def __init__(self, \
                 TEXT_DIR = "dataset/sportsArticles/raw_data", \
                 MAX_DOC_COUNT = 100, \
                 lower_case=True, \
                 norm_spaces=True, \
                 punctuation=True):
        self.TEXT_DIR = TEXT_DIR
        self.MAX_DOC_COUNT = MAX_DOC_COUNT
        self.lower_case = lower_case
        self.norm_spaces = norm_spaces
        self.punctuation = punctuation

        self.corpus = []

    def load_texts_from_dir(self):
        for count, file_name in enumerate(os.listdir(self.TEXT_DIR)):
            if count < self.MAX_DOC_COUNT:
                file_path = self.TEXT_DIR+"/"+file_name
                with codecs.open(file_path, 'r', 'ISO-8859-1') as text_file:
                    text = reader = str(text_file.read())
                    clean_text = self.clean_text(text)
                    self.corpus.append(clean_text)

    def clean_text(self, txt):
        if self.lower_case:
            txt = txt.lower()
        if self.norm_spaces:
            txt = ' '.join(txt.split()) # split recognizes all types of whitespaces
        if self.punctuation:
            txt = ''.join(c for c in txt if c not in string.punctuation)
        return txt

    def load_test_cases(self):
        text1 = """
        Nadal was named Sportsman of the Year after a remarkable season in which he won the French Open, Wimbledon and US Open trophies while Spain's World Cup side were named Team of the Year at a glittering ceremony attended by celebrities and sporting greats.
        "It's an honour, in my name, that of my colleagues and the Spanish football federation, to receive this award from the world of sport," Spain coach Vicente del Bosque said in a live feed to the awards ceremony from the team's training base outside Madrid.
        American Alpine skier Lindsay Vonn, who won the Olympic downhill gold at the Vancouver Games last February just days after suffering a shin injury, was voted Sportswoman of the Year.
        Spain, the USA and Germany were the big winners with each country bagging two awards.
        
        There was a rapturous welcome for French football great Zinedine Zidane, who received the Lifetime Achievement Award in recognition of his remarkable career.
        The Spirit of Sport Award was presented to the European Ryder Cup Team to mark their emotional win over the United States in a match "which demonstrated great sportsmanship, golf played at the highest level and enormous and passionate galleries", a statement from the organisers said.
        The Laureus World Sports Awards, which recognise sporting achievement, are the premier honours on the international sporting calendar.
        Double Oscar winner Kevin Spacey hosted the event attended by celebrities from the world of sports and entertainment.
        The award winners were: 
        Laureus World Sportsman of the Year: Rafael Nadal (Spain) 
        Laureus World Sportswoman of the Year: Lindsey Vonn (US) 
        Laureus World Team of the Year: Spain World Cup 
        Team Laureus World Breakthrough of the Year: Martin Kaymer (Germany) 
        Laureus World Comeback of the Year: Valentino Rossi (Italy) 
        Laureus World Sportsperson of the Year with a Disability: Verena Bentele (Germany) 
        Laureus World Action Sportsperson of the Year: Kelly Slater (US)
        """
        self.corpus.append(text1)
        text2 = """
        Nadal was named Spodrtsman of the Year after a remadrkable season in which he won the French Open, Wimbledon and US Open trophies while Spain's World Cup side were named Team of the Year at a glittering ceremony attended by celebrities and sporting greats.
        "It's an honour, ddin my nadme, that of my codlleagues and the dSpanish football dfederation, to receive this award from the world of sport," Spain coach Vicente del Bosque said in a live feed to the awards ceremony from the team's training base outside Madrid.
        American Alpine skier Lindsay Vonnd, who won the Olympic downhill gold at the Vancouver Games last February just days after suffering a shin injury, was voted Sportswoman of the Year.
        Spain, the USA and Germany were the big dwinners with each country bagging two awards.
        dd
        There was a rapturous welcome for French football great Zinedine Zidane, who received the Lifetime Achievement Award in recognition of his remarkable career.
        The Spirit of Sport Award was presendted to the European Ryder Cup Team to dmark their emotional win over the United States in a match "which demonstrated great sportsmanship, golf played at the highest level and enormous and passionate galleries", a statement from the organisers said.
        The Laureus World Sports Awaasdrds, which recogdnise sporting achievement, are the premier honours on the international sporting calendar.
        Double Oscar winner Kevind Spacey hosted the event attended by celebrities from the world of sports and entertainment.
        The award winners were: 
        Laureus World Sportsman of the Year: Rafael Nadal (Spain) 
        Laureus World Sportdswoman of the Year: Lindsedy Vonn (US) 
        Laureusd Wordddld Team of the Year: Spain World Cup 
        Team Laureus Wdorld Breakthrough of the Yeadr: Martin Kaymer (Germany) 
        Laureusd World Comeback of the Year: Valentino Rossi (Italy) 
        Laureus World Sportdspersodn of the Year with a Disability: Verena Bentele (Germany) 
        Laureus World Actiond Sportsperson of the Year: dKelly Slater (US)
        """
        self.corpus.append(text2)
